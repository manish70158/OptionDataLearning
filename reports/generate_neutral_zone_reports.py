import pandas as pd
import os
from pathlib import Path
from collections import Counter

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CSV_PATH = PROJECT_ROOT / "vix_fii_t1_intraday_daily_results.csv"
REPORTS_DIR = SCRIPT_DIR

def fii_section_order(neutral_threshold):
    tk = neutral_threshold // 1000
    return [
        "Strong Bullish", "Bullish", f"MildBull{tk}",
        f"Neutral{tk}",
        f"MildBear{tk}", "Bearish", "Strong Bearish",
    ]


def load_data():
    df = pd.read_csv(CSV_PATH)
    df["fii_composite"] = pd.to_numeric(df["fii_composite"], errors="coerce")
    df["pro_composite"] = pd.to_numeric(df["pro_composite"], errors="coerce")
    df["actual_open_close_pct"] = pd.to_numeric(df["actual_open_close_pct"], errors="coerce")
    df["actual_range_pct"] = pd.to_numeric(df["actual_range_pct"], errors="coerce")
    df["intraday_high_pct"] = pd.to_numeric(df["intraday_high_pct"], errors="coerce")
    df["intraday_low_pct"] = pd.to_numeric(df["intraday_low_pct"], errors="coerce")
    df["is_nifty_expiry"] = pd.to_numeric(df["is_nifty_expiry"], errors="coerce").fillna(0).astype(int)
    return df


def classify_composite(value, neutral_threshold):
    tk = neutral_threshold // 1000
    if pd.isna(value):
        return f"Neutral{tk}"
    if value < -100000:
        return "Strong Bearish"
    elif value < -50000:
        return "Bearish"
    elif value < -neutral_threshold:
        return f"MildBear{tk}"
    elif value <= neutral_threshold:
        return f"Neutral{tk}"
    elif value <= 50000:
        return f"MildBull{tk}"
    elif value <= 100000:
        return "Bullish"
    else:
        return "Strong Bullish"


def reclassify_views(df, neutral_threshold):
    df = df.copy()
    df["fii_view_new"] = df["fii_composite"].apply(lambda v: classify_composite(v, neutral_threshold))
    df["pro_view_new"] = df["pro_composite"].apply(lambda v: classify_composite(v, neutral_threshold))
    return df


def compute_combination_stats(df):
    results = []
    grouped = df.groupby(["fii_view_new", "pro_view_new"])
    for (fii_v, pro_v), grp in grouped:
        days = len(grp)
        green_days = (grp["nifty_day"] == "Green").sum()
        green_pct = (green_days / days) * 100 if days > 0 else 0.0
        avg_chg = grp["actual_open_close_pct"].mean()
        avg_range = grp["actual_range_pct"].mean()
        up_from_open = grp["intraday_high_pct"].mean() * 100
        down_from_open = grp["intraday_low_pct"].abs().mean() * 100
        move_counts = grp["move_direction"].value_counts()
        dominant_move = move_counts.index[0] if len(move_counts) > 0 else "Mixed"
        dominant_pct = (move_counts.iloc[0] / days) * 100 if len(move_counts) > 0 else 0
        results.append({
            "fii_view": fii_v,
            "pro_view": pro_v,
            "days": days,
            "green_pct": green_pct,
            "avg_chg": avg_chg,
            "avg_range": avg_range,
            "up_from_open": up_from_open,
            "down_from_open": down_from_open,
            "dominant_move": dominant_move,
            "dominant_pct": dominant_pct,
        })
    return pd.DataFrame(results)


