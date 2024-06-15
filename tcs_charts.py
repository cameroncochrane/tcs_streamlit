import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import TCS_pipeline as tcs

usa_data = tcs.TCSpipelineCountry(country='USA')
tcs.fill_m_q_p(usa_data)

usa_chart = tcs.return_plot

st.pyplot(usa_chart)

