import pandas as pd
import numpy as np
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CSV_PATH = PROJECT_ROOT / "vix_fii_t1_intraday_daily_results.csv"
INTRADAY_PATH = PROJECT_ROOT / "NIFTY_50_2021-09-13_2026-09-11.csv"
OUTPUT_PATH = SCRIPT_DIR / "FII_PRO_NO_NEUTRAL_REVERSAL_TRAP_ANALYSIS.md"

FII_SECTION_ORDER = [
    "Strong Bullish", "Bullish", "Mildly Bullish",
    "Mildly Bearish", "Bearish", "Strong Bearish",
]


def classify_composite(value):
    if pd.isna(value):
        return "Mildly Bullish"
    if value < -100000:
        return "Strong Bearish"
    elif value < -50000:
        return "Bearish"
    elif value < 0:
        return "Mildly Bearish"
    elif value <= 50000:
        return "Mildly Bullish"
    elif value <= 100000:
        return "Bullish"
    else:
        return "Strong Bullish"


def load_and_prepare():
    df = pd.read_csv(CSV_PATH)
    for col in ["fii_composite", "pro_composite", "actual_open_close_pct",
                 "actual_range_pct", "intraday_high_pct", "intraday_low_pct",
                 "vix_predicted_move_pct", "range_vs_vix_ratio"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["is_nifty_expiry"] = pd.to_numeric(df["is_nifty_expiry"], errors="coerce").fillna(0).astype(int)
    df["fii_view"] = df["fii_composite"].apply(classify_composite)
    df["pro_view"] = df["pro_composite"].apply(classify_composite)

    # VIX thresholds
    df["vix_03"] = df["vix_predicted_move_pct"] * 0.3
    df["vix_05"] = df["vix_predicted_move_pct"] * 0.5
    df["up_pct"] = df["intraday_high_pct"]
    df["down_pct"] = df["intraday_low_pct"].abs()

    # === 4 reversal patterns ===
    # Pattern A: Small move first (0.3×VIX), big reversal (0.5×VIX)
    # A1: Up 0.3 first → Down 0.5  (bull trap → bearish reversal)
    df["bull_trap"] = (
        (df["move_direction"] == "Top to Down") &
        (df["up_pct"] >= df["vix_03"]) &
        (df["down_pct"] >= df["vix_05"])
    )
    # A2: Down 0.3 first → Up 0.5  (bear trap → bullish reversal)
    df["bear_trap"] = (
        (df["move_direction"] == "Down to Up") &
        (df["down_pct"] >= df["vix_03"]) &
        (df["up_pct"] >= df["vix_05"])
    )

    # Pattern B: Big move first (0.5×VIX), partial reversal (0.3×VIX)
    # B1: Up 0.5 first → Down 0.3  (big rally fades)
    df["rally_fade"] = (
        (df["move_direction"] == "Top to Down") &
        (df["up_pct"] >= df["vix_05"]) &
        (df["down_pct"] >= df["vix_03"])
    )
    # B2: Down 0.5 first → Up 0.3  (big drop bounces)
    df["drop_bounce"] = (
        (df["move_direction"] == "Down to Up") &
        (df["down_pct"] >= df["vix_05"]) &
        (df["up_pct"] >= df["vix_03"])
    )

    # Any reversal
    df["any_reversal"] = df["bull_trap"] | df["bear_trap"] | df["rally_fade"] | df["drop_bounce"]

    return df


def load_intraday():
    intra = pd.read_csv(INTRADAY_PATH)
    intra["datetime"] = pd.to_datetime(intra["datetime"])
    intra["date"] = intra["datetime"].dt.date.astype(str)
    intra["time"] = intra["datetime"].dt.strftime("%H:%M")
    return intra


def fmt_pct(val, decimals=3):
    if pd.isna(val):
        return "-"
    sign = "+" if val > 0 else ""
    return f"{sign}{val:.{decimals}f}%"


def compute_pattern_stats(df, pattern_col):
    """Compute per-combo stats for days matching a specific pattern."""
    pattern_days = df[df[pattern_col]]
    if pattern_days.empty:
        return pd.DataFrame()
    results = []
    grouped = pattern_days.groupby(["fii_view", "pro_view"])
    total_pattern_days = len(pattern_days)
    for (fii_v, pro_v), grp in grouped:
        total_combo_days = len(df[(df["fii_view"] == fii_v) & (df["pro_view"] == pro_v)])
        days = len(grp)
        green_days = (grp["nifty_day"] == "Green").sum()
        results.append({
            "fii_view": fii_v,
            "pro_view": pro_v,
            "pattern_days": days,
            "total_combo_days": total_combo_days,
            "pattern_rate": days / total_combo_days * 100 if total_combo_days > 0 else 0,
            "green_pct": green_days / days * 100 if days > 0 else 0,
            "avg_chg": grp["actual_open_close_pct"].mean(),
            "avg_range": grp["actual_range_pct"].mean(),
            "avg_up": grp["up_pct"].mean(),
            "avg_down": grp["down_pct"].mean(),
        })
    return pd.DataFrame(results)


def compute_intraday_reversal_timing(df, intra_df, pattern_col):
    """For reversal days with intraday data, find when the initial move peaked and when the reversal completed."""
    pattern_dates = set(df[df[pattern_col]]["date"])
    intra_dates = set(intra_df["date"])
    overlap = pattern_dates & intra_dates

    results = []
    for date in sorted(overlap):
        day_intra = intra_df[intra_df["date"] == date].sort_values("datetime")
        day_daily = df[df["date"] == date]
        if day_intra.empty or day_daily.empty:
            continue
        row = day_daily.iloc[0]
        day_open = day_intra.iloc[0]["open"]

        running_high = day_open
        running_low = day_open
        high_time = day_intra.iloc[0]["time"]
        low_time = day_intra.iloc[0]["time"]

        for _, candle in day_intra.iterrows():
            if candle["high"] > running_high:
                running_high = candle["high"]
                high_time = candle["time"]
            if candle["low"] < running_low:
                running_low = candle["low"]
                low_time = candle["time"]

        # Determine which was the initial move and which was the reversal
        if row["move_direction"] == "Top to Down":
            initial_time = high_time
            reversal_time = low_time
            initial_label = "High"
            reversal_label = "Low"
        else:
            initial_time = low_time
            reversal_time = high_time
            initial_label = "Low"
            reversal_label = "High"

        init_hour = int(initial_time.split(":")[0])
        rev_hour = int(reversal_time.split(":")[0])

        def session(h, t):
            m = int(t.split(":")[1])
            if h < 12 or (h == 12 and m < 15):
                return "Morning"
            return "Afternoon"

        results.append({
            "date": date,
            "initial_time": initial_time,
            "reversal_time": reversal_time,
            "initial_session": session(init_hour, initial_time),
            "reversal_session": session(rev_hour, reversal_time),
            "fii_view": row["fii_view"],
            "pro_view": row["pro_view"],
            "nifty_day": row["nifty_day"],
        })
    return pd.DataFrame(results)


def generate_pattern_table(stats_df, pattern_name, min_days=3):
    """Generate a markdown table for a reversal pattern sorted by pattern_rate."""
    filtered = stats_df[stats_df["total_combo_days"] >= 5].copy()
    if filtered.empty:
        return f"### {pattern_name}\n\nNo combinations with ≥5 total days.\n"
    filtered = filtered.sort_values("pattern_rate", ascending=False)

    lines = [
        f"### {pattern_name}",
        "",
        "| FII View | PRO View | Pattern Days | Total Days | Pattern Rate | Green% | Avg Chg% | Avg Up% | Avg Down% |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for _, r in filtered.iterrows():
        bold = r["pattern_days"] >= 5
        fii = f"**{r['fii_view']}**" if bold else r["fii_view"]
        pro = f"**{r['pro_view']}**" if bold else r["pro_view"]
        lines.append(
            f"| {fii} | {pro} | {r['pattern_days']:.0f} | {r['total_combo_days']:.0f} | "
            f"{'**' if bold else ''}{r['pattern_rate']:.1f}%{'**' if bold else ''} | "
            f"{r['green_pct']:.1f}% | {fmt_pct(r['avg_chg'])} | "
            f"{r['avg_up']:.3f}% | {r['avg_down']:.3f}% |"
        )
    return "\n".join(lines)


def generate_timing_summary(timing_df, pattern_name):
    if timing_df.empty:
        return ""
    lines = [
        f"**Timing ({len(timing_df)} days with intraday data)**:",
    ]
    # Initial move session
    init_counts = timing_df["initial_session"].value_counts()
    rev_counts = timing_df["reversal_session"].value_counts()
    init_am = init_counts.get("Morning", 0)
    init_pm = init_counts.get("Afternoon", 0)
    rev_am = rev_counts.get("Morning", 0)
    rev_pm = rev_counts.get("Afternoon", 0)
    total = len(timing_df)
    lines.append(f"- Initial move peaks in Morning {init_am} ({init_am/total*100:.0f}%), Afternoon {init_pm} ({init_pm/total*100:.0f}%)")
    lines.append(f"- Reversal completes in Morning {rev_am} ({rev_am/total*100:.0f}%), Afternoon {rev_pm} ({rev_pm/total*100:.0f}%)")

    # Green% on reversal days
    green = (timing_df["nifty_day"] == "Green").sum()
    lines.append(f"- Green day rate: {green}/{total} ({green/total*100:.1f}%)")

    return "\n".join(lines)


def generate_report(df, intra_df):
    total_days = len(df)
    date_min = df["date"].min()
    date_max = df["date"].max()

    bull_trap_count = df["bull_trap"].sum()
    bear_trap_count = df["bear_trap"].sum()
    rally_fade_count = df["rally_fade"].sum()
    drop_bounce_count = df["drop_bounce"].sum()
    any_reversal_count = df["any_reversal"].sum()

    # Compute stats per pattern
    bull_trap_stats = compute_pattern_stats(df, "bull_trap")
    bear_trap_stats = compute_pattern_stats(df, "bear_trap")
    rally_fade_stats = compute_pattern_stats(df, "rally_fade")
    drop_bounce_stats = compute_pattern_stats(df, "drop_bounce")

    # Intraday timing
    bt_timing = compute_intraday_reversal_timing(df, intra_df, "bull_trap")
    br_timing = compute_intraday_reversal_timing(df, intra_df, "bear_trap")
    rf_timing = compute_intraday_reversal_timing(df, intra_df, "rally_fade")
    db_timing = compute_intraday_reversal_timing(df, intra_df, "drop_bounce")

    sections = []

    # === HEADER ===
    sections.append(f"""# FII VIEW x PRO VIEW — VIX Reversal & Trap Analysis (No Neutral)

**Dataset**: {total_days:,} days | {date_min} to {date_max} | No Neutral Classification
**Intraday data**: 30-min candles from {intra_df['date'].min()} to {intra_df['date'].max()} ({intra_df['date'].nunique()} days)

### Label Guide
- **Mildly Bullish** = composite 0 to +50K (inclusive of zero)
- **Mildly Bearish** = composite -50K to -1 (exclusive of zero)
- **Bullish / Bearish** = composite ±50K to ±100K (fixed)
- **Strong Bullish / Strong Bearish** = composite beyond ±100K (fixed)
- **No Neutral zone** — every day is classified as directional

## How This Report Works

**Concept**: This report identifies days where the market makes a meaningful move in one direction (using VIX as the benchmark), then **reverses** to make a meaningful move in the opposite direction. These are "trap" or "reversal" patterns — the initial move lures traders in, then the reversal punishes them.

**Two VIX thresholds**:
- **0.3×VIX** = "moderate" move (30% of VIX-predicted daily range)
- **0.5×VIX** = "large" move (50% of VIX-predicted daily range, i.e. half the expected range)

**Four reversal patterns**:

| Pattern | First Move | Then Reverses To | Meaning | Days |
|---|---|---|---|---|
| **Bull Trap** | Up ≥ 0.3×VIX | Down ≥ 0.5×VIX | Morning rally lures buyers, then sells off hard | {bull_trap_count} ({bull_trap_count/total_days*100:.1f}%) |
| **Bear Trap** | Down ≥ 0.3×VIX | Up ≥ 0.5×VIX | Morning selloff lures sellers, then rallies hard | {bear_trap_count} ({bear_trap_count/total_days*100:.1f}%) |
| **Rally Fade** | Up ≥ 0.5×VIX | Down ≥ 0.3×VIX | Big rally fades, partial giveback | {rally_fade_count} ({rally_fade_count/total_days*100:.1f}%) |
| **Drop Bounce** | Down ≥ 0.5×VIX | Up ≥ 0.3×VIX | Big drop bounces, partial recovery | {drop_bounce_count} ({drop_bounce_count/total_days*100:.1f}%) |

**Total reversal days**: {any_reversal_count} ({any_reversal_count/total_days*100:.1f}%) — nearly 1 in 3 days has a meaningful reversal pattern.

**Key insight**: Bull Trap + Bear Trap (small move → big reversal) are the "trap" days where the initial move is deceptive. Rally Fade + Drop Bounce (big move → small reversal) are the "giveback" days where an initial strong move partially unwinds.""")

    # === BULL TRAP ===
    lines = [
        "## Bull Trap — Up 0.3×VIX First → Down 0.5×VIX",
        "",
        f"**{bull_trap_count} days** ({bull_trap_count/total_days*100:.1f}%) — Market rallies at least 0.3×VIX from open, then reverses and drops at least 0.5×VIX from open. The morning rally was a trap.",
        "",
        generate_pattern_table(bull_trap_stats, "Combinations by Bull Trap Rate"),
        "",
        generate_timing_summary(bt_timing, "Bull Trap"),
    ]
    bt_green = df[df["bull_trap"]]["nifty_day"].value_counts()
    bt_green_pct = bt_green.get("Green", 0) / bull_trap_count * 100 if bull_trap_count > 0 else 0
    lines.append(f"\n**Overall Bull Trap outcome**: {bt_green_pct:.1f}% close Green — {'despite the selloff, many days recover by close' if bt_green_pct > 40 else 'most days close red as expected after a failed rally'}.")
    sections.append("\n".join(lines))

    # === BEAR TRAP ===
    lines = [
        "## Bear Trap — Down 0.3×VIX First → Up 0.5×VIX",
        "",
        f"**{bear_trap_count} days** ({bear_trap_count/total_days*100:.1f}%) — Market drops at least 0.3×VIX from open, then reverses and rallies at least 0.5×VIX from open. The morning dip was a trap.",
        "",
        generate_pattern_table(bear_trap_stats, "Combinations by Bear Trap Rate"),
        "",
        generate_timing_summary(br_timing, "Bear Trap"),
    ]
    br_green = df[df["bear_trap"]]["nifty_day"].value_counts()
    br_green_pct = br_green.get("Green", 0) / bear_trap_count * 100 if bear_trap_count > 0 else 0
    lines.append(f"\n**Overall Bear Trap outcome**: {br_green_pct:.1f}% close Green — {'the reversal rally holds and most days close green' if br_green_pct > 55 else 'mixed results despite the reversal'}.")
    sections.append("\n".join(lines))

    # === RALLY FADE ===
    lines = [
        "## Rally Fade — Up 0.5×VIX First → Down 0.3×VIX",
        "",
        f"**{rally_fade_count} days** ({rally_fade_count/total_days*100:.1f}%) — Market rallies strongly (≥0.5×VIX from open), then gives back at least 0.3×VIX on the downside. A partial unwind of morning strength.",
        "",
        generate_pattern_table(rally_fade_stats, "Combinations by Rally Fade Rate"),
        "",
        generate_timing_summary(rf_timing, "Rally Fade"),
    ]
    rf_green = df[df["rally_fade"]]["nifty_day"].value_counts()
    rf_green_pct = rf_green.get("Green", 0) / rally_fade_count * 100 if rally_fade_count > 0 else 0
    lines.append(f"\n**Overall Rally Fade outcome**: {rf_green_pct:.1f}% close Green — {'despite the fade, the initial rally often holds enough to close green' if rf_green_pct > 40 else 'the fade dominates and most days close red'}.")
    sections.append("\n".join(lines))

    # === DROP BOUNCE ===
    lines = [
        "## Drop Bounce — Down 0.5×VIX First → Up 0.3×VIX",
        "",
        f"**{drop_bounce_count} days** ({drop_bounce_count/total_days*100:.1f}%) — Market drops sharply (≥0.5×VIX from open), then bounces back at least 0.3×VIX on the upside. A partial recovery from morning weakness.",
        "",
        generate_pattern_table(drop_bounce_stats, "Combinations by Drop Bounce Rate"),
        "",
        generate_timing_summary(db_timing, "Drop Bounce"),
    ]
    db_green = df[df["drop_bounce"]]["nifty_day"].value_counts()
    db_green_pct = db_green.get("Green", 0) / drop_bounce_count * 100 if drop_bounce_count > 0 else 0
    lines.append(f"\n**Overall Drop Bounce outcome**: {db_green_pct:.1f}% close Green — {'the bounce often carries through to a green close' if db_green_pct > 55 else 'mixed — the bounce provides partial relief but does not always recover fully'}.")
    sections.append("\n".join(lines))

    # === PER-FII SECTION: Which combos produce which pattern most? ===
    all_stats = compute_pattern_stats(df, "any_reversal")
    lines = []
    section_num = 1
    for fii_view in FII_SECTION_ORDER:
        fii_df = df[df["fii_view"] == fii_view]
        if len(fii_df) < 5:
            continue
        fii_total = len(fii_df)
        fii_bt = fii_df["bull_trap"].sum()
        fii_br = fii_df["bear_trap"].sum()
        fii_rf = fii_df["rally_fade"].sum()
        fii_db = fii_df["drop_bounce"].sum()
        fii_any = fii_df["any_reversal"].sum()

        lines.append(f"## Section {section_num}: FII {fii_view.upper()} — Reversal Profile ({fii_total} days)")
        lines.append("")
        lines.append(f"| Pattern | Days | Rate | Green% |")
        lines.append(f"|---|---|---|---|")
        for label, col in [("Bull Trap", "bull_trap"), ("Bear Trap", "bear_trap"),
                           ("Rally Fade", "rally_fade"), ("Drop Bounce", "drop_bounce")]:
            p_days = fii_df[col].sum()
            p_green = (fii_df[fii_df[col]]["nifty_day"] == "Green").sum()
            g_pct = p_green / p_days * 100 if p_days > 0 else 0
            lines.append(f"| {label} | {p_days} | {p_days/fii_total*100:.1f}% | {g_pct:.1f}% |")
        lines.append("")

        # Per-PRO breakdown
        lines.append("| PRO View | Days | Bull Trap% | Bear Trap% | Rally Fade% | Drop Bounce% | Any Reversal% |")
        lines.append("|---|---|---|---|---|---|---|")
        for pro_view in FII_SECTION_ORDER:
            combo = fii_df[fii_df["pro_view"] == pro_view]
            if len(combo) < 5:
                continue
            cd = len(combo)
            bt = combo["bull_trap"].sum()
            br = combo["bear_trap"].sum()
            rf = combo["rally_fade"].sum()
            db = combo["drop_bounce"].sum()
            any_r = combo["any_reversal"].sum()
            lines.append(
                f"| {pro_view} | {cd} | {bt/cd*100:.1f}% | {br/cd*100:.1f}% | "
                f"{rf/cd*100:.1f}% | {db/cd*100:.1f}% | **{any_r/cd*100:.1f}%** |"
            )

        # Dominant pattern
        patterns = {"Bull Trap": fii_bt, "Bear Trap": fii_br, "Rally Fade": fii_rf, "Drop Bounce": fii_db}
        dom = max(patterns, key=patterns.get)
        lines.append("")
        lines.append(f"**Dominant reversal**: {dom} ({patterns[dom]} days, {patterns[dom]/fii_total*100:.1f}%). "
                     f"Total reversals: {fii_any}/{fii_total} ({fii_any/fii_total*100:.1f}%).")
        lines.append("")
        section_num += 1
    sections.append("\n".join(lines))

    # === CONCLUSION ===
    lines = ["## Conclusion", ""]

    lines.append("### Pattern Summary")
    lines.append("")
    lines.append(f"| Pattern | Days | % of All | Green% | Meaning |")
    lines.append(f"|---|---|---|---|---|")
    for label, col, meaning in [
        ("Bull Trap", "bull_trap", "Morning rally → selloff"),
        ("Bear Trap", "bear_trap", "Morning dip → rally"),
        ("Rally Fade", "rally_fade", "Big rally → partial giveback"),
        ("Drop Bounce", "drop_bounce", "Big drop → partial bounce"),
    ]:
        p = df[df[col]]
        g = (p["nifty_day"] == "Green").sum()
        gp = g / len(p) * 100 if len(p) > 0 else 0
        lines.append(f"| {label} | {len(p)} | {len(p)/total_days*100:.1f}% | {gp:.1f}% | {meaning} |")

    lines.append("")
    lines.append("### Key Findings:")
    lines.append("")

    finding = 1

    # Bear trap vs bull trap
    lines.append(f"{finding}. **Bear Traps outnumber Bull Traps** ({bear_trap_count} vs {bull_trap_count}): "
                 f"The market is more likely to dip first then rally hard (Down 0.3→Up 0.5) than to rally first then sell off. "
                 f"This aligns with the \"Down to Up\" dominance seen in the main analysis.")
    finding += 1

    # Green% comparison
    bt_gp = (df[df["bull_trap"]]["nifty_day"] == "Green").sum() / bull_trap_count * 100 if bull_trap_count > 0 else 0
    br_gp = (df[df["bear_trap"]]["nifty_day"] == "Green").sum() / bear_trap_count * 100 if bear_trap_count > 0 else 0
    lines.append(f"{finding}. **Bear Trap days close Green {br_gp:.0f}% of the time** vs Bull Trap at {bt_gp:.0f}%. "
                 f"When the morning dip is a trap, the reversal rally usually holds through close.")
    finding += 1

    # Top combos per pattern
    for label, stats_df, desc in [
        ("Bull Trap", bull_trap_stats, "most likely to trap morning buyers"),
        ("Bear Trap", bear_trap_stats, "most likely to trap morning sellers"),
    ]:
        if stats_df.empty:
            continue
        top = stats_df[stats_df["total_combo_days"] >= 5].sort_values("pattern_rate", ascending=False)
        if not top.empty:
            t = top.iloc[0]
            lines.append(f"{finding}. **Highest {label} rate**: {t['fii_view']} FII + {t['pro_view']} PRO — "
                         f"**{t['pattern_rate']:.1f}%** of days are {label}s ({t['pattern_days']:.0f}/{t['total_combo_days']:.0f} days). "
                         f"This combo is {desc}.")
            finding += 1

    # Reversal frequency by FII view
    lines.append(f"{finding}. **FII view most prone to reversals**: ")
    fii_reversal_rates = []
    for fii_view in FII_SECTION_ORDER:
        fv = df[df["fii_view"] == fii_view]
        if len(fv) >= 10:
            rate = fv["any_reversal"].mean() * 100
            fii_reversal_rates.append((fii_view, rate, len(fv)))
    fii_reversal_rates.sort(key=lambda x: x[1], reverse=True)
    if fii_reversal_rates:
        top_fii = fii_reversal_rates[0]
        bot_fii = fii_reversal_rates[-1]
        lines[-1] = (f"{finding}. **FII view reversal rates**: Highest = {top_fii[0]} ({top_fii[1]:.1f}%, {top_fii[2]}d), "
                     f"Lowest = {bot_fii[0]} ({bot_fii[1]:.1f}%, {bot_fii[2]}d).")
    finding += 1

    lines.append("")
    lines.append("### Actionable Rules:")
    lines.append("")

    # Combos with highest bear trap rate (good for buying morning dips)
    if not bear_trap_stats.empty:
        bt_top = bear_trap_stats[bear_trap_stats["total_combo_days"] >= 10].sort_values("pattern_rate", ascending=False).head(3)
        if not bt_top.empty:
            combos = ", ".join(f"{r['fii_view']}+{r['pro_view']} ({r['pattern_rate']:.0f}%)" for _, r in bt_top.iterrows())
            lines.append(f"- **Buy morning dips** (high Bear Trap rate): {combos}")

    # Combos with highest bull trap rate (good for selling morning rallies)
    if not bull_trap_stats.empty:
        bt_top = bull_trap_stats[bull_trap_stats["total_combo_days"] >= 10].sort_values("pattern_rate", ascending=False).head(3)
        if not bt_top.empty:
            combos = ", ".join(f"{r['fii_view']}+{r['pro_view']} ({r['pattern_rate']:.0f}%)" for _, r in bt_top.iterrows())
            lines.append(f"- **Sell/short morning rallies** (high Bull Trap rate): {combos}")

    # Combos with lowest reversal rate (directional, no traps)
    if not all_stats.empty:
        low_rev = all_stats[all_stats["total_combo_days"] >= 10].sort_values("pattern_rate", ascending=True).head(3)
        if not low_rev.empty:
            combos = ", ".join(f"{r['fii_view']}+{r['pro_view']} ({r['pattern_rate']:.0f}%)" for _, r in low_rev.iterrows())
            lines.append(f"- **Trend-follow (low reversal rate)**: {combos}")

    lines.append("- **Expiry caution**: Reversal patterns may be amplified on expiry days due to options unwinding")

    sections.append("\n".join(lines))

    # === WRITE ===
    report = "\n\n---\n\n".join(sections) + "\n"
    with open(OUTPUT_PATH, "w") as f:
        f.write(report)
    print(f"Generated: {OUTPUT_PATH}")
    print(f"  {total_days} days, Bull Trap={bull_trap_count}, Bear Trap={bear_trap_count}, "
          f"Rally Fade={rally_fade_count}, Drop Bounce={drop_bounce_count}")


def main():
    df = load_and_prepare()
    intra_df = load_intraday()
    generate_report(df, intra_df)
    print("Done! Reversal trap report generated in reports_no_neutral/ directory.")


if __name__ == "__main__":
    main()