def compute_expiry_stats(df):
    results = []
    grouped = df.groupby(["fii_view_new", "pro_view_new"])
    for (fii_v, pro_v), grp in grouped:
        exp = grp[grp["is_nifty_expiry"] == 1]
        non_exp = grp[grp["is_nifty_expiry"] == 0]
        exp_days = len(exp)
        non_exp_days = len(non_exp)
        if exp_days > 0:
            exp_green_pct = (exp["nifty_day"] == "Green").sum() / exp_days * 100
        else:
            exp_green_pct = None
        if non_exp_days > 0:
            non_exp_green_pct = (non_exp["nifty_day"] == "Green").sum() / non_exp_days * 100
        else:
            non_exp_green_pct = None
        results.append({
            "fii_view": fii_v,
            "pro_view": pro_v,
            "exp_days": exp_days,
            "non_exp_days": non_exp_days,
            "exp_green_pct": exp_green_pct,
            "non_exp_green_pct": non_exp_green_pct,
        })
    return pd.DataFrame(results)


def fmt_pct(val, decimals=2):
    if val is None or pd.isna(val):
        return "-"
    sign = "+" if val > 0 else ""
    return f"{sign}{val:.{decimals}f}%"


def fmt_pct_nosign(val, decimals=2):
    if val is None or pd.isna(val):
        return "-"
    return f"{val:.{decimals}f}%"


def generate_header(df, neutral_threshold):
    total_days = len(df)
    date_min = df["date"].min()
    date_max = df["date"].max()
    combos = df.groupby(["fii_view_new", "pro_view_new"]).ngroups
    threshold_k = neutral_threshold // 1000
    lines = [
        f"# FII VIEW x PRO VIEW — All Combinations Analysis (±{threshold_k}K Neutral)",
        "",
        f"**Dataset**: {total_days:,} days | {date_min} to {date_max} | {combos} unique combinations",
        "",
        f"### Label Guide",
        f"- **Neutral{threshold_k}** = composite between ±{threshold_k}K (i.e. -{threshold_k}K to +{threshold_k}K)",
        f"- **MildBull{threshold_k}** = Mildly Bullish = composite +{threshold_k}K to +50K",
        f"- **MildBear{threshold_k}** = Mildly Bearish = composite -{threshold_k}K to -50K",
        f"- **Bullish / Bearish** = composite ±50K to ±100K (fixed across all thresholds)",
        f"- **Strong Bullish / Strong Bearish** = composite beyond ±100K (fixed across all thresholds)",
    ]
    return "\n".join(lines)


def generate_fii_distribution(df, stats):
    total_days = len(df)
    fii_dist = df["fii_view_new"].value_counts().reset_index()
    fii_dist.columns = ["FII View", "Days"]
    fii_dist = fii_dist.sort_values("Days", ascending=False)
    lines = [
        "## FII View Distribution",
        "",
        "| FII View | Days | % of Total |",
        "|---|---|---|",
    ]
    for _, row in fii_dist.iterrows():
        pct = row["Days"] / total_days * 100
        lines.append(f"| {row['FII View']} | {row['Days']} | {pct:.2f}% |")
    return "\n".join(lines)


