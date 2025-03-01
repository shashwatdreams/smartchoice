import streamlit as st

st.set_page_config(page_title='Xfinity Personalized Recommendation System', layout='centered')

st.title('Xfinity Personalized Recommendation System')

st.subheader('Which services are you interested in?')
services = st.multiselect('Select one or more options:', ['Internet', 'Mobile', 'TV', 'Home Phone', 'Home Security'])

if services:
    st.success('Services selected: ' + ', '.join(services))