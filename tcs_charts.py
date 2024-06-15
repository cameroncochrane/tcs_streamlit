import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import TCS_pipeline as tcs

usa_data = tcs.TCSpipelineCountry(country='USA')
tcs.fill_m_q_p(usa_data)

usa_chart = tcs.return_plot(data=usa_data,country_name='USA')

st.pyplot(fig=usa_chart,use_container_width=True)