def generate_master_table(stats, expiry_stats):
    merged = stats.merge(expiry_stats, on=["fii_view", "pro_view"], how="left")
    merged = merged.sort_values("green_pct", ascending=False)
    lines = [
        "## Master Summary Table (Sorted by Green% Descending)",
        "",
        "| FII View | PRO View | Days | Green% | Avg Chg% | Dominant Pattern | Exp G% | Non-Exp G% |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for _, r in merged.iterrows():
        bold = r["days"] >= 5
        fii = f"**{r['fii_view']}**" if bold else r["fii_view"]
        pro = f"**{r['pro_view']}**" if bold else r["pro_view"]
        days_s = f"**{r['days']}**" if bold else str(r["days"])
        green_s = f"**{r['green_pct']:.2f}%**" if bold else f"{r['green_pct']:.2f}%"
        chg_s = f"**{fmt_pct(r['avg_chg'], 3)}**" if bold else fmt_pct(r["avg_chg"], 3)
        dom = r["dominant_move"]
        dom_pct = r["dominant_pct"]
        if dom_pct >= 55:
            pattern = f"{dom} ({dom_pct:.0f}%)"
        else:
            pattern = "Mixed"
        pattern_s = f"**{pattern}**" if bold else pattern
        exp_g = fmt_pct_nosign(r.get("exp_green_pct"), 1)
        non_exp_g = fmt_pct_nosign(r.get("non_exp_green_pct"), 1)
        if bold:
            exp_g_s = f"**{exp_g}**" if exp_g != "-" else "-"
            non_exp_g_s = f"**{non_exp_g}**" if non_exp_g != "-" else non_exp_g
        else:
            exp_g_s = exp_g
            non_exp_g_s = non_exp_g
        lines.append(f"| {fii} | {pro} | {days_s} | {green_s} | {chg_s} | {pattern_s} | {exp_g_s} | {non_exp_g_s} |")
    return "\n".join(lines)


def generate_fii_sections(stats, df, neutral_threshold=20000):
    lines = []
    section_num = 1
    for fii_view in fii_section_order(neutral_threshold):
        section_stats = stats[stats["fii_view"] == fii_view].copy()
        if section_stats.empty:
            continue
        total_days = section_stats["days"].sum()
        section_stats = section_stats.sort_values("green_pct", ascending=False)
        lines.append(f"## Section {section_num}: FII {fii_view.upper()} ({total_days} days)")
        lines.append("")
        lines.append("| PRO View | Days | Green% | Avg Chg% | Avg Range% | Up from Open | Down from Open | Dominant Move |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for _, r in section_stats.iterrows():
            dom = r["dominant_move"]
            dom_pct = r["dominant_pct"]
            if dom_pct >= 55:
                dom_str = f"{dom} ({dom_pct:.0f}%)"
            else:
                dom_str = "Mixed"
            lines.append(
                f"| {r['pro_view']} | {r['days']} | {r['green_pct']:.2f}% "
                f"| {fmt_pct(r['avg_chg'], 3)} | {r['avg_range']:.3f}% "
                f"| {r['up_from_open']:.1f} | {r['down_from_open']:.1f} "
                f"| {dom_str} |"
            )
        lines.append("")
        # Generate pattern insight
        best = section_stats.iloc[0]
        worst = section_stats.iloc[-1]
        insight = _generate_section_insight(fii_view, section_stats, best, worst, total_days)
        lines.append(insight)
        lines.append("")
        section_num += 1
    return "\n".join(lines)


def _generate_section_insight(fii_view, section_stats, best, worst, total_days):
    best_pro = best["pro_view"]
    best_green = best["green_pct"]
    best_chg = best["avg_chg"]
    worst_pro = worst["pro_view"]
    worst_green = worst["green_pct"]
    worst_chg = worst["avg_chg"]

    parts = []
    if best["days"] >= 3:
        parts.append(
            f"**Pattern**: {fii_view} FII works best with {best_pro} PRO "
            f"({best_green:.0f}% Green, {fmt_pct(best_chg, 3)} avg)."
        )
    if worst["days"] >= 3 and worst_pro != best_pro:
        parts.append(
            f"{worst_pro} PRO is the worst ({worst_green:.0f}% Green, {fmt_pct(worst_chg, 3)} avg)."
        )
    # Find large-sample notable combos
    large = section_stats[section_stats["days"] >= 10]
    if not large.empty:
        notable = large.iloc[0]
        if notable["pro_view"] != best_pro:
            parts.append(
                f"Largest sample: {notable['pro_view']} PRO ({notable['days']} days, "
                f"{notable['green_pct']:.1f}% Green)."
            )
    if not parts:
        parts.append(f"**Pattern**: Limited data for {fii_view} FII combinations.")
    return " ".join(parts)


def generate_top_bottom_tables(stats):
    filtered = stats[stats["days"] >= 5].copy()
    lines = []

    # Top 5 Best by Green%
    top_green = filtered.sort_values("green_pct", ascending=False).head(5)
    lines.append("## Top 5 Best Combinations (>=5 days)")
    lines.append("")
    lines.append("| Rank | FII View | PRO View | Days | Green% | Avg Chg% |")
    lines.append("|---|---|---|---|---|---|")
    for rank, (_, r) in enumerate(top_green.iterrows(), 1):
        lines.append(f"| {rank} | {r['fii_view']} | {r['pro_view']} | {r['days']} | **{r['green_pct']:.2f}%** | {fmt_pct(r['avg_chg'], 3)} |")
    lines.append("")

    # Top 5 Worst by Green%
    bottom_green = filtered.sort_values("green_pct", ascending=True).head(5)
    lines.append("## Top 5 Worst Combinations (>=5 days)")
    lines.append("")
    lines.append("| Rank | FII View | PRO View | Days | Green% | Avg Chg% |")
    lines.append("|---|---|---|---|---|---|")
    for rank, (_, r) in enumerate(bottom_green.iterrows(), 1):
        lines.append(f"| {rank} | {r['fii_view']} | {r['pro_view']} | {r['days']} | **{r['green_pct']:.2f}%** | {fmt_pct(r['avg_chg'], 3)} |")
    lines.append("")

    # Top 5 Highest Avg Change
    top_chg = filtered.sort_values("avg_chg", ascending=False).head(5)
    lines.append("## Top 5 Highest Avg Change (>=5 days)")
    lines.append("")
    lines.append("| Rank | FII View | PRO View | Days | Avg Chg% | Green% |")
    lines.append("|---|---|---|---|---|---|")
    for rank, (_, r) in enumerate(top_chg.iterrows(), 1):
        lines.append(f"| {rank} | {r['fii_view']} | {r['pro_view']} | {r['days']} | **{fmt_pct(r['avg_chg'], 3)}** | {r['green_pct']:.2f}% |")
    lines.append("")

    # Top 5 Lowest Avg Change
    bottom_chg = filtered.sort_values("avg_chg", ascending=True).head(5)
    lines.append("## Top 5 Lowest Avg Change (>=5 days)")
    lines.append("")
    lines.append("| Rank | FII View | PRO View | Days | Avg Chg% | Green% |")
    lines.append("|---|---|---|---|---|---|")
    for rank, (_, r) in enumerate(bottom_chg.iterrows(), 1):
        lines.append(f"| {rank} | {r['fii_view']} | {r['pro_view']} | {r['days']} | **{fmt_pct(r['avg_chg'], 3)}** | {r['green_pct']:.2f}% |")

    return "\n".join(lines)


def generate_expiry_divergence(expiry_stats):
    lines = [
        "## Expiry vs Non-Expiry Divergence (>15%, >=3 days each side)",
        "",
        "| FII View | PRO View | Exp Days | Exp G% | Non-Exp Days | Non-Exp G% | Divergence |",
        "|---|---|---|---|---|---|---|",
    ]
    rows = []
    for _, r in expiry_stats.iterrows():
        if r["exp_days"] < 3 or r["non_exp_days"] < 3:
            continue
        if r["exp_green_pct"] is None or r["non_exp_green_pct"] is None:
            continue
        if pd.isna(r["exp_green_pct"]) or pd.isna(r["non_exp_green_pct"]):
            continue
        div = abs(r["exp_green_pct"] - r["non_exp_green_pct"])
        if div > 15:
            rows.append({**r.to_dict(), "divergence": div})
    rows.sort(key=lambda x: x["divergence"], reverse=True)
    for row in rows:
        lines.append(
            f"| {row['fii_view']} | {row['pro_view']} | {row['exp_days']} "
            f"| {row['exp_green_pct']:.1f}% | {row['non_exp_days']} "
            f"| {row['non_exp_green_pct']:.1f}% | **{row['divergence']:.1f}%** |"
        )
    return "\n".join(lines)


def generate_conclusion(stats, neutral_threshold, df):
    threshold_k = neutral_threshold // 1000
    filtered = stats[stats["days"] >= 5].copy()
    total_days = len(df)
    neutral_days = (df["fii_view_new"] == "Neutral").sum()
    neutral_pct = neutral_days / total_days * 100
    mild_bull = (df["fii_view_new"] == "Mildly Bullish").sum()
    mild_bear = (df["fii_view_new"] == "Mildly Bearish").sum()

    # Find best and worst combos
    if not filtered.empty:
        best = filtered.sort_values("green_pct", ascending=False).iloc[0]
        worst = filtered.sort_values("green_pct", ascending=True).iloc[0]
        best_chg = filtered.sort_values("avg_chg", ascending=False).iloc[0]
        worst_chg = filtered.sort_values("avg_chg", ascending=True).iloc[0]
    else:
        return "## Conclusion\n\nInsufficient data with >=5 day combinations for conclusions."

    # Find contrarian and aligned patterns
    bullish_aligned = filtered[
        (filtered["fii_view"].isin(["Bullish", "Strong Bullish"])) &
        (filtered["pro_view"].isin(["Bullish", "Strong Bullish"]))
    ]
    contrarian = filtered[
        (filtered["fii_view"].isin(["Bearish", "Strong Bearish", "Mildly Bearish"])) &
        (filtered["pro_view"].isin(["Bullish", "Strong Bullish"]))
    ]

    # Find "Down to Up" dominant combos
    dtu_combos = filtered[
        (filtered["dominant_move"] == "Down to Up") & (filtered["dominant_pct"] >= 55)
    ]

    lines = ["## Conclusion", ""]
    lines.append(f"### Analysis with ±{threshold_k}K Neutral Zone")
    lines.append("")
    lines.append(f"**Distribution impact**: With ±{threshold_k}K neutral, {neutral_days} days ({neutral_pct:.1f}%) "
                 f"are classified as FII Neutral, {mild_bull} as Mildly Bullish, {mild_bear} as Mildly Bearish.")
    lines.append("")
    lines.append("### Key Findings:")
    lines.append("")

    finding_num = 1

    lines.append(f"{finding_num}. **Best combination (≥5 days)**: {best['fii_view']} FII + {best['pro_view']} PRO = "
                 f"**{best['green_pct']:.1f}% Green** across {best['days']} days, {fmt_pct(best['avg_chg'], 3)} avg change.")
    finding_num += 1

    lines.append(f"{finding_num}. **Worst combination (≥5 days)**: {worst['fii_view']} FII + {worst['pro_view']} PRO = "
                 f"**{worst['green_pct']:.1f}% Green** across {worst['days']} days, {fmt_pct(worst['avg_chg'], 3)} avg change.")
    finding_num += 1

    if not bullish_aligned.empty:
        ba_best = bullish_aligned.sort_values("green_pct", ascending=False).iloc[0]
        ba_worst = bullish_aligned.sort_values("green_pct", ascending=True).iloc[0]
        lines.append(f"{finding_num}. **Bullish alignment**: Best = {ba_best['fii_view']}+{ba_best['pro_view']} "
                     f"({ba_best['green_pct']:.1f}%, {ba_best['days']}d), "
                     f"Worst = {ba_worst['fii_view']}+{ba_worst['pro_view']} "
                     f"({ba_worst['green_pct']:.1f}%, {ba_worst['days']}d).")
        finding_num += 1

    if not contrarian.empty:
        ct_best = contrarian.sort_values("green_pct", ascending=False).iloc[0]
        lines.append(f"{finding_num}. **Contrarian signal**: {ct_best['fii_view']} FII + {ct_best['pro_view']} PRO = "
                     f"{ct_best['green_pct']:.1f}% Green ({ct_best['days']}d) — bearish FII opposed by bullish PRO tends to recover.")
        finding_num += 1

    if not dtu_combos.empty:
        dtu_count = len(dtu_combos)
        lines.append(f"{finding_num}. **\"Down to Up\" dominance**: {dtu_count} combinations (≥5 days) show "
                     f"Down to Up as dominant pattern — morning dips followed by afternoon recovery remain the primary winning mechanism.")
        finding_num += 1

    # Note about threshold impact
    lines.append(f"{finding_num}. **Neutral zone impact**: The ±{threshold_k}K threshold classifies {neutral_pct:.1f}% of days as Neutral. "
                 f"{'Wider mild categories capture more transitional days, potentially revealing signals hidden in the standard ±30K neutral.' if threshold_k < 30 else 'This matches the standard classification.'}")
    finding_num += 1

    lines.append("")
    lines.append("### Actionable Rules:")
    lines.append("")

    # Build rules from data
    if not filtered.empty:
        go_long = filtered[filtered["green_pct"] >= 65].sort_values("green_pct", ascending=False)
        if not go_long.empty:
            combos_str = ", ".join(
                f"{r['fii_view']} FII + {r['pro_view']} PRO ({r['green_pct']:.0f}%)"
                for _, r in go_long.head(3).iterrows()
            )
            lines.append(f"- **Go long**: {combos_str}")

        high_conf = filtered[(filtered["green_pct"] >= 55) & (filtered["days"] >= 15)]
        if not high_conf.empty:
            combos_str = ", ".join(
                f"{r['fii_view']}+{r['pro_view']} ({r['green_pct']:.0f}%, {r['days']}d)"
                for _, r in high_conf.sort_values("green_pct", ascending=False).head(3).iterrows()
            )
            lines.append(f"- **Go long (high confidence, large sample)**: {combos_str}")

        avoid = filtered[(filtered["green_pct"] <= 35) & (filtered["days"] >= 15)]
        if not avoid.empty:
            combos_str = ", ".join(
                f"{r['fii_view']}+{r['pro_view']} ({r['green_pct']:.0f}%, {r['days']}d)"
                for _, r in avoid.sort_values("green_pct", ascending=True).head(3).iterrows()
            )
            lines.append(f"- **Avoid longs / consider shorts**: {combos_str}")

    lines.append("- **Expiry caution**: Reduce position size on expiry days, patterns are less reliable")

    return "\n".join(lines)


def generate_report(neutral_threshold, output_path):
    df = load_data()
    df = reclassify_views(df, neutral_threshold)
    stats = compute_combination_stats(df)
    expiry_stats = compute_expiry_stats(df)

    sections = [
        generate_header(df, neutral_threshold),
        generate_fii_distribution(df, stats),
        generate_master_table(stats, expiry_stats),
    ]

    # Per-FII sections
    sections.append(generate_fii_sections(stats, df, neutral_threshold))

    sections.append(generate_top_bottom_tables(stats))
    sections.append(generate_expiry_divergence(expiry_stats))
    sections.append(generate_conclusion(stats, neutral_threshold, df))

    report = "\n\n---\n\n".join(sections) + "\n"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(report)

    threshold_k = neutral_threshold // 1000
    print(f"Generated: {output_path} (±{threshold_k}K neutral, {len(df)} days, {len(stats)} combinations)")


def main():
    generate_report(30000, str(REPORTS_DIR / "FII_PRO_NEUTRAL_30K_ANALYSIS.md"))
    generate_report(25000, str(REPORTS_DIR / "FII_PRO_NEUTRAL_25K_ANALYSIS.md"))
    generate_report(20000, str(REPORTS_DIR / "FII_PRO_NEUTRAL_20K_ANALYSIS.md"))
    generate_report(10000, str(REPORTS_DIR / "FII_PRO_NEUTRAL_10K_ANALYSIS.md"))
    print("Done! All 4 reports generated in reports/ directory.")


if __name__ == "__main__":
    main()
