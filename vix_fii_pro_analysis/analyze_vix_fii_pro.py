#!/usr/bin/env python3
"""Analyze which FII+Pro view combinations dominate when VIX accuracy is wrong."""

import os
import sys
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CSV_PATH = os.path.join(PROJECT_ROOT, "vix_fii_t1_intraday_daily_results.csv")
OUTPUT_DIR = SCRIPT_DIR

REQUIRED_COLS = ["vix_accuracy", "fii_view", "pro_view", "nifty_day",
                 "fii_composite", "pro_composite", "move_direction",
                 "actual_range_pct", "actual_open_close_pct"]


def load_data():
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: CSV file not found at {CSV_PATH}")
        sys.exit(1)

    df = pd.read_csv(CSV_PATH)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        print(f"ERROR: Missing required columns: {missing}")
        sys.exit(1)

    print(f"Loaded {len(df)} rows from {os.path.basename(CSV_PATH)}")
    return df


def classify_view(composite, neutral_threshold):
    """Classify composite score into a view label using the given neutral threshold."""
    if composite <= -100000:
        return "Strong Bearish"
    elif composite <= -50000:
        return "Bearish"
    elif composite <= -neutral_threshold:
        return "Mildly Bearish"
    elif composite <= neutral_threshold:
        return f"Neutral{neutral_threshold // 1000}"
    elif composite <= 50000:
        return "Mildly Bullish"
    elif composite <= 100000:
        return "Bullish"
    else:
        return "Strong Bullish"


def rank_combinations(df, fii_col="fii_view", pro_col="pro_view"):
    """Compute ranked FII+Pro view combinations with move direction breakdown."""
    grouped = df.groupby([fii_col, pro_col])

    rows = []
    for (fii, pro), group in grouped:
        total_count = len(group)
        top_to_down = (group["move_direction"] == "Top to Down").sum()
        down_to_up = (group["move_direction"] == "Down to Up").sum()
        avg_range = group["actual_range_pct"].mean()
        avg_oc = group["actual_open_close_pct"].mean()
        # Average move for each direction
        ttd_group = group[group["move_direction"] == "Top to Down"]
        dtu_group = group[group["move_direction"] == "Down to Up"]
        avg_range_ttd = ttd_group["actual_range_pct"].mean() if len(ttd_group) > 0 else 0
        avg_oc_ttd = ttd_group["actual_open_close_pct"].mean() if len(ttd_group) > 0 else 0
        avg_range_dtu = dtu_group["actual_range_pct"].mean() if len(dtu_group) > 0 else 0
        avg_oc_dtu = dtu_group["actual_open_close_pct"].mean() if len(dtu_group) > 0 else 0

        rows.append({
            "fii_view": fii,
            "pro_view": pro,
            "count": total_count,
            "top_to_down": top_to_down,
            "ttd_pct": round(top_to_down / total_count * 100, 1),
            "down_to_up": down_to_up,
            "dtu_pct": round(down_to_up / total_count * 100, 1),
            "avg_range_pct": round(avg_range, 2),
            "avg_oc_pct": round(avg_oc, 2),
            "avg_range_ttd": round(avg_range_ttd, 2),
            "avg_oc_ttd": round(avg_oc_ttd, 2),
            "avg_range_dtu": round(avg_range_dtu, 2),
            "avg_oc_dtu": round(avg_oc_dtu, 2),
        })

    counts = pd.DataFrame(rows)
    counts = counts[counts["count"] > 0].sort_values("count", ascending=False).reset_index(drop=True)
    total = counts["count"].sum()
    counts["percentage"] = (counts["count"] / total * 100).round(2)
    counts["rank"] = range(1, len(counts) + 1)
    counts = counts[["rank", "fii_view", "pro_view", "count", "percentage",
                      "top_to_down", "ttd_pct", "down_to_up", "dtu_pct",
                      "avg_range_pct", "avg_oc_pct",
                      "avg_range_ttd", "avg_oc_ttd",
                      "avg_range_dtu", "avg_oc_dtu"]]
    return counts


