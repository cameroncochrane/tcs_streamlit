import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import TCS_pipeline as tcs


def usa_page():
    data = tcs.TCSpipelineCountry(country='USA')
    tcs.fill_m_q_p(data)

    usa_chart = tcs.return_plot(data=data,country_name='USA')

    st.title("USA Sales Data")
    st.pyplot(fig=usa_chart,use_container_width=True)


with st.sidebar:
    selected = option_menu(menu_title="Main Menu",
        options=["USA", "UK", "Germany"],
        icons=["house", "file-earmark", "file-earmark"],
        menu_icon="cast",
        default_index=0)

if selected == "USA":
    usa_page()