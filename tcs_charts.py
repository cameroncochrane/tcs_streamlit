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

def uk_page():
    data = tcs.TCSpipelineCountry(country='UK')
    tcs.fill_m_q_p(data)

    uk_chart = tcs.return_plot(data=data,country_name='UK')

    st.title("UK Sales Data")
    st.pyplot(fig=uk_chart,use_container_width=True)

def germany_page():
    data = tcs.TCSpipelineCountry(country='Germany')
    tcs.fill_m_q_p(data)

    germany_chart = tcs.return_plot(data=data,country_name='Germany')

    st.title("Germany Sales Data")
    st.pyplot(fig=germany_chart,use_container_width=True)

with st.sidebar:
    selected = option_menu(menu_title="Main Menu",
        options=["USA", "UK", "Germany"],
        icons=["house", "file-earmark", "file-earmark"],
        menu_icon="cast",
        default_index=0)

if selected == "USA":
    usa_page()
if selected == "UK":
    uk_page()
if selected == "Germany":
    germany_page()