def hit_rate_analysis(df, fii_col="fii_view", pro_col="pro_view", ratio_threshold=1.5):
    """For each combination, compute what % of days exceed ratio_threshold x VIX."""
    grouped = df.groupby([fii_col, pro_col])

    rows = []
    for (fii, pro), group in grouped:
        total = len(group)
        above = (group["range_vs_vix_ratio"] > ratio_threshold).sum()
        hit_rate = round(above / total * 100, 1) if total > 0 else 0
        avg_ratio = round(group["range_vs_vix_ratio"].mean(), 2)
        avg_range = round(group["actual_range_pct"].mean(), 2)
        avg_oc = round(group["actual_open_close_pct"].mean(), 2)
        ttd = (group["move_direction"] == "Top to Down").sum()
        dtu = (group["move_direction"] == "Down to Up").sum()
        ttd_pct = round(ttd / total * 100, 1) if total > 0 else 0
        dtu_pct = round(dtu / total * 100, 1) if total > 0 else 0

        # Stats only for the days that exceeded the threshold
        above_df = group[group["range_vs_vix_ratio"] > ratio_threshold]
        if len(above_df) > 0:
            above_avg_ratio = round(above_df["range_vs_vix_ratio"].mean(), 2)
            above_avg_range = round(above_df["actual_range_pct"].mean(), 2)
            above_avg_oc = round(above_df["actual_open_close_pct"].mean(), 2)
            above_ttd = (above_df["move_direction"] == "Top to Down").sum()
            above_dtu = (above_df["move_direction"] == "Down to Up").sum()
            above_ttd_pct = round(above_ttd / len(above_df) * 100, 1)
            above_dtu_pct = round(above_dtu / len(above_df) * 100, 1)
        else:
            above_avg_ratio = 0
            above_avg_range = 0
            above_avg_oc = 0
            above_ttd = 0
            above_dtu = 0
            above_ttd_pct = 0
            above_dtu_pct = 0

        rows.append({
            "fii_view": fii,
            "pro_view": pro,
            "total_days": total,
            "days_above_1_5x": above,
            "hit_rate_pct": hit_rate,
            "avg_ratio": avg_ratio,
            "avg_range_pct": avg_range,
            "avg_oc_pct": avg_oc,
            "ttd": ttd,
            "ttd_pct": ttd_pct,
            "dtu": dtu,
            "dtu_pct": dtu_pct,
            "above_avg_ratio": above_avg_ratio,
            "above_avg_range_pct": above_avg_range,
            "above_avg_oc_pct": above_avg_oc,
            "above_ttd": above_ttd,
            "above_ttd_pct": above_ttd_pct,
            "above_dtu": above_dtu,
            "above_dtu_pct": above_dtu_pct,
        })

    result = pd.DataFrame(rows)
    result = result.sort_values("hit_rate_pct", ascending=False).reset_index(drop=True)
    result["rank"] = range(1, len(result) + 1)
    cols = ["rank", "fii_view", "pro_view", "total_days", "days_above_1_5x",
            "hit_rate_pct", "avg_ratio", "avg_range_pct", "avg_oc_pct",
            "ttd", "ttd_pct", "dtu", "dtu_pct",
            "above_avg_ratio", "above_avg_range_pct", "above_avg_oc_pct",
            "above_ttd", "above_ttd_pct", "above_dtu", "above_dtu_pct"]
    result = result[cols]
    return result


