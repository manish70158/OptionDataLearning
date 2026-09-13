## Context

The existing `reports/` folder contains three Python scripts that each independently define a `classify_composite()` function with a `neutral_threshold` parameter. Each script loads the same CSVs, reclassifies FII/PRO views, then generates markdown reports. The classification logic and report generation are tightly coupled within each script — there is no shared library. See proposal.md for motivation.

Key constraint: the existing `reports/` folder must not be modified.

## Goals / Non-Goals

**Goals:**
- Create `reports_no_neutral/` with three standalone scripts that mirror the existing analysis types
- Replace the 7-tier classification (with neutral) with a 6-tier classification (no neutral)
- Produce the same report structure and metrics so results are directly comparable
- Simplify: since there is no variable neutral threshold, scripts produce one report each (not four variants)

**Non-Goals:**
- Refactoring the existing `reports/` scripts or extracting shared code
- Creating a shared classification library across `reports/` and `reports_no_neutral/`
- Changing any analysis methodology (VIX fractions, whipsaw tiers, reversal trap thresholds)
- Adding new metrics or report sections not present in the originals

## Decisions

### 1. Fork-and-modify approach over shared library
**Decision**: Copy each script from `reports/` and modify the classification logic in place.

**Rationale**: The existing scripts duplicate `classify_composite()` across all three files already. Extracting a shared module would require modifying `reports/` (violating the constraint) or creating a third-party dependency that both folders import. A simple fork keeps each folder self-contained and independently runnable.

**Alternative considered**: Shared `utils/classification.py` — rejected because it would couple the two analysis folders and require `reports/` changes.

### 2. Classification function change
**Decision**: Replace `classify_composite(value, neutral_threshold)` with `classify_composite(value)` (no threshold parameter). The boundary at zero:
- `value >= 0` → "Mildly Bullish"
- `value < 0` → "Mildly Bearish"
- NaN → "Mildly Bullish" (treat missing data as zero-equivalent, same as the current scripts' approach of mapping NaN to neutral)

**Rationale**: Zero is the natural boundary — any positive composite means net bullish positioning, any negative means net bearish.

### 3. Label naming without numeric suffixes
**Decision**: Use plain labels "Mildly Bullish" and "Mildly Bearish" instead of "MildBull20" / "MildBear20" style.

**Rationale**: The numeric suffix in the original scripts encodes the neutral threshold. With no neutral threshold, the suffix is meaningless.

### 4. Single report per analysis type
**Decision**: The directional combination script produces one report (not four variants for different thresholds). Volatility whipsaw still produces two reports (0.5x and 0.3x VIX). Reversal trap produces one report.

**Rationale**: The four-variant approach exists because of four neutral thresholds. Without neutral, there is only one classification, so only one directional report. VIX fractions are independent of the classification change, so two whipsaw variants remain.

### 5. File naming convention
**Decision**:
- `generate_directional_reports.py` → `FII_PRO_NO_NEUTRAL_DIRECTIONAL_ANALYSIS.md`
- `generate_volatility_report.py` → `FII_PRO_NO_NEUTRAL_VOLATILITY_WHIPSAW_ANALYSIS.md` and `FII_PRO_NO_NEUTRAL_VOLATILITY_WHIPSAW_0.3VIX_ANALYSIS.md`
- `generate_reversal_report.py` → `FII_PRO_NO_NEUTRAL_REVERSAL_TRAP_ANALYSIS.md`

**Rationale**: "NO_NEUTRAL" prefix makes the classification variant immediately obvious in filenames, matching the existing convention of embedding parameters in report names.

## Risks / Trade-offs

- **Code duplication**: Three scripts in `reports_no_neutral/` duplicate most logic from `reports/`. → Accepted: keeps folders independent and avoids coupling. If future refactoring extracts shared code, both can be migrated.
- **Mildly Bullish/Bearish buckets absorb former neutral days**: These buckets will have more days than their counterparts in the original analysis, potentially diluting signal strength for combinations that include them. → The whole point of this analysis is to measure whether that dilution matters or whether the direction (even at low conviction) still carries signal.
- **NaN-as-MildlyBullish assumption**: Could skew results if NaN data is concentrated in certain time periods. → Same assumption as existing scripts (NaN→Neutral), and NaN rows are rare in the dataset.
