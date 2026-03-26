import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data.foods import FOODS

_COLUMN_MAP = {
    "name":     "Продукт",
    "calories": "Калории",
    "protein":  "Белки (г)",
    "fat":      "Жиры (г)",
    "carbs":    "Углеводы (г)",
    "fiber":    "Клетчатка (г)",
    "category": "Категория",
}

_NUTRIENT_OPTIONS = {
    "Белки (г)":     "protein",
    "Клетчатка (г)": "fiber",
    "Калории":       "calories",
    "Жиры (г)":      "fat",
    "Углеводы (г)":  "carbs",
}

_CATEGORY_COLORS = {
    "Мясо":     "#E07B5A",
    "Рыба":     "#5A9BE0",
    "Молочное": "#E0C95A",
    "Крупы":    "#A0785A",
    "Овощи":    "#5AC97A",
    "Фрукты":   "#C95AB0",
    "Бобовые":  "#7A5AC9",
}


def _bar_chart(df_full: pd.DataFrame, nutrient_col: str) -> None:
    all_cols = ["Продукт", "Категория", nutrient_col, "Калории", "Белки (г)", "Клетчатка (г)", "Жиры (г)", "Углеводы (г)"]
    unique_cols = list(dict.fromkeys(all_cols))
    top = df_full[unique_cols].sort_values(nutrient_col, ascending=True).tail(15)

    fig = px.bar(
        top, x=nutrient_col, y="Продукт", orientation="h",
        color="Категория", color_discrete_map=_CATEGORY_COLORS,
        custom_data=["Категория", "Калории", "Белки (г)", "Клетчатка (г)", "Жиры (г)", "Углеводы (г)"],
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            f"<b>{nutrient_col}:</b> %{{x:.1f}}<br>"
            "<b>Категория:</b> %{customdata[0]}<br>"
            "<b>Калории:</b> %{customdata[1]:.0f} ккал<br>"
            "<b>Белки:</b> %{customdata[2]:.1f} г<br>"
            "<b>Клетчатка:</b> %{customdata[3]:.1f} г<br>"
            "<b>Жиры:</b> %{customdata[4]:.1f} г<br>"
            "<b>Углеводы:</b> %{customdata[5]:.1f} г"
            "<extra></extra>"
        ),
        marker_line_width=0,
    )
    fig.update_layout(
        xaxis_title=nutrient_col, yaxis_title="", legend_title="Категория",
        height=480, margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(gridcolor="#333", zerolinecolor="#555"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#2b2b2b", font_color="white", font_size=13, bordercolor="#555"),
    )
    st.plotly_chart(fig, use_container_width=True)


def _scatter_chart(df_full: pd.DataFrame) -> None:
    fig = px.scatter(
        df_full, x="Белки (г)", y="Клетчатка (г)", size="Калории",
        color="Категория", hover_name="Продукт",
        color_discrete_map=_CATEGORY_COLORS,
        custom_data=["Калории", "Жиры (г)", "Углеводы (г)", "Категория"],
        size_max=40,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "<b>Белки:</b> %{x:.1f} г<br>"
            "<b>Клетчатка:</b> %{y:.1f} г<br>"
            "<b>Калории:</b> %{customdata[0]:.0f} ккал<br>"
            "<b>Жиры:</b> %{customdata[1]:.1f} г<br>"
            "<b>Углеводы:</b> %{customdata[2]:.1f} г<br>"
            "<b>Категория:</b> %{customdata[3]}"
            "<extra></extra>"
        ),
        marker=dict(line=dict(width=1, color="#1e1e1e")),
    )
    fig.update_layout(
        xaxis_title="Белки (г на 100г)", yaxis_title="Клетчатка (г на 100г)",
        height=420, margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(gridcolor="#333", zerolinecolor="#555"),
        yaxis=dict(gridcolor="#333", zerolinecolor="#555"),
        hoverlabel=dict(bgcolor="#2b2b2b", font_color="white", font_size=13, bordercolor="#555"),
        legend_title="Категория",
    )
    st.plotly_chart(fig, use_container_width=True)


