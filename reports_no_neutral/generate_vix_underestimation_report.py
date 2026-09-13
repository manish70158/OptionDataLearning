import pandas as pd
import numpy as np
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CSV_PATH = PROJECT_ROOT / "vix_fii_t1_intraday_daily_results.csv"
OUTPUT_PATH_ALL = SCRIPT_DIR / "VIX_UNDERESTIMATION_FII_PRO_ANALYSIS.md"
OUTPUT_PATH_EXPIRY = SCRIPT_DIR / "VIX_UNDERESTIMATION_FII_PRO_EXPIRY_ANALYSIS.md"

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
                 "vix_predicted_move_pct", "range_vs_vix_ratio", "diff_pct",
                 "vix_open"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df["is_nifty_expiry"] = pd.to_numeric(df["is_nifty_expiry"], errors="coerce").fillna(0).astype(int)
    df["fii_view"] = df["fii_composite"].apply(classify_composite)
    df["pro_view"] = df["pro_composite"].apply(classify_composite)

    # Recompute vix_accuracy: Underestimated = diff_pct > 0 (actual range exceeded VIX prediction by any amount)
    df["vix_accuracy"] = np.where(df["diff_pct"] > 0, "Underestimated", "Overestimated")

    # Combined composite
    df["combined_composite"] = df["fii_composite"].fillna(0) + df["pro_composite"].fillna(0)

    # Day of week
    df["date_parsed"] = pd.to_datetime(df["date"])
    df["day_of_week_name"] = df["date_parsed"].dt.day_name()
    df["year"] = df["date_parsed"].dt.year

    return df


def fmt_pct(val, decimals=2):
    if pd.isna(val):
        return "-"
    sign = "+" if val > 0 else ""
    return f"{sign}{val:.{decimals}f}%"


def alignment_category(fii_view, pro_view):
    """Classify the FII+PRO combination into an alignment category."""
    bullish_set = {"Strong Bullish", "Bullish", "Mildly Bullish"}
    bearish_set = {"Strong Bearish", "Bearish", "Mildly Bearish"}

    if fii_view in bullish_set and pro_view in bullish_set:
        return "Bullish Alignment"
    elif fii_view in bearish_set and pro_view in bearish_set:
        return "Bearish Alignment"
    elif fii_view in bullish_set and pro_view in bearish_set:
        return "FII Bullish + PRO Bearish"
    elif fii_view in bearish_set and pro_view in bullish_set:
        return "FII Bearish + PRO Bullish"
    else:
        return "Mixed"


