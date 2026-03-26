# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the app
.venv/bin/streamlit run app.py

# Install dependencies
.venv/bin/pip install -r requirements.txt
```

## Architecture

Streamlit app with two tabs. Entry point is `app.py` which mounts the two tabs.

**Separation of concerns:**
- `calculators/kbju.py` — pure math functions (no Streamlit imports). BMR, TDEE, deficit, macros. All testable without running the app.
- `data/foods.py` — static list of ~40 foods as `list[dict]` with keys: `name, calories, protein, fat, carbs, fiber, category`.
- `ui/tab_calculator.py` — Tab 1: inputs (body params + goal) on the left, results (st.metric cards + bar chart) on the right.
- `ui/tab_food_db.py` — Tab 2: searchable/filterable st.dataframe of foods.
- `utils/formatters.py` — display helpers (`format_kcal`, `format_grams`).

**Key formulas (in `calculators/kbju.py`):**
- BMR: Mifflin-St Jeor
- TDEE: BMR × activity multiplier derived from average daily steps (5 tiers)
- Daily deficit: `(target_kg × 7700) / period_days`
- Target calories floored at 1200 kcal
- Macros: protein = 2g/kg body weight, fat = 25% of calories, carbs = remainder