def _comparison_chart(df_full: pd.DataFrame, selected_names: list[str]) -> None:
    subset = df_full[df_full["Продукт"].isin(selected_names)]
    nutrients = ["Белки (г)", "Жиры (г)", "Углеводы (г)", "Клетчатка (г)"]
    colors = ["#4C9BE8", "#F4845F", "#58C4A0", "#A0785A"]

    fig = go.Figure()
    for nutrient, color in zip(nutrients, colors):
        fig.add_trace(go.Bar(
            name=nutrient,
            x=subset["Продукт"],
            y=subset[nutrient],
            marker_color=color,
            hovertemplate=f"<b>%{{x}}</b><br>{nutrient}: %{{y:.1f}} г<extra></extra>",
        ))

    fig.update_layout(
        barmode="group",
        xaxis_title="", yaxis_title="г на 100г",
        legend_title="Нутриент",
        height=380, margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(gridcolor="#333"),
        hoverlabel=dict(bgcolor="#2b2b2b", font_color="white", font_size=13, bordercolor="#555"),
    )
    st.plotly_chart(fig, use_container_width=True)


def _portion_section(df_full: pd.DataFrame) -> None:
    st.subheader("Калькулятор порции")
    col_food, col_g = st.columns([2, 1])
    with col_food:
        food_name = st.selectbox("Продукт", df_full["Продукт"].tolist(), key="portion_food")
    with col_g:
        grams = st.number_input("Граммы", min_value=1, max_value=5000, value=100, key="portion_grams")

    row = df_full[df_full["Продукт"] == food_name].iloc[0]
    ratio = grams / 100

    p1, p2, p3, p4, p5 = st.columns(5)
    p1.metric("Калории",    f"{int(row['Калории'] * ratio)} ккал")
    p2.metric("Белки",      f"{row['Белки (г)'] * ratio:.1f} г")
    p3.metric("Жиры",       f"{row['Жиры (г)'] * ratio:.1f} г")
    p4.metric("Углеводы",   f"{row['Углеводы (г)'] * ratio:.1f} г")
    p5.metric("Клетчатка",  f"{row['Клетчатка (г)'] * ratio:.1f} г")


def render_food_db_tab() -> None:
    st.header("База продуктов")
    st.caption("Все значения указаны на 100 г продукта")

    df = pd.DataFrame(FOODS).rename(columns=_COLUMN_MAP)

    # Search + category filter
    col_search, col_cat = st.columns([2, 1])
    with col_search:
        search = st.text_input("Поиск", placeholder="Например: куриная, рис...")
    with col_cat:
        categories = ["Все"] + sorted(df["Категория"].unique().tolist())
        selected_cat = st.selectbox("Категория", categories)

    # Nutrient filter
    with st.expander("Фильтр по нутриентам"):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            min_protein = st.slider("Белки не менее (г)", 0, int(df["Белки (г)"].max()), 0)
        with fc2:
            max_calories = st.slider("Калории не более", int(df["Калории"].min()), int(df["Калории"].max()), int(df["Калории"].max()))
        with fc3:
            min_fiber = st.slider("Клетчатка не менее (г)", 0, int(df["Клетчатка (г)"].max()), 0)

    mask = pd.Series([True] * len(df), index=df.index)
    if search:
        mask &= df["Продукт"].str.contains(search, case=False, na=False)
    if selected_cat != "Все":
        mask &= df["Категория"] == selected_cat
    mask &= df["Белки (г)"] >= min_protein
    mask &= df["Калории"] <= max_calories
    mask &= df["Клетчатка (г)"] >= min_fiber

    filtered = df[mask]

    st.dataframe(
        filtered, use_container_width=True, hide_index=True,
        column_config={
            "Калории":       st.column_config.NumberColumn(format="%d ккал"),
            "Белки (г)":     st.column_config.NumberColumn(format="%.1f г"),
            "Жиры (г)":      st.column_config.NumberColumn(format="%.1f г"),
            "Углеводы (г)":  st.column_config.NumberColumn(format="%.1f г"),
            "Клетчатка (г)": st.column_config.NumberColumn(format="%.1f г"),
        },
    )
    st.caption(f"Показано {len(filtered)} из {len(df)} продуктов")

    st.divider()
    _portion_section(df)

    st.divider()
    tab_bar, tab_scatter, tab_compare = st.tabs(["Топ-15 по нутриенту", "Белки vs Клетчатка", "Сравнение продуктов"])

    with tab_bar:
        nutrient_col = st.selectbox("Показать топ по:", list(_NUTRIENT_OPTIONS.keys()), key="nutrient_select")
        _bar_chart(df, nutrient_col)

    with tab_scatter:
        st.caption("Размер точки — калорийность продукта")
        _scatter_chart(df)

    with tab_compare:
        selected = st.multiselect(
            "Выберите продукты для сравнения (до 6):",
            df["Продукт"].tolist(),
            max_selections=6,
            key="compare_select",
        )
        if len(selected) >= 2:
            _comparison_chart(df, selected)
        else:
            st.info("Выберите минимум 2 продукта")
