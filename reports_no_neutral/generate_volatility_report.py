import pandas as pd
import numpy as np
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CSV_PATH = PROJECT_ROOT / "vix_fii_t1_intraday_daily_results.csv"
INTRADAY_PATH = PROJECT_ROOT / "NIFTY_50_2021-09-13_2026-09-11.csv"

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


def load_and_prepare(vix_fraction=0.5):
    df = pd.read_csv(CSV_PATH)
    for col in ["fii_composite", "pro_composite", "actual_open_close_pct",
                 "actual_range_pct", "intraday_high_pct", "intraday_low_pct",
                 "vix_predicted_move_pct", "range_vs_vix_ratio"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["is_nifty_expiry"] = pd.to_numeric(df["is_nifty_expiry"], errors="coerce").fillna(0).astype(int)
    df["fii_view"] = df["fii_composite"].apply(classify_composite)
    df["pro_view"] = df["pro_composite"].apply(classify_composite)

    # Volatility metrics — vix_fraction defines what fraction of VIX range = "significant" per side
    df["vix_threshold"] = df["vix_predicted_move_pct"] * vix_fraction
    df["up_ratio"] = df["intraday_high_pct"] / df["vix_threshold"]       # how much of threshold was used on upside
    df["down_ratio"] = df["intraday_low_pct"].abs() / df["vix_threshold"] # how much of threshold was used on downside
    df["both_min_ratio"] = df[["up_ratio", "down_ratio"]].min(axis=1)  # the weaker side
    df["total_swing_pct"] = df["intraday_high_pct"] + df["intraday_low_pct"].abs()  # total swing from open

    # Whipsaw tiers (ratio > 1.0 means the move exceeded the vix_fraction threshold)
    df["whipsaw_extreme"] = (df["up_ratio"] > 1.0) & (df["down_ratio"] > 1.0)   # both exceeded threshold
    df["whipsaw_strong"] = (df["up_ratio"] > 0.75) & (df["down_ratio"] > 0.75)   # both > 75% of threshold
    df["whipsaw_moderate"] = (df["up_ratio"] > 0.5) & (df["down_ratio"] > 0.5)   # both > 50% of threshold

    return df


def load_intraday():
    intra = pd.read_csv(INTRADAY_PATH)
    intra["datetime"] = pd.to_datetime(intra["datetime"])
    intra["date"] = intra["datetime"].dt.date.astype(str)
    intra["time"] = intra["datetime"].dt.strftime("%H:%M")
    return intra


def compute_intraday_swing_timing(daily_df, intra_df):
    """For days in both datasets, find when the high/low occurred (morning vs afternoon)."""
    merged_dates = set(daily_df["date"]) & set(intra_df["date"])
    results = []
    for date in sorted(merged_dates):
        day_intra = intra_df[intra_df["date"] == date].sort_values("datetime")
        day_daily = daily_df[daily_df["date"] == date]
        if day_intra.empty or day_daily.empty:
            continue

        row = day_daily.iloc[0]
        day_open = day_intra.iloc[0]["open"]

        # Track running high and low from open
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

        high_hour = int(high_time.split(":")[0])
        low_hour = int(low_time.split(":")[0])

        # Morning = before 12:15, Afternoon = 12:15 onwards
        high_session = "Morning" if high_hour < 12 or (high_hour == 12 and int(high_time.split(":")[1]) < 15) else "Afternoon"
        low_session = "Morning" if low_hour < 12 or (low_hour == 12 and int(low_time.split(":")[1]) < 15) else "Afternoon"

        # Determine swing pattern
        if high_session == "Morning" and low_session == "Afternoon":
            swing_pattern = "Up Morning → Down Afternoon"
        elif low_session == "Morning" and high_session == "Afternoon":
            swing_pattern = "Down Morning → Up Afternoon"
        elif high_session == "Morning" and low_session == "Morning":
            swing_pattern = "Both Morning"
        else:
            swing_pattern = "Both Afternoon"

        # Did high come first or low come first?
        if high_time < low_time:
            sequence = "High First"
        elif low_time < high_time:
            sequence = "Low First"
        else:
            sequence = "Simultaneous"

        results.append({
            "date": date,
            "high_time": high_time,
            "low_time": low_time,
            "high_session": high_session,
            "low_session": low_session,
            "swing_pattern": swing_pattern,
            "sequence": sequence,
        })

    return pd.DataFrame(results)


def compute_combo_volatility(df):
    results = []
    grouped = df.groupby(["fii_view", "pro_view"])
    for (fii_v, pro_v), grp in grouped:
        days = len(grp)
        results.append({
            "fii_view": fii_v,
            "pro_view": pro_v,
            "days": days,
            "avg_range_pct": grp["actual_range_pct"].mean(),
            "avg_vix_pct": grp["vix_predicted_move_pct"].mean(),
            "avg_range_vs_vix": grp["range_vs_vix_ratio"].mean(),
            "avg_up_pct": grp["intraday_high_pct"].mean(),
            "avg_down_pct": grp["intraday_low_pct"].abs().mean(),
            "avg_total_swing": grp["total_swing_pct"].mean(),
            "avg_up_ratio": grp["up_ratio"].mean(),
            "avg_down_ratio": grp["down_ratio"].mean(),
            "avg_both_min": grp["both_min_ratio"].mean(),
            "whipsaw_extreme_pct": grp["whipsaw_extreme"].mean() * 100,
            "whipsaw_strong_pct": grp["whipsaw_strong"].mean() * 100,
            "whipsaw_moderate_pct": grp["whipsaw_moderate"].mean() * 100,
            "whipsaw_extreme_count": grp["whipsaw_extreme"].sum(),
            "green_pct": (grp["nifty_day"] == "Green").mean() * 100,
            "avg_chg": grp["actual_open_close_pct"].mean(),
        })
    return pd.DataFrame(results)


def fmt_pct(val, decimals=2):
    if pd.isna(val):
        return "-"
    sign = "+" if val > 0 else ""
    return f"{sign}{val:.{decimals}f}%"


def generate_report(df, intra_df, vix_fraction=0.5, output_path=None):
    stats = compute_combo_volatility(df)
    swing_timing = compute_intraday_swing_timing(df, intra_df)

    # Merge swing timing back
    df_with_swing = df.merge(swing_timing, on="date", how="left")

    total_days = len(df)
    date_min = df["date"].min()
    date_max = df["date"].max()
    extreme_days = df["whipsaw_extreme"].sum()
    strong_days = df["whipsaw_strong"].sum()

    frac_label = f"{vix_fraction:.1f}×VIX" if vix_fraction != 0.5 else "Half-VIX"
    frac_pct = f"{vix_fraction*100:.0f}%"

    sections = []

    # === HEADER ===
    sections.append(f"""# FII VIEW x PRO VIEW — Volatility & Whipsaw Analysis ({frac_label} Threshold, No Neutral)

**Dataset**: {total_days:,} days | {date_min} to {date_max} | No Neutral Classification
**Intraday data**: 30-min candles from {intra_df['date'].min()} to {intra_df['date'].max()} ({intra_df['date'].nunique()} days)
**VIX Threshold**: {frac_label} = VIX predicted move × {vix_fraction} — a move in one direction must exceed this to count as "significant"

### Label Guide
- **Mildly Bullish** = composite 0 to +50K (inclusive of zero)
- **Mildly Bearish** = composite -50K to -1 (exclusive of zero)
- **Bullish / Bearish** = composite ±50K to ±100K (fixed)
- **Strong Bullish / Strong Bearish** = composite beyond ±100K (fixed)
- **No Neutral zone** — every day is classified as directional

## How This Report Works

**Concept**: On any given day, VIX predicts an expected daily range. A "whipsaw" day is when the market swings significantly in BOTH directions from the open — going up by a meaningful fraction of the VIX range AND down by a meaningful fraction.

**Threshold used**: **{frac_label}** = VIX predicted move × {vix_fraction}. {'This is the standard half-VIX benchmark.' if vix_fraction == 0.5 else f'This is a tighter threshold than half-VIX (0.5), so MORE days qualify as whipsaw since the bar for significance is lower ({frac_pct} of VIX vs 50%).' if vix_fraction < 0.5 else f'This is a wider threshold than half-VIX (0.5), so FEWER days qualify.'}

**Metrics**:
- **{frac_label}** = VIX predicted move × {vix_fraction}. This is the benchmark for a "significant" move in one direction.
- **Up Ratio** = (High - Open) / {frac_label}. How much of the VIX budget was used going up.
- **Down Ratio** = |Low - Open| / {frac_label}. How much of the VIX budget was used going down.
- **Whipsaw Extreme**: Both Up Ratio AND Down Ratio > 1.0 (both sides exceeded {frac_label})
- **Whipsaw Strong**: Both > 0.75
- **Whipsaw Moderate**: Both > 0.50

**Overall Stats**:
- Whipsaw Extreme days: **{extreme_days}** ({extreme_days/total_days*100:.1f}% of all days)
- Whipsaw Strong days: **{strong_days}** ({strong_days/total_days*100:.1f}% of all days)
- Average Up Ratio: {df['up_ratio'].mean():.2f} | Average Down Ratio: {df['down_ratio'].mean():.2f}""")

    # === MASTER TABLE: Sorted by Whipsaw Extreme % ===
    filtered = stats[stats["days"] >= 5].copy()
    sorted_by_whipsaw = filtered.sort_values("whipsaw_extreme_pct", ascending=False)

    lines = [
        "## Master Table — Combinations Sorted by Whipsaw Extreme %",
        "",
        "Combinations with ≥5 days, sorted by % of days that had extreme whipsaw (both sides > half VIX).",
        "",
        "| FII View | PRO View | Days | Whipsaw Extreme % | Whipsaw Strong % | Avg Total Swing | Avg Range% | Range/VIX | Green% | Avg Chg% |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for _, r in sorted_by_whipsaw.iterrows():
        bold = r["whipsaw_extreme_pct"] >= 15
        fii = f"**{r['fii_view']}**" if bold else r["fii_view"]
        pro = f"**{r['pro_view']}**" if bold else r["pro_view"]
        lines.append(
            f"| {fii} | {pro} | {r['days']:.0f} | "
            f"{'**' if bold else ''}{r['whipsaw_extreme_pct']:.1f}%{'**' if bold else ''} | "
            f"{r['whipsaw_strong_pct']:.1f}% | "
            f"{r['avg_total_swing']:.3f}% | "
            f"{r['avg_range_pct']:.3f}% | "
            f"{r['avg_range_vs_vix']:.2f} | "
            f"{r['green_pct']:.1f}% | "
            f"{fmt_pct(r['avg_chg'], 3)} |"
        )
    sections.append("\n".join(lines))

    # === TOP 10 MOST VOLATILE (by total swing) ===
    top_swing = filtered.sort_values("avg_total_swing", ascending=False).head(10)
    lines = [
        "## Top 10 Highest Total Swing Combinations (≥5 days)",
        "",
        "Total Swing = (High - Open) + |Low - Open|. This measures how much ground the market covered in both directions.",
        "",
        "| Rank | FII View | PRO View | Days | Avg Total Swing | Avg Up% | Avg Down% | Avg Range% | VIX Pred% | Whipsaw Ex% | Green% |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for rank, (_, r) in enumerate(top_swing.iterrows(), 1):
        lines.append(
            f"| {rank} | {r['fii_view']} | {r['pro_view']} | {r['days']:.0f} | "
            f"**{r['avg_total_swing']:.3f}%** | "
            f"{r['avg_up_pct']:.3f}% | {r['avg_down_pct']:.3f}% | "
            f"{r['avg_range_pct']:.3f}% | {r['avg_vix_pct']:.3f}% | "
            f"{r['whipsaw_extreme_pct']:.1f}% | {r['green_pct']:.1f}% |"
        )
    sections.append("\n".join(lines))

    # === TOP 10 LEAST VOLATILE ===
    bottom_swing = filtered.sort_values("avg_total_swing", ascending=True).head(10)
    lines = [
        "## Top 10 Lowest Total Swing Combinations (≥5 days)",
        "",
        "These combinations produce the calmest, most directional days with minimal whipsaw.",
        "",
        "| Rank | FII View | PRO View | Days | Avg Total Swing | Avg Up% | Avg Down% | Avg Range% | Whipsaw Ex% | Green% |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for rank, (_, r) in enumerate(bottom_swing.iterrows(), 1):
        lines.append(
            f"| {rank} | {r['fii_view']} | {r['pro_view']} | {r['days']:.0f} | "
            f"**{r['avg_total_swing']:.3f}%** | "
            f"{r['avg_up_pct']:.3f}% | {r['avg_down_pct']:.3f}% | "
            f"{r['avg_range_pct']:.3f}% | "
            f"{r['whipsaw_extreme_pct']:.1f}% | {r['green_pct']:.1f}% |"
        )
    sections.append("\n".join(lines))

    # === ASYMMETRY ANALYSIS: Up-biased vs Down-biased swings ===
    filtered["swing_bias"] = filtered["avg_up_ratio"] - filtered["avg_down_ratio"]
    up_biased = filtered[filtered["swing_bias"] > 0.15].sort_values("swing_bias", ascending=False)
    down_biased = filtered[filtered["swing_bias"] < -0.15].sort_values("swing_bias", ascending=True)

    lines = [
        "## Swing Asymmetry — Which Side Dominates?",
        "",
        "**Swing Bias** = Avg Up Ratio - Avg Down Ratio. Positive = upside swings dominate, Negative = downside swings dominate.",
        "",
        "### Up-Biased Combinations (swing bias > +0.15)",
        "These combinations swing MORE to the upside relative to VIX. The upside move consumes more of the VIX budget.",
        "",
        "| FII View | PRO View | Days | Avg Up Ratio | Avg Down Ratio | Swing Bias | Green% | Avg Chg% |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for _, r in up_biased.iterrows():
        lines.append(
            f"| {r['fii_view']} | {r['pro_view']} | {r['days']:.0f} | "
            f"{r['avg_up_ratio']:.2f} | {r['avg_down_ratio']:.2f} | "
            f"**+{r['swing_bias']:.2f}** | {r['green_pct']:.1f}% | {fmt_pct(r['avg_chg'], 3)} |"
        )

    lines.append("")
    lines.append("### Down-Biased Combinations (swing bias < -0.15)")
    lines.append("These combinations swing MORE to the downside. Sellers dominate the intraday action.")
    lines.append("")
    lines.append("| FII View | PRO View | Days | Avg Up Ratio | Avg Down Ratio | Swing Bias | Green% | Avg Chg% |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for _, r in down_biased.iterrows():
        lines.append(
            f"| {r['fii_view']} | {r['pro_view']} | {r['days']:.0f} | "
            f"{r['avg_up_ratio']:.2f} | {r['avg_down_ratio']:.2f} | "
            f"**{r['swing_bias']:.2f}** | {r['green_pct']:.1f}% | {fmt_pct(r['avg_chg'], 3)} |"
        )
    sections.append("\n".join(lines))

    # === PER-FII SECTION VOLATILITY ===
    lines = []
    section_num = 1
    for fii_view in FII_SECTION_ORDER:
        section_stats = filtered[filtered["fii_view"] == fii_view].copy()
        if section_stats.empty:
            continue
        section_stats = section_stats.sort_values("whipsaw_extreme_pct", ascending=False)
        total_d = section_stats["days"].sum()
        avg_whipsaw = (section_stats["whipsaw_extreme_pct"] * section_stats["days"]).sum() / total_d

        lines.append(f"## Section {section_num}: FII {fii_view.upper()} — Volatility Profile ({total_d} days, {avg_whipsaw:.1f}% avg whipsaw)")
        lines.append("")
        lines.append("| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|")

        for _, r in section_stats.iterrows():
            lines.append(
                f"| {r['pro_view']} | {r['days']:.0f} | "
                f"{r['whipsaw_extreme_pct']:.1f}% | {r['whipsaw_strong_pct']:.1f}% | "
                f"{r['avg_total_swing']:.3f}% | {r['avg_range_pct']:.3f}% | "
                f"{r['avg_range_vs_vix']:.2f} | "
                f"{r['avg_up_ratio']:.2f} | {r['avg_down_ratio']:.2f} | "
                f"{r['green_pct']:.1f}% |"
            )

        # Insight
        most_volatile = section_stats.iloc[0]
        least_volatile = section_stats.iloc[-1] if len(section_stats) > 1 else section_stats.iloc[0]
        lines.append("")
        lines.append(
            f"**Volatility pattern**: Most whipsaw with {most_volatile['pro_view']} PRO "
            f"({most_volatile['whipsaw_extreme_pct']:.0f}% extreme days, "
            f"{most_volatile['avg_total_swing']:.3f}% avg swing). "
            f"Calmest with {least_volatile['pro_view']} PRO "
            f"({least_volatile['whipsaw_extreme_pct']:.0f}% extreme, "
            f"{least_volatile['avg_total_swing']:.3f}% avg swing)."
        )
        lines.append("")
        section_num += 1
    sections.append("\n".join(lines))

    # === INTRADAY SWING TIMING ANALYSIS ===
    whipsaw_dates = set(df[df["whipsaw_extreme"] == True]["date"])
    swing_whipsaw = df_with_swing[
        (df_with_swing["date"].isin(whipsaw_dates)) &
        (df_with_swing["swing_pattern"].notna())
    ]

    if not swing_whipsaw.empty:
        lines = [
            "## Intraday Swing Timing — When Do Whipsaws Happen?",
            "",
            f"Analysis of {len(swing_whipsaw)} extreme whipsaw days with intraday data available.",
            "",
        ]

        # Overall swing pattern distribution
        pattern_counts = swing_whipsaw["swing_pattern"].value_counts()
        lines.append("### Overall Swing Pattern (Extreme Whipsaw Days)")
        lines.append("")
        lines.append("| Pattern | Days | % |")
        lines.append("|---|---|---|")
        for pattern, count in pattern_counts.items():
            lines.append(f"| {pattern} | {count} | {count/len(swing_whipsaw)*100:.1f}% |")

        # Sequence: high first or low first
        seq_counts = swing_whipsaw["sequence"].value_counts()
        lines.append("")
        lines.append("### Sequence — Does High or Low Come First?")
        lines.append("")
        lines.append("| Sequence | Days | % |")
        lines.append("|---|---|---|")
        for seq, count in seq_counts.items():
            lines.append(f"| {seq} | {count} | {count/len(swing_whipsaw)*100:.1f}% |")

        # By FII view
        lines.append("")
        lines.append("### Swing Pattern by FII View (Extreme Whipsaw Days)")
        lines.append("")
        lines.append("| FII View | Days | Up AM→Down PM | Down AM→Up PM | Both AM | Both PM |")
        lines.append("|---|---|---|---|---|---|")
        for fii_view in FII_SECTION_ORDER:
            subset = swing_whipsaw[swing_whipsaw["fii_view"] == fii_view]
            if len(subset) < 3:
                continue
            d = len(subset)
            p1 = (subset["swing_pattern"] == "Up Morning → Down Afternoon").sum()
            p2 = (subset["swing_pattern"] == "Down Morning → Up Afternoon").sum()
            p3 = (subset["swing_pattern"] == "Both Morning").sum()
            p4 = (subset["swing_pattern"] == "Both Afternoon").sum()
            lines.append(f"| {fii_view} | {d} | {p1} ({p1/d*100:.0f}%) | {p2} ({p2/d*100:.0f}%) | {p3} ({p3/d*100:.0f}%) | {p4} ({p4/d*100:.0f}%) |")

        sections.append("\n".join(lines))

    # === RANGE EXCEEDS VIX ANALYSIS ===
    lines = [
        "## Range vs VIX — Which Combos Exceed VIX Predictions?",
        "",
        "Range/VIX Ratio > 1.0 means the actual daily range exceeded the VIX-predicted range. Higher = more volatile than expected.",
        "",
        "### Top 10 Combos that EXCEED VIX (≥5 days)",
        "",
        "| Rank | FII View | PRO View | Days | Avg Range/VIX | Avg Range% | Avg VIX% | Whipsaw Ex% |",
        "|---|---|---|---|---|---|---|---|",
    ]
    exceed_vix = filtered.sort_values("avg_range_vs_vix", ascending=False).head(10)
    for rank, (_, r) in enumerate(exceed_vix.iterrows(), 1):
        lines.append(
            f"| {rank} | {r['fii_view']} | {r['pro_view']} | {r['days']:.0f} | "
            f"**{r['avg_range_vs_vix']:.2f}** | {r['avg_range_pct']:.3f}% | "
            f"{r['avg_vix_pct']:.3f}% | {r['whipsaw_extreme_pct']:.1f}% |"
        )

    lines.append("")
    lines.append("### Top 10 Combos UNDER VIX (≥5 days)")
    lines.append("")
    lines.append("| Rank | FII View | PRO View | Days | Avg Range/VIX | Avg Range% | Avg VIX% | Whipsaw Ex% |")
    lines.append("|---|---|---|---|---|---|---|---|")
    under_vix = filtered.sort_values("avg_range_vs_vix", ascending=True).head(10)
    for rank, (_, r) in enumerate(under_vix.iterrows(), 1):
        lines.append(
            f"| {rank} | {r['fii_view']} | {r['pro_view']} | {r['days']:.0f} | "
            f"**{r['avg_range_vs_vix']:.2f}** | {r['avg_range_pct']:.3f}% | "
            f"{r['avg_vix_pct']:.3f}% | {r['whipsaw_extreme_pct']:.1f}% |"
        )
    sections.append("\n".join(lines))

    # === CONCLUSION ===
    top3_whipsaw = sorted_by_whipsaw.head(3)
    bottom3_whipsaw = sorted_by_whipsaw.tail(3)
    top3_swing = filtered.sort_values("avg_total_swing", ascending=False).head(3)

    lines = [
        "## Conclusion",
        "",
        "### Key Findings:",
        "",
    ]

    finding = 1
    t = top3_whipsaw.iloc[0]
    lines.append(f"{finding}. **Most whipsaw-prone combination**: {t['fii_view']} FII + {t['pro_view']} PRO — "
                 f"**{t['whipsaw_extreme_pct']:.1f}%** of days are extreme whipsaws "
                 f"(both sides exceed half VIX), with {t['avg_total_swing']:.3f}% average total swing across {t['days']:.0f} days.")
    finding += 1

    b = bottom3_whipsaw.iloc[-1]
    lines.append(f"{finding}. **Calmest combination**: {b['fii_view']} FII + {b['pro_view']} PRO — "
                 f"only **{b['whipsaw_extreme_pct']:.1f}%** extreme whipsaw days, "
                 f"{b['avg_total_swing']:.3f}% avg swing across {b['days']:.0f} days.")
    finding += 1

    # Whipsaw vs Green% correlation
    corr = filtered[["whipsaw_extreme_pct", "green_pct"]].corr().iloc[0, 1]
    lines.append(f"{finding}. **Whipsaw vs Green% correlation**: r = {corr:.2f}. "
                 f"{'Volatile days tend to close green (reversal pattern).' if corr > 0.1 else 'Volatile days tend to close red.' if corr < -0.1 else 'No strong relationship between whipsaw intensity and close direction.'}")
    finding += 1

    # Range vs VIX insight
    high_exceed = filtered[filtered["avg_range_vs_vix"] > 1.0]
    lines.append(f"{finding}. **Range exceeds VIX**: {len(high_exceed)} out of {len(filtered)} combinations (≥5 days) have "
                 f"average range > VIX prediction. VIX tends to {'underestimate' if len(high_exceed) > len(filtered)/2 else 'overestimate'} "
                 f"actual volatility for most FII×PRO combos.")
    finding += 1

    if not swing_whipsaw.empty:
        dom_pattern = swing_whipsaw["swing_pattern"].value_counts().index[0]
        dom_pct = swing_whipsaw["swing_pattern"].value_counts().iloc[0] / len(swing_whipsaw) * 100
        lines.append(f"{finding}. **Dominant whipsaw pattern**: \"{dom_pattern}\" accounts for {dom_pct:.0f}% of extreme whipsaw days.")
        finding += 1

    lines.append("")
    lines.append("### Actionable Rules:")
    lines.append("")
    lines.append("- **Expect whipsaw**: " + ", ".join(
        f"{r['fii_view']}+{r['pro_view']} ({r['whipsaw_extreme_pct']:.0f}%)"
        for _, r in top3_whipsaw.iterrows()
    ))
    lines.append("- **Expect directional/calm**: " + ", ".join(
        f"{r['fii_view']}+{r['pro_view']} ({r['whipsaw_extreme_pct']:.0f}%)"
        for _, r in bottom3_whipsaw.iloc[::-1].head(3).iterrows()
    ))
    lines.append("- **Straddle/strangle candidates** (high whipsaw + high range/VIX): " + ", ".join(
        f"{r['fii_view']}+{r['pro_view']}"
        for _, r in filtered[(filtered["whipsaw_extreme_pct"] >= 15) & (filtered["avg_range_vs_vix"] >= 0.95)].sort_values("whipsaw_extreme_pct", ascending=False).head(5).iterrows()
    ))
    iron_condor = filtered[(filtered["whipsaw_extreme_pct"] <= 8) & (filtered["avg_range_vs_vix"] <= 1.15)].sort_values("avg_range_vs_vix").head(5)
    if not iron_condor.empty:
        lines.append("- **Iron condor / range-bound candidates** (low whipsaw + low range/VIX): " + ", ".join(
            f"{r['fii_view']}+{r['pro_view']}"
            for _, r in iron_condor.iterrows()
        ))
    else:
        lines.append("- **Iron condor / range-bound candidates**: Most combos exceed VIX prediction; look for Mildly Bullish+Mildly Bullish (lowest whipsaw+range/VIX ratio)")

    sections.append("\n".join(lines))

    # === WRITE ===
    report = "\n\n---\n\n".join(sections) + "\n"
    with open(output_path, "w") as f:
        f.write(report)
    print(f"Generated: {output_path} ({frac_label} threshold, no neutral)")
    print(f"  {total_days} days, {len(stats)} combinations, {extreme_days} extreme whipsaw days")


def main():
    intra_df = load_intraday()

    # 0.5×VIX (Half-VIX) report
    df_half = load_and_prepare(vix_fraction=0.5)
    generate_report(df_half, intra_df, vix_fraction=0.5,
                    output_path=str(SCRIPT_DIR / "FII_PRO_NO_NEUTRAL_VOLATILITY_WHIPSAW_ANALYSIS.md"))

    # 0.3×VIX report
    df_03 = load_and_prepare(vix_fraction=0.3)
    generate_report(df_03, intra_df, vix_fraction=0.3,
                    output_path=str(SCRIPT_DIR / "FII_PRO_NO_NEUTRAL_VOLATILITY_WHIPSAW_0.3VIX_ANALYSIS.md"))

    print("Done! Both volatility reports generated in reports_no_neutral/ directory.")


if __name__ == "__main__":
    main()
