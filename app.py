import streamlit as st

from ui.tab_calculator import render_calculator_tab
from ui.tab_diary import render_diary_tab
from ui.tab_food_db import render_food_db_tab

st.set_page_config(
    page_title="КБЖУ Трекер",
    page_icon="🥗",
    layout="wide",
)

tab1, tab2, tab3 = st.tabs(["КБЖУ Калькулятор", "База продуктов", "Дневник питания"])

with tab1:
    render_calculator_tab()

with tab2:
    render_food_db_tab()

with tab3:
    render_diary_tab()
