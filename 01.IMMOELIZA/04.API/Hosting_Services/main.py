import streamlit as st
import pandas as pd
import numpy as np


st.title('Simple Streamlit App')

st.write("Here is our first attempt at using Streamlit to create a table:")
st.write(pd.DataFrame({
    'first_column': [1, 2, 3, 4],
    'second_column': [10, 20, 30, 40]
}))

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns = ['a', 'b', 'c'])
    st.line_chart(chart_data)