def main():
    # --- Task 2.1: Load and validate ---
    df = load_data()

    # --- Task 2.2: Partition by VIX accuracy ---
    overestimated_df = df[df["vix_accuracy"] == "Overestimated"]
    underestimated_df = df[df["vix_accuracy"] == "Underestimated"]
    print(f"\nVIX Accuracy Partitions:")
    print(f"  Overestimated: {len(overestimated_df)} rows")
    print(f"  Underestimated: {len(underestimated_df)} rows")

    # --- Task 2.3: Cross-tabulation and ranking ---
    over_ranked = rank_combinations(overestimated_df)
    under_ranked = rank_combinations(underestimated_df)

    print(f"\n{'='*100}")
    print("RANKED FII+PRO COMBINATIONS — VIX OVERESTIMATED")
    print(f"{'='*100}")
    print(over_ranked.to_string(index=False))

    print(f"\n{'='*100}")
    print("RANKED FII+PRO COMBINATIONS — VIX UNDERESTIMATED")
    print(f"{'='*100}")
    print(under_ranked.to_string(index=False))

    # --- Task 2.4: Market direction breakdown ---
    breakdown_parts = []
    for vix_acc, vix_df in [("Overestimated", overestimated_df), ("Underestimated", underestimated_df)]:
        for day_type in ["Green", "Red"]:
            subset = vix_df[vix_df["nifty_day"] == day_type]
            if len(subset) == 0:
                continue
            ranked = rank_combinations(subset)
            ranked.insert(0, "vix_accuracy", vix_acc)
            ranked.insert(1, "nifty_day", day_type)
            breakdown_parts.append(ranked)

            print(f"\n{'='*70}")
            print(f"BREAKDOWN: {vix_acc} + {day_type} Day ({len(subset)} rows)")
            print(f"{'='*70}")
            print(ranked[["rank", "fii_view", "pro_view", "count", "percentage"]].to_string(index=False))

    market_breakdown = pd.concat(breakdown_parts, ignore_index=True)

    # --- Task 3.1: CSV export ---
    over_path = os.path.join(OUTPUT_DIR, "overestimated_combinations.csv")
    under_path = os.path.join(OUTPUT_DIR, "underestimated_combinations.csv")
    breakdown_path = os.path.join(OUTPUT_DIR, "market_direction_breakdown.csv")

    over_ranked.to_csv(over_path, index=False)
    under_ranked.to_csv(under_path, index=False)
    market_breakdown.to_csv(breakdown_path, index=False)

    print(f"\nCSV files written to {OUTPUT_DIR}/:")
    print(f"  - overestimated_combinations.csv")
    print(f"  - underestimated_combinations.csv")
    print(f"  - market_direction_breakdown.csv")

    # --- Task 3.2: Console summary report ---
    print(f"\n{'#'*70}")
    print("SUMMARY REPORT: FII+PRO DOMINANCE WHEN VIX IS WRONG")
    print(f"{'#'*70}")

    print(f"\n--- Top 5 Combinations When VIX OVERESTIMATED ({len(overestimated_df)} days) ---")
    print("(VIX predicted larger move than actual — calmer day than expected)\n")
    for _, row in over_ranked.head(5).iterrows():
        print(f"  #{int(row['rank']):2d}  FII: {row['fii_view']:<20s} + PRO: {row['pro_view']:<20s}  →  {int(row['count']):4d} days ({row['percentage']:.1f}%)")

    print(f"\n--- Top 5 Combinations When VIX UNDERESTIMATED ({len(underestimated_df)} days) ---")
    print("(VIX predicted smaller move than actual — more volatile day than expected)\n")
    for _, row in under_ranked.head(5).iterrows():
        print(f"  #{int(row['rank']):2d}  FII: {row['fii_view']:<20s} + PRO: {row['pro_view']:<20s}  →  {int(row['count']):4d} days ({row['percentage']:.1f}%)")

    # Comparison: unique to each category's top 10
    over_top10 = set(zip(over_ranked.head(10)["fii_view"], over_ranked.head(10)["pro_view"]))
    under_top10 = set(zip(under_ranked.head(10)["fii_view"], under_ranked.head(10)["pro_view"]))

    only_over = over_top10 - under_top10
    only_under = under_top10 - over_top10
    shared = over_top10 & under_top10

    print(f"\n--- Comparison: Top 10 Overlap ---")
    print(f"  Shared in both top 10:       {len(shared)} combinations")
    print(f"  Unique to Overestimated:     {len(only_over)} combinations")
    print(f"  Unique to Underestimated:    {len(only_under)} combinations")

    if only_over:
        print(f"\n  Combinations only in Overestimated top 10:")
        for fii, pro in sorted(only_over):
            print(f"    FII: {fii:<20s} + PRO: {pro}")

    if only_under:
        print(f"\n  Combinations only in Underestimated top 10:")
        for fii, pro in sorted(only_under):
            print(f"    FII: {fii:<20s} + PRO: {pro}")

    # Market direction shift highlights
    print(f"\n--- Market Direction Shifts ---")
    for vix_acc in ["Overestimated", "Underestimated"]:
        green_part = market_breakdown[(market_breakdown["vix_accuracy"] == vix_acc) & (market_breakdown["nifty_day"] == "Green")]
        red_part = market_breakdown[(market_breakdown["vix_accuracy"] == vix_acc) & (market_breakdown["nifty_day"] == "Red")]
        if len(green_part) > 0 and len(red_part) > 0:
            green_top = green_part.iloc[0]
            red_top = red_part.iloc[0]
            print(f"\n  {vix_acc}:")
            print(f"    Green day #1: FII {green_top['fii_view']} + PRO {green_top['pro_view']} ({green_top['percentage']:.1f}%)")
            print(f"    Red day   #1: FII {red_top['fii_view']} + PRO {red_top['pro_view']} ({red_top['percentage']:.1f}%)")
            if green_top["fii_view"] != red_top["fii_view"] or green_top["pro_view"] != red_top["pro_view"]:
                print(f"    → Dominant combination SHIFTS between Green and Red days")
            else:
                print(f"    → Same dominant combination on both Green and Red days")

    print(f"\n{'#'*70}")
    print("END OF ORIGINAL REPORT (Neutral30 = +-30K)")
    print(f"{'#'*70}")

    # ===================================================================
    # MULTI-THRESHOLD NEUTRAL ANALYSIS (+-30K, +-20K, +-10K)
    # ===================================================================
    thresholds = [30000, 20000, 10000]

    for thresh in thresholds:
        label = f"Neutral{thresh // 1000}"
        fii_col = f"fii_view_{thresh // 1000}k"
        pro_col = f"pro_view_{thresh // 1000}k"

        df[fii_col] = df["fii_composite"].apply(lambda x: classify_view(x, thresh))
        df[pro_col] = df["pro_composite"].apply(lambda x: classify_view(x, thresh))

    # Print distribution for each threshold
    print(f"\n{'#'*70}")
    print("MULTI-THRESHOLD NEUTRAL ANALYSIS")
    print(f"{'#'*70}")

    for thresh in thresholds:
        label = f"Neutral{thresh // 1000}"
        fii_col = f"fii_view_{thresh // 1000}k"
        pro_col = f"pro_view_{thresh // 1000}k"

        print(f"\n{'='*70}")
        print(f"THRESHOLD: +-{thresh:,} ({label})")
        print(f"{'='*70}")

        # Show how many rows fall into each neutral
        fii_neutral_count = (df[fii_col] == label).sum()
        pro_neutral_count = (df[pro_col] == label).sum()
        print(f"\n  FII {label}: {fii_neutral_count} rows ({fii_neutral_count/len(df)*100:.1f}%)")
        print(f"  PRO {label}: {pro_neutral_count} rows ({pro_neutral_count/len(df)*100:.1f}%)")

        # FII view distribution
        print(f"\n  FII View Distribution ({label}):")
        for view, count in df[fii_col].value_counts().sort_index().items():
            print(f"    {view:<20s}: {count:>5d} ({count/len(df)*100:.1f}%)")

        # PRO view distribution
        print(f"\n  PRO View Distribution ({label}):")
        for view, count in df[pro_col].value_counts().sort_index().items():
            print(f"    {view:<20s}: {count:>5d} ({count/len(df)*100:.1f}%)")

        # Top 10 for Overestimated
        over_df = df[df["vix_accuracy"] == "Overestimated"]
        under_df = df[df["vix_accuracy"] == "Underestimated"]

        over_ranked = rank_combinations(over_df, fii_col, pro_col)
        under_ranked = rank_combinations(under_df, fii_col, pro_col)

        print(f"\n  --- Top 10 When VIX OVERESTIMATED ({len(over_df)} days) ---")
        print(over_ranked.head(10).to_string(index=False))

        print(f"\n  --- Top 10 When VIX UNDERESTIMATED ({len(under_df)} days) ---")
        print(under_ranked.head(10).to_string(index=False))

        # Save CSVs
        over_path = os.path.join(OUTPUT_DIR, f"overestimated_{label.lower()}.csv")
        under_path = os.path.join(OUTPUT_DIR, f"underestimated_{label.lower()}.csv")
        over_ranked.to_csv(over_path, index=False)
        under_ranked.to_csv(under_path, index=False)
        print(f"\n  CSV: {os.path.basename(over_path)}, {os.path.basename(under_path)}")

    # ===================================================================
    # COMPARISON TABLE ACROSS ALL THREE THRESHOLDS
    # ===================================================================
    print(f"\n{'#'*70}")
    print("COMPARISON: TOP 5 ACROSS ALL NEUTRAL THRESHOLDS")
    print(f"{'#'*70}")

    for vix_acc in ["Overestimated", "Underestimated"]:
        print(f"\n{'='*70}")
        print(f"VIX {vix_acc.upper()}")
        print(f"{'='*70}")

        subset = df[df["vix_accuracy"] == vix_acc]

        for thresh in thresholds:
            label = f"Neutral{thresh // 1000}"
            fii_col = f"fii_view_{thresh // 1000}k"
            pro_col = f"pro_view_{thresh // 1000}k"
            ranked = rank_combinations(subset, fii_col, pro_col)

            print(f"\n  +-{thresh//1000}K ({label}):")
            for _, row in ranked.head(5).iterrows():
                print(f"    #{int(row['rank']):2d}  FII: {row['fii_view']:<20s} + PRO: {row['pro_view']:<20s}  {int(row['count']):4d} days ({row['percentage']:.1f}%)")

    print(f"\n{'#'*70}")
    print("END OF MULTI-THRESHOLD REPORT")
    print(f"{'#'*70}")

    # ===================================================================
    # 1.5x VIX EXCEEDANCE HIT RATE ANALYSIS
    # ===================================================================
    print(f"\n{'#'*70}")
    print("1.5x VIX EXCEEDANCE - HIT RATE ANALYSIS")
    print(f"{'#'*70}")

    # All days - original +-30K views
    hit_all_30k = hit_rate_analysis(df, "fii_view", "pro_view")
    hit_all_30k.to_csv(os.path.join(OUTPUT_DIR, "hit_rate_1_5x_all_neutral30.csv"), index=False)

    # All days - +-10K views
    hit_all_10k = hit_rate_analysis(df, "fii_view_10k", "pro_view_10k")
    hit_all_10k.to_csv(os.path.join(OUTPUT_DIR, "hit_rate_1_5x_all_neutral10.csv"), index=False)

    # All days - +-20K views
    hit_all_20k = hit_rate_analysis(df, "fii_view_20k", "pro_view_20k")
    hit_all_20k.to_csv(os.path.join(OUTPUT_DIR, "hit_rate_1_5x_all_neutral20.csv"), index=False)

    # Days where actual > 1.5x VIX only - combo breakdown
    big_moves = df[df["range_vs_vix_ratio"] > 1.5]
    big_30k = rank_combinations(big_moves, "fii_view", "pro_view")
    big_30k.to_csv(os.path.join(OUTPUT_DIR, "above_1_5x_combinations_neutral30.csv"), index=False)

    big_10k = rank_combinations(big_moves, "fii_view_10k", "pro_view_10k")
    big_10k.to_csv(os.path.join(OUTPUT_DIR, "above_1_5x_combinations_neutral10.csv"), index=False)

    big_20k = rank_combinations(big_moves, "fii_view_20k", "pro_view_20k")
    big_20k.to_csv(os.path.join(OUTPUT_DIR, "above_1_5x_combinations_neutral20.csv"), index=False)

    total_above = len(big_moves)
    print(f"\n  Days where actual range > 1.5x VIX: {total_above} of {len(df)} ({total_above/len(df)*100:.1f}%)")
    print(f"\n  CSV files written:")
    print(f"    - hit_rate_1_5x_all_neutral30.csv  (hit rate per combo, +-30K)")
    print(f"    - hit_rate_1_5x_all_neutral20.csv  (hit rate per combo, +-20K)")
    print(f"    - hit_rate_1_5x_all_neutral10.csv  (hit rate per combo, +-10K)")
    print(f"    - above_1_5x_combinations_neutral30.csv  (ranked combos for >1.5x days, +-30K)")
    print(f"    - above_1_5x_combinations_neutral20.csv  (ranked combos for >1.5x days, +-20K)")
    print(f"    - above_1_5x_combinations_neutral10.csv  (ranked combos for >1.5x days, +-10K)")

    print(f"\n{'#'*70}")
    print("END OF FULL REPORT")
    print(f"{'#'*70}")


if __name__ == "__main__":
    main()
