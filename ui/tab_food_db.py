import pandas as pd
import plotly.express as px
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


def _bar_chart(df_full: pd.DataFrame, nutrient_col: str, nutrient_key: str) -> None:
    top = (
        df_full[["Продукт", "Категория", nutrient_col, "Калории", "Белки (г)", "Клетчатка (г)"]]
        .sort_values(nutrient_col, ascending=True)
        .tail(15)
    )

    fig = px.bar(
        top,
        x=nutrient_col,
        y="Продукт",
        orientation="h",
        color="Категория",
        color_discrete_map=_CATEGORY_COLORS,
        custom_data=["Категория", "Калории", "Белки (г)", "Клетчатка (г)"],
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            f"<b>{nutrient_col}:</b> %{{x:.1f}}<br>"
            "<b>Категория:</b> %{customdata[0]}<br>"
            "<b>Калории:</b> %{customdata[1]:.0f} ккал<br>"
            "<b>Белки:</b> %{customdata[2]:.1f} г<br>"
            "<b>Клетчатка:</b> %{customdata[3]:.1f} г"
            "<extra></extra>"
        ),
        marker_line_width=0,
    )

    fig.update_layout(
        xaxis_title=nutrient_col,
        yaxis_title="",
        legend_title="Категория",
        height=480,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(gridcolor="#333", zerolinecolor="#555"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#2b2b2b", font_color="white", font_size=13, bordercolor="#555"),
    )

    st.plotly_chart(fig, use_container_width=True)


def _scatter_chart(df_full: pd.DataFrame) -> None:
    fig = px.scatter(
        df_full,
        x="Белки (г)",
        y="Клетчатка (г)",
        size="Калории",
        color="Категория",
        hover_name="Продукт",
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
        xaxis_title="Белки (г на 100г)",
        yaxis_title="Клетчатка (г на 100г)",
        height=420,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(gridcolor="#333", zerolinecolor="#555"),
        yaxis=dict(gridcolor="#333", zerolinecolor="#555"),
        hoverlabel=dict(bgcolor="#2b2b2b", font_color="white", font_size=13, bordercolor="#555"),
        legend_title="Категория",
    )

    st.plotly_chart(fig, use_container_width=True)


def render_food_db_tab() -> None:
    st.header("База продуктов")
    st.caption("Все значения указаны на 100 г продукта")

    df = pd.DataFrame(FOODS).rename(columns=_COLUMN_MAP)

    col_search, col_cat = st.columns([2, 1])
    with col_search:
        search = st.text_input("Поиск", placeholder="Например: куриная, рис...")
    with col_cat:
        categories = ["Все"] + sorted(df["Категория"].unique().tolist())
        selected_cat = st.selectbox("Категория", categories)

    mask = pd.Series([True] * len(df), index=df.index)
    if search:
        mask &= df["Продукт"].str.contains(search, case=False, na=False)
    if selected_cat != "Все":
        mask &= df["Категория"] == selected_cat

    filtered = df[mask]

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
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

    tab_bar, tab_scatter = st.tabs(["Топ-15 по нутриенту", "Белки vs Клетчатка"])

    with tab_bar:
        nutrient_col = st.selectbox("Показать топ по:", list(_NUTRIENT_OPTIONS.keys()), key="nutrient_select")
        _bar_chart(df, nutrient_col, _NUTRIENT_OPTIONS[nutrient_col])

    with tab_scatter:
        st.caption("Размер точки — калорийность продукта")
        _scatter_chart(df)