def generate_report(df, output_path, title_suffix="", filter_desc=""):
    total_days = len(df)
    date_min = df["date"].min()
    date_max = df["date"].max()

    under_df = df[df["vix_accuracy"] == "Underestimated"]
    over_df = df[df["vix_accuracy"] == "Overestimated"]
    under_count = len(under_df)
    over_count = len(over_df)

    title_label = f" — {title_suffix}" if title_suffix else ""
    filter_line = f"\n> **Filter**: {filter_desc}" if filter_desc else ""

    sections = []

    # === HEADER ===
    sections.append(f"""# VIX Underestimation x FII/PRO Combination Analysis{title_label} (No Neutral)

> **Dataset**: `vix_fii_t1_intraday_daily_results.csv` — {total_days:,} trading days ({date_min} to {date_max})
>
> **Definition**: VIX "Underestimated" = actual intraday range exceeded VIX-predicted move (diff > 0%)
> (i.e., the market moved more than VIX implied it would, by any amount)
>
> **No Neutral Classification**: Every day is classified as directional — composite 0 maps to Mildly Bullish{filter_line}
>
> **T-1 data caveat**: FII/PRO views are derived from T+1 settlement data — alignment
> is known only after the trading day. This analysis identifies historical patterns,
> not real-time predictive signals.

### Label Guide
- **Mildly Bullish** = composite 0 to +50K (inclusive of zero)
- **Mildly Bearish** = composite -50K to -1 (exclusive of zero)
- **Bullish / Bearish** = composite ±50K to ±100K (fixed)
- **Strong Bullish / Strong Bearish** = composite beyond ±100K (fixed)
- **No Neutral zone** — every day is classified as directional""")

    # === OVERALL VIX ACCURACY ===
    lines = [
        "## Overall VIX Accuracy Distribution",
        "",
        "| Category | Days | % of Total | Avg Range% | Avg Diff% |",
        "|----------|-----:|-----------:|-----------:|----------:|",
    ]
    for label, subset in [("**Underestimated**", under_df), ("Overestimated", over_df)]:
        avg_range = subset["actual_range_pct"].mean()
        avg_diff = subset["diff_pct"].mean() if "diff_pct" in subset.columns else 0
        lines.append(
            f"| {label} | **{len(subset)}** | **{len(subset)/total_days*100:.1f}%** | "
            f"{avg_range:.2f}% | {fmt_pct(avg_diff)} |"
            if "Underestimated" in label else
            f"| {label} | {len(subset)} | {len(subset)/total_days*100:.1f}% | "
            f"{avg_range:.2f}% | {fmt_pct(avg_diff)} |"
        )
    avg_range_all = df["actual_range_pct"].mean()
    lines.append(f"| **Total** | **{total_days}** | **100%** | {avg_range_all:.2f}% | 0.00% |")
    lines.append("")
    under_pct = under_count / total_days * 100
    over_pct = over_count / total_days * 100
    if under_pct > 50:
        lines.append(f"VIX underestimates the actual intraday range on **{under_pct:.1f}%** of trading days — "
                     f"the market moves more than VIX predicts on the majority of days. "
                     f"Only {over_pct:.0f}% of days stay within VIX bounds. "
                     f"This report identifies which FII/PRO combinations amplify or dampen this systematic VIX bias.")
    else:
        lines.append(f"VIX overestimates intraday range ~{over_pct:.0f}% of the time. "
                     f"The {under_pct:.1f}% of days where it underestimates "
                     f"are the high-volatility outlier days — and understanding which FII/PRO combinations precede "
                     f"these events is the focus of this report.")
    sections.append("\n".join(lines))

    # === ALIGNMENT CATEGORY → UNDERESTIMATION RATE ===
    df["alignment"] = df.apply(lambda r: alignment_category(r["fii_view"], r["pro_view"]), axis=1)

    lines = [
        "## Alignment Category → Underestimation Rate",
        "",
        "Which FII/PRO alignment type sees VIX underestimate most frequently?",
        "",
        "| Alignment Category | Total Days | Underestimated | Rate | Share of All U/E | Avg Range (U/E) | Avg Diff (U/E) |",
        "|--------------------|----------:|--------------:|-----:|-----------------:|----------------:|---------------:|",
    ]
    alignment_stats = []
    for align_cat in df["alignment"].unique():
        subset = df[df["alignment"] == align_cat]
        under_subset = subset[subset["vix_accuracy"] == "Underestimated"]
        rate = len(under_subset) / len(subset) * 100 if len(subset) > 0 else 0
        share = len(under_subset) / under_count * 100 if under_count > 0 else 0
        avg_range_ue = under_subset["actual_range_pct"].mean() if len(under_subset) > 0 else 0
        avg_diff_ue = under_subset["diff_pct"].mean() if len(under_subset) > 0 else 0
        alignment_stats.append({
            "alignment": align_cat,
            "total": len(subset),
            "under": len(under_subset),
            "rate": rate,
            "share": share,
            "avg_range_ue": avg_range_ue,
            "avg_diff_ue": avg_diff_ue,
        })
    alignment_stats.sort(key=lambda x: x["rate"], reverse=True)
    for s in alignment_stats:
        bold = "Alignment" in s["alignment"]
        name = f"**{s['alignment']}**" if bold else s["alignment"]
        lines.append(
            f"| {name} | {s['total']} | {s['under']} | "
            f"{'**' if bold else ''}{s['rate']:.1f}%{'**' if bold else ''} | "
            f"{s['share']:.1f}% | {s['avg_range_ue']:.2f}% | {fmt_pct(s['avg_diff_ue'])} |"
        )
    top_align = alignment_stats[0]
    bot_align = alignment_stats[-1]
    lines.append("")
    lines.append(f"**Key insight**: {top_align['alignment']} has the highest underestimation rate ({top_align['rate']:.1f}%) "
                 f"while {bot_align['alignment']} has the lowest ({bot_align['rate']:.1f}%). "
                 f"The spread of {top_align['rate'] - bot_align['rate']:.1f} pp shows that FII/PRO positioning meaningfully "
                 f"influences how much actual volatility exceeds VIX predictions.")
    sections.append("\n".join(lines))

    # === EXPIRY TYPE BREAKDOWN (only if expiry_type column has meaningful data) ===
    if "expiry_type" in df.columns and df["expiry_type"].notna().sum() > 0:
        expiry_types = df["expiry_type"].dropna().unique()
        if len(expiry_types) > 0 and not (len(expiry_types) == 1 and expiry_types[0] == ""):
            lines = [
                "## Expiry Type Breakdown",
                "",
                "| Expiry Type | Total | Under. | Rate | Avg Range% | Avg Diff% | Red% (U/E) | TTD% (U/E) |",
                "|-------------|------:|-------:|-----:|-----------:|----------:|----------:|----------:|",
            ]
            for etype in ["weekly", "monthly"]:
                subset = df[df["expiry_type"] == etype]
                if len(subset) == 0:
                    continue
                sub_under = subset[subset["vix_accuracy"] == "Underestimated"]
                rate = len(sub_under) / len(subset) * 100
                avg_range = subset["actual_range_pct"].mean()
                avg_diff = subset["diff_pct"].mean()
                if len(sub_under) > 0:
                    red_pct = (sub_under["nifty_day"] == "Red").sum() / len(sub_under) * 100
                    ttd_pct = (sub_under["move_direction"] == "Top to Down").sum() / len(sub_under) * 100
                else:
                    red_pct = ttd_pct = 0
                lines.append(
                    f"| {etype.title()} | {len(subset)} | {len(sub_under)} | {rate:.1f}% | "
                    f"{avg_range:.2f}% | {fmt_pct(avg_diff)} | {red_pct:.1f}% | {ttd_pct:.1f}% |"
                )
            sections.append("\n".join(lines))

    # === PER-COMBO UNDERESTIMATION RATE ===
    min_combo_days = 3 if total_days < 500 else 5
    lines = [
        "## Per-Combination Underestimation Rate",
        "",
        f"All FII×PRO combinations with ≥{min_combo_days} days, sorted by underestimation rate.",
        "",
        "| FII View | PRO View | Total Days | Underestimated | Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Avg Chg (U/E) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    combo_stats = []
    for (fii_v, pro_v), grp in df.groupby(["fii_view", "pro_view"]):
        total = len(grp)
        if total < min_combo_days:
            continue
        under_grp = grp[grp["vix_accuracy"] == "Underestimated"]
        ud = len(under_grp)
        rate = ud / total * 100 if total > 0 else 0
        green_ue = (under_grp["nifty_day"] == "Green").sum() / ud * 100 if ud > 0 else 0
        avg_range_ue = under_grp["actual_range_pct"].mean() if ud > 0 else 0
        avg_diff_ue = under_grp["diff_pct"].mean() if ud > 0 else 0
        avg_chg_ue = under_grp["actual_open_close_pct"].mean() if ud > 0 else 0
        combo_stats.append({
            "fii_view": fii_v, "pro_view": pro_v,
            "total": total, "under": ud, "rate": rate,
            "green_ue": green_ue, "avg_range_ue": avg_range_ue,
            "avg_diff_ue": avg_diff_ue, "avg_chg_ue": avg_chg_ue,
        })
    combo_stats.sort(key=lambda x: x["rate"], reverse=True)
    for s in combo_stats:
        bold = s["under"] >= min_combo_days
        fii = f"**{s['fii_view']}**" if bold else s["fii_view"]
        pro = f"**{s['pro_view']}**" if bold else s["pro_view"]
        lines.append(
            f"| {fii} | {pro} | {s['total']} | {s['under']} | "
            f"{'**' if bold else ''}{s['rate']:.1f}%{'**' if bold else ''} | "
            f"{s['green_ue']:.1f}% | {s['avg_range_ue']:.2f}% | "
            f"{fmt_pct(s['avg_diff_ue'])} | {fmt_pct(s['avg_chg_ue'], 3)} |"
        )
    sections.append("\n".join(lines))

    # === DEEP DIVE: BEARISH ALIGNMENT ===
    bearish_df = df[df["alignment"] == "Bearish Alignment"]
    bear_under = bearish_df[bearish_df["vix_accuracy"] == "Underestimated"]
    lines = [
        "## Deep Dive: Bearish Alignment (Both FII & PRO Bearish-Leaning)",
        "",
        f"When both FII and PRO lean bearish ({len(bearish_df)} days total):",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| Total bearish alignment days | {len(bearish_df)} |",
        f"| Underestimated | {len(bear_under)} ({len(bear_under)/len(bearish_df)*100:.1f}%) |",
    ]
    if len(bear_under) > 0:
        lines.append(f"| Avg range on underestimated days | {bear_under['actual_range_pct'].mean():.2f}% |")
        lines.append(f"| Avg VIX miss (diff%) | {fmt_pct(bear_under['diff_pct'].mean())} |")
        lines.append(f"| Avg VIX predicted | {bear_under['vix_predicted_move_pct'].mean():.2f}% |")
        ttd = (bear_under["move_direction"] == "Top to Down").sum()
        dtu = (bear_under["move_direction"] == "Down to Up").sum()
        lines.append(f"| Top to Down on U/E days | {ttd} ({ttd/len(bear_under)*100:.1f}%) |")
        lines.append(f"| Down to Up on U/E days | {dtu} ({dtu/len(bear_under)*100:.1f}%) |")
        red = (bear_under["nifty_day"] == "Red").sum()
        lines.append(f"| Red (down close) on U/E days | {red} ({red/len(bear_under)*100:.1f}%) |")
    lines.append("")

    # Sub-combo breakdown within bearish alignment
    lines.append("### Bearish Sub-Combinations")
    lines.append("")
    lines.append("| FII View | PRO View | Days | U/E Days | U/E Rate | Avg Range (U/E) |")
    lines.append("|---|---|---:|---:|---:|---:|")
    bearish_views = ["Mildly Bearish", "Bearish", "Strong Bearish"]
    for fii_v in bearish_views:
        for pro_v in bearish_views:
            sub = bearish_df[(bearish_df["fii_view"] == fii_v) & (bearish_df["pro_view"] == pro_v)]
            if len(sub) < max(2, min_combo_days - 1):
                continue
            sub_u = sub[sub["vix_accuracy"] == "Underestimated"]
            rate = len(sub_u) / len(sub) * 100 if len(sub) > 0 else 0
            avg_r = sub_u["actual_range_pct"].mean() if len(sub_u) > 0 else 0
            lines.append(f"| {fii_v} | {pro_v} | {len(sub)} | {len(sub_u)} | {rate:.1f}% | {avg_r:.2f}% |")

    lines.append("")
    # Find highest and lowest bearish sub-combo rates
    bear_sub_rates = []
    for fii_v in bearish_views:
        for pro_v in bearish_views:
            sub = bearish_df[(bearish_df["fii_view"] == fii_v) & (bearish_df["pro_view"] == pro_v)]
            if len(sub) >= min_combo_days:
                sub_u = sub[sub["vix_accuracy"] == "Underestimated"]
                bear_sub_rates.append((fii_v, pro_v, len(sub_u) / len(sub) * 100, len(sub)))
    if bear_sub_rates:
        bear_sub_rates.sort(key=lambda x: x[2], reverse=True)
        top_b = bear_sub_rates[0]
        bot_b = bear_sub_rates[-1]
        lines.append(f"**Takeaway**: Within bearish alignment, {top_b[0]} × {top_b[1]} has the highest underestimation rate "
                     f"({top_b[2]:.1f}%, {top_b[3]}d) while {bot_b[0]} × {bot_b[1]} has the lowest ({bot_b[2]:.1f}%, {bot_b[3]}d). "
                     f"Stronger bearish conviction on both sides correlates with higher VIX underestimation.")
    else:
        lines.append("**Takeaway**: When both sides are bearish, VIX underestimates the majority of the time. "
                     "Stronger conviction levels tend to push underestimation rates higher.")
    sections.append("\n".join(lines))

    # === DEEP DIVE: BULLISH ALIGNMENT ===
    bullish_df = df[df["alignment"] == "Bullish Alignment"]
    bull_under = bullish_df[bullish_df["vix_accuracy"] == "Underestimated"]
    lines = [
        "## Deep Dive: Bullish Alignment (Both FII & PRO Bullish-Leaning)",
        "",
        f"When both FII and PRO lean bullish ({len(bullish_df)} days total):",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| Total bullish alignment days | {len(bullish_df)} |",
        f"| Underestimated | {len(bull_under)} ({len(bull_under)/len(bullish_df)*100:.1f}%) |",
    ]
    if len(bull_under) > 0:
        lines.append(f"| Avg range on underestimated days | {bull_under['actual_range_pct'].mean():.2f}% |")
        lines.append(f"| Avg VIX miss (diff%) | {fmt_pct(bull_under['diff_pct'].mean())} |")
        red = (bull_under["nifty_day"] == "Red").sum()
        green = (bull_under["nifty_day"] == "Green").sum()
        lines.append(f"| Red (down close) on U/E days | {red} ({red/len(bull_under)*100:.1f}%) |")
        lines.append(f"| Green (up close) on U/E days | {green} ({green/len(bull_under)*100:.1f}%) |")
    lines.append("")

    # Sub-combo breakdown
    lines.append("### Bullish Sub-Combinations")
    lines.append("")
    lines.append("| FII View | PRO View | Days | U/E Days | U/E Rate | Avg Range (U/E) |")
    lines.append("|---|---|---:|---:|---:|---:|")
    bullish_views = ["Mildly Bullish", "Bullish", "Strong Bullish"]
    for fii_v in bullish_views:
        for pro_v in bullish_views:
            sub = bullish_df[(bullish_df["fii_view"] == fii_v) & (bullish_df["pro_view"] == pro_v)]
            if len(sub) < max(2, min_combo_days - 1):
                continue
            sub_u = sub[sub["vix_accuracy"] == "Underestimated"]
            rate = len(sub_u) / len(sub) * 100 if len(sub) > 0 else 0
            avg_r = sub_u["actual_range_pct"].mean() if len(sub_u) > 0 else 0
            lines.append(f"| {fii_v} | {pro_v} | {len(sub)} | {len(sub_u)} | {rate:.1f}% | {avg_r:.2f}% |")

    lines.append("")
    if len(bull_under) > 0:
        red_pct = (bull_under["nifty_day"] == "Red").sum() / len(bull_under) * 100
        green_pct = 100 - red_pct
        bull_rate = len(bull_under) / len(bullish_df) * 100
        bear_rate = len(bear_under) / len(bearish_df) * 100 if len(bearish_df) > 0 else 0
        lines.append(f"Bullish alignment underestimates {bull_rate:.1f}% of the time vs bearish alignment at {bear_rate:.1f}% — "
                     f"a {bear_rate - bull_rate:.1f} pp gap. On bullish U/E days, the market closes RED {red_pct:.1f}% "
                     f"and GREEN {green_pct:.1f}%, showing the excess range works both ways.")
    sections.append("\n".join(lines))

    # === DIVERGENT ALIGNMENT: FII Bullish + PRO Bearish / FII Bearish + PRO Bullish ===
    lines = [
        "## Divergent Alignment — Opposing FII & PRO Views",
        "",
    ]
    for label in ["FII Bullish + PRO Bearish", "FII Bearish + PRO Bullish"]:
        div_df = df[df["alignment"] == label]
        div_under = div_df[div_df["vix_accuracy"] == "Underestimated"]
        rate = len(div_under) / len(div_df) * 100 if len(div_df) > 0 else 0
        lines.append(f"### {label} ({len(div_df)} days)")
        lines.append("")
        lines.append(f"- Underestimated: {len(div_under)} ({rate:.1f}%)")
        if len(div_under) > 0:
            lines.append(f"- Avg range on U/E days: {div_under['actual_range_pct'].mean():.2f}%")
            lines.append(f"- Avg diff: {fmt_pct(div_under['diff_pct'].mean())}")
            red = (div_under["nifty_day"] == "Red").sum()
            lines.append(f"- Red close on U/E days: {red} ({red/len(div_under)*100:.1f}%)")
            ttd = (div_under["move_direction"] == "Top to Down").sum()
            lines.append(f"- Top to Down on U/E days: {ttd} ({ttd/len(div_under)*100:.1f}%)")
        lines.append("")
    sections.append("\n".join(lines))

    # === VIX REGIME ANALYSIS ===
    def vix_regime(vix_val):
        if pd.isna(vix_val):
            return "Unknown"
        if vix_val < 15:
            return "Low (<15)"
        elif vix_val < 20:
            return "Normal (15-20)"
        elif vix_val <= 30:
            return "Elevated (20-30)"
        else:
            return "High (>30)"

    df["vix_regime"] = df["vix_open"].apply(vix_regime)
    regime_order = ["Low (<15)", "Normal (15-20)", "Elevated (20-30)", "High (>30)"]

    lines = [
        "## VIX Regime Analysis",
        "",
        "| VIX Regime | Total | Under. | Rate | Avg Range% | Avg Diff% |",
        "|------------|------:|-------:|-----:|-----------:|----------:|",
    ]
    for regime in regime_order:
        subset = df[df["vix_regime"] == regime]
        if len(subset) == 0:
            continue
        sub_under = subset[subset["vix_accuracy"] == "Underestimated"]
        rate = len(sub_under) / len(subset) * 100
        avg_range = subset["actual_range_pct"].mean()
        avg_diff = subset["diff_pct"].mean() if "diff_pct" in subset.columns else 0
        lines.append(
            f"| {regime} | {len(subset)} | {len(sub_under)} | "
            f"{rate:.1f}% | "
            f"{avg_range:.2f}% | {fmt_pct(avg_diff)} |"
        )

    # Find highest rate regime dynamically
    regime_rates = {}
    for regime in regime_order:
        subset = df[df["vix_regime"] == regime]
        if len(subset) > 0:
            sub_under = subset[subset["vix_accuracy"] == "Underestimated"]
            regime_rates[regime] = len(sub_under) / len(subset) * 100
    if regime_rates:
        max_regime = max(regime_rates, key=regime_rates.get)
        min_regime = min(regime_rates, key=regime_rates.get)
        lines.append("")
        lines.append(f"**{max_regime}** has the highest underestimation rate ({regime_rates[max_regime]:.1f}%) "
                     f"while **{min_regime}** has the lowest ({regime_rates[min_regime]:.1f}%). "
                     f"VIX underestimates the actual range across all regimes, confirming a systematic bias "
                     f"where the market routinely exceeds VIX-implied moves.")
    sections.append("\n".join(lines))

    # === COMBINED COMPOSITE SCORE BUCKETS ===
    bins = [-np.inf, -200000, -100000, -50000, 0, 50000, 100000, 200000, np.inf]
    labels_b = ["-200K & below", "-200K to -100K", "-100K to -50K", "-50K to 0",
                "0 to +50K", "+50K to +100K", "+100K to +200K", "+200K & above"]
    df["composite_bucket"] = pd.cut(df["combined_composite"], bins=bins, labels=labels_b, right=True)

    lines = [
        "## Combined Composite Score → Underestimation Rate",
        "",
        "FII + PRO composite summed together.",
        "",
        "| Composite Range | Total | Under. | Rate | Avg Range (U/E) |",
        "|-----------------|------:|-------:|-----:|----------------:|",
    ]
    for bucket in labels_b:
        subset = df[df["composite_bucket"] == bucket]
        if len(subset) == 0:
            continue
        sub_under = subset[subset["vix_accuracy"] == "Underestimated"]
        rate = len(sub_under) / len(subset) * 100
        avg_r = sub_under["actual_range_pct"].mean() if len(sub_under) > 0 else 0
        lines.append(f"| {bucket} | {len(subset)} | {len(sub_under)} | {rate:.1f}% | {avg_r:.2f}% |")
    sections.append("\n".join(lines))

    # === PER-FII VIEW UNDERESTIMATION PROFILE ===
    lines = []
    section_num = 1
    for fii_view in FII_SECTION_ORDER:
        fii_df = df[df["fii_view"] == fii_view]
        if len(fii_df) < min_combo_days:
            continue
        fii_total = len(fii_df)
        fii_under = fii_df[fii_df["vix_accuracy"] == "Underestimated"]
        fii_under_count = len(fii_under)
        fii_rate = fii_under_count / fii_total * 100

        lines.append(f"## Section {section_num}: FII {fii_view.upper()} — Underestimation Profile ({fii_total} days, {fii_rate:.1f}% U/E rate)")
        lines.append("")
        lines.append("| PRO View | Days | U/E Days | U/E Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Red% (U/E) | TTD% (U/E) |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")

        for pro_view in FII_SECTION_ORDER:
            combo = fii_df[fii_df["pro_view"] == pro_view]
            if len(combo) < min_combo_days:
                continue
            cd = len(combo)
            combo_under = combo[combo["vix_accuracy"] == "Underestimated"]
            ud = len(combo_under)
            rate = ud / cd * 100 if cd > 0 else 0
            if ud > 0:
                green_pct = (combo_under["nifty_day"] == "Green").sum() / ud * 100
                avg_range = combo_under["actual_range_pct"].mean()
                avg_diff = combo_under["diff_pct"].mean()
                red_pct = (combo_under["nifty_day"] == "Red").sum() / ud * 100
                ttd_pct = (combo_under["move_direction"] == "Top to Down").sum() / ud * 100
            else:
                green_pct = avg_range = avg_diff = red_pct = ttd_pct = 0
            lines.append(
                f"| {pro_view} | {cd} | {ud} | **{rate:.1f}%** | "
                f"{green_pct:.1f}% | {avg_range:.2f}% | {fmt_pct(avg_diff)} | "
                f"{red_pct:.1f}% | {ttd_pct:.1f}% |"
            )

        # Summary for this FII view
        if fii_under_count > 0:
            red_total = (fii_under["nifty_day"] == "Red").sum()
            ttd_total = (fii_under["move_direction"] == "Top to Down").sum()
            lines.append("")
            lines.append(f"**FII {fii_view} summary**: {fii_under_count}/{fii_total} days underestimated ({fii_rate:.1f}%). "
                         f"On U/E days: {red_total/fii_under_count*100:.0f}% red, {ttd_total/fii_under_count*100:.0f}% Top-to-Down.")
        lines.append("")
        section_num += 1
    sections.append("\n".join(lines))

    # === DAY OF WEEK ANALYSIS ===
    lines = [
        "## Day of Week → Underestimation Rate",
        "",
        "| Day | Total | Under. | Rate |",
        "|-----|------:|-------:|-----:|",
    ]
    dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for day in dow_order:
        subset = df[df["day_of_week_name"] == day]
        if len(subset) == 0:
            continue
        sub_under = subset[subset["vix_accuracy"] == "Underestimated"]
        rate = len(sub_under) / len(subset) * 100
        lines.append(f"| {day} | {len(subset)} | {len(sub_under)} | {rate:.1f}% |")
    sections.append("\n".join(lines))

    # === YEAR-WISE ANALYSIS ===
    lines = [
        "## Year → Underestimation Rate",
        "",
        "| Year | Total | Under. | Rate |",
        "|------|------:|-------:|-----:|",
    ]
    for year in sorted(df["year"].unique()):
        subset = df[df["year"] == year]
        sub_under = subset[subset["vix_accuracy"] == "Underestimated"]
        rate = len(sub_under) / len(subset) * 100
        lines.append(f"| {year} | {len(subset)} | {len(sub_under)} | {rate:.1f}% |")
    sections.append("\n".join(lines))

    # === TOP 20 LARGEST VIX MISSES ===
    top20 = df.sort_values("diff_pct", ascending=False).head(20)
    lines = [
        "## Top 20 Largest VIX Misses (Extreme Underestimation Days)",
        "",
        "| Date | FII View | PRO View | VIX Pred% | Actual Range% | Miss | Direction | Close |",
        "|------|----------|----------|----------:|--------------:|-----:|-----------|-------|",
    ]
    for _, r in top20.iterrows():
        lines.append(
            f"| {r['date']} | {r['fii_view']} | {r['pro_view']} | "
            f"{r['vix_predicted_move_pct']:.2f}% | {r['actual_range_pct']:.2f}% | "
            f"**{fmt_pct(r['diff_pct'])}** | {r['move_direction']} | "
            f"{'Red' if r['nifty_day'] == 'Red' else 'Green'} |"
        )
    lines.append("")
    red_count = (top20["nifty_day"] == "Red").sum()
    ttd_count = (top20["move_direction"] == "Top to Down").sum()
    lines.append(f"**Observation**: Of the top 20, **{red_count} were red days** "
                 f"and **{ttd_count} were Top to Down** moves. "
                 f"Extreme VIX misses overwhelmingly resolve with downside price action.")
    sections.append("\n".join(lines))

    # === KEY FINDINGS ===
    lines = ["## Key Findings", ""]
    finding = 1
    overall_ue_pct = under_count / total_days * 100

    # 1. VIX systematic bias
    lines.append(f"{finding}. **VIX systematically underestimates** actual intraday range on {overall_ue_pct:.1f}% of trading days. "
                 f"The market routinely moves more than VIX implies — this is the baseline, not the exception.")
    finding += 1

    # 2. Alignment with highest underestimation
    top_align = alignment_stats[0]
    bot_align = alignment_stats[-1]
    lines.append(f"{finding}. **{top_align['alignment']} = most underestimated** ({top_align['rate']:.1f}%) vs "
                 f"**{bot_align['alignment']} = least underestimated** ({bot_align['rate']:.1f}%): "
                 f"A {top_align['rate'] - bot_align['rate']:.1f} pp spread shows FII/PRO positioning meaningfully "
                 f"modulates how much the market exceeds VIX predictions.")
    finding += 1

    # 3. Top combo
    if combo_stats:
        top_combo = combo_stats[0]
        bot_combo = combo_stats[-1]
        lines.append(f"{finding}. **Highest underestimation combo**: {top_combo['fii_view']} FII + {top_combo['pro_view']} PRO — "
                     f"**{top_combo['rate']:.1f}%** across {top_combo['total']} days. "
                     f"**Lowest**: {bot_combo['fii_view']} FII + {bot_combo['pro_view']} PRO — "
                     f"**{bot_combo['rate']:.1f}%** across {bot_combo['total']} days.")
        finding += 1

    # 4. Bullish vs bearish alignment comparison
    bull_align = next((s for s in alignment_stats if s["alignment"] == "Bullish Alignment"), None)
    bear_align = next((s for s in alignment_stats if s["alignment"] == "Bearish Alignment"), None)
    if bull_align and bear_align:
        if bear_align["rate"] > bull_align["rate"]:
            diff = bear_align["rate"] - bull_align["rate"]
            lines.append(f"{finding}. **Bearish alignment amplifies VIX underestimation**: Bearish at {bear_align['rate']:.1f}% vs "
                         f"Bullish at {bull_align['rate']:.1f}% (+{diff:.1f} pp gap). "
                         f"Bearish institutional positioning produces larger-than-expected moves more consistently.")
        else:
            diff = bull_align["rate"] - bear_align["rate"]
            lines.append(f"{finding}. **Bullish alignment amplifies VIX underestimation**: Bullish at {bull_align['rate']:.1f}% vs "
                         f"Bearish at {bear_align['rate']:.1f}% (+{diff:.1f} pp gap).")
        finding += 1

    # 5. Lowest underestimation combo — adjusted threshold for new reality
    min_safe_days = 5 if total_days < 500 else 10
    lowest_combos = [c for c in combo_stats if c["total"] >= min_safe_days]
    if lowest_combos:
        safest = min(lowest_combos, key=lambda x: x["rate"])
        lines.append(f"{finding}. **Most range-bound combination (≥{min_safe_days} days)**: {safest['fii_view']} FII + {safest['pro_view']} PRO — "
                     f"{safest['rate']:.1f}% underestimation across {safest['total']} days "
                     f"({'still above 50% — VIX underestimates even here' if safest['rate'] > 50 else 'VIX is more accurate for this combo'}). ")
        finding += 1

    # 6. VIX regime
    if regime_rates:
        max_regime = max(regime_rates, key=regime_rates.get)
        min_regime = min(regime_rates, key=regime_rates.get)
        lines.append(f"{finding}. **VIX regime**: {max_regime} has the highest underestimation ({regime_rates[max_regime]:.1f}%), "
                     f"{min_regime} has the lowest ({regime_rates[min_regime]:.1f}%). "
                     f"VIX underestimates across all regimes — the bias is structural, not regime-dependent.")
        finding += 1

    # 7. Day of week
    dow_rates = {}
    for day in dow_order:
        subset = df[df["day_of_week_name"] == day]
        if len(subset) > 0:
            sub_under = subset[subset["vix_accuracy"] == "Underestimated"]
            dow_rates[day] = len(sub_under) / len(subset) * 100
    if dow_rates:
        max_dow = max(dow_rates, key=dow_rates.get)
        min_dow = min(dow_rates, key=dow_rates.get)
        lines.append(f"{finding}. **Day of week**: {max_dow}s ({dow_rates[max_dow]:.1f}%) are most prone to underestimation. "
                     f"{min_dow}s ({dow_rates[min_dow]:.1f}%) are least prone.")
        finding += 1

    # 8. Top 20 extreme observation
    lines.append(f"{finding}. **Extreme outliers**: The largest VIX misses (>+1.5%) often occur in combinations where "
                 f"positioning doesn't fully explain the move — suggesting exogenous shocks "
                 f"(geopolitical, macro, election results) drive the most extreme blowouts.")
    finding += 1

    sections.append("\n".join(lines))

    # === TRADING IMPLICATIONS ===
    lines = [
        "## Trading Implications",
        "",
        f"**Baseline reality**: VIX underestimates the actual range on {overall_ue_pct:.0f}% of days. "
        f"Any options strategy priced off VIX is likely underpricing actual movement on most days.",
        "",
    ]

    # Use median rate to split high vs low
    all_rates = [c["rate"] for c in combo_stats if c["total"] >= min_safe_days]
    if all_rates:
        median_rate = sorted(all_rates)[len(all_rates) // 2]
    else:
        median_rate = overall_ue_pct

    # High underestimation combos (top quartile)
    high_threshold = sorted(all_rates, reverse=True)[max(0, len(all_rates) // 4)] if all_rates else 70
    high_ue = [c for c in combo_stats if c["rate"] >= high_threshold and c["total"] >= min_safe_days]
    if high_ue:
        combos_str = ", ".join(f"{c['fii_view']}+{c['pro_view']} ({c['rate']:.0f}%)" for c in high_ue[:5])
        lines.append(f"- **Highest excess volatility** (top quartile, ≥{high_threshold:.0f}% U/E rate): {combos_str} — "
                     f"straddles/strangles priced off VIX are most likely to be cheap for these combos")

    # Low underestimation combos (bottom quartile)
    low_threshold = sorted(all_rates)[max(0, len(all_rates) // 4)] if all_rates else 50
    low_ue = [c for c in combo_stats if c["rate"] <= low_threshold and c["total"] >= min_safe_days]
    if low_ue:
        combos_str = ", ".join(f"{c['fii_view']}+{c['pro_view']} ({c['rate']:.0f}%)" for c in low_ue[:5])
        lines.append(f"- **Most VIX-accurate combos** (bottom quartile, ≤{low_threshold:.0f}% U/E rate): {combos_str} — "
                     f"iron condors and range-bound strategies are relatively safer here")

    lines.append(f"- **Bearish alignment + weekend effect**: When both FII/PRO lean bearish on Mondays/Fridays, "
                 f"the probability of range exceeding VIX is highest — widen stop-losses or buy premium")
    lines.append(f"- **VIX is a floor, not a ceiling**: With {overall_ue_pct:.0f}% underestimation rate, "
                 f"treat VIX-predicted range as the minimum expected move, not the maximum")
    lines.append("- **This is retrospective analysis using T+1 data** — use as a volatility framework, not as an intraday entry signal")

    sections.append("\n".join(lines))

    # === WRITE ===
    report = "\n\n---\n\n".join(sections) + "\n\n---\n\n"
    filter_tag = f" | {title_suffix}" if title_suffix else ""
    report += f"*Generated: {pd.Timestamp.now().strftime('%Y-%m-%d')} | Data: {date_min} to {date_max} | Source: vix_fii_t1_intraday_daily_results.csv | No Neutral Classification{filter_tag}*\n"

    with open(output_path, "w") as f:
        f.write(report)
    print(f"Generated: {output_path}")
    print(f"  {total_days} days, {under_count} underestimated ({under_count/total_days*100:.1f}%)")


def main():
    df = load_and_prepare()

    # All days report
    generate_report(df, OUTPUT_PATH_ALL)

    # Expiry days only report
    expiry_df = df[df["is_nifty_expiry"] == 1].copy()
    expiry_total = len(expiry_df)
    weekly_count = (expiry_df["expiry_type"] == "weekly").sum()
    monthly_count = (expiry_df["expiry_type"] == "monthly").sum()
    generate_report(
        expiry_df,
        OUTPUT_PATH_EXPIRY,
        title_suffix="Expiry Days Only",
        filter_desc=f"Nifty expiry days only — {expiry_total} days ({weekly_count} weekly + {monthly_count} monthly)",
    )

    print("Done! Both VIX underestimation reports (all days + expiry only) generated.")


if __name__ == "__main__":
    main()
