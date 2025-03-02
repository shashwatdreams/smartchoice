import streamlit as st

st.set_page_config(page_title='Xfinity Personalized Recommendation System', layout='centered')

st.markdown("""
    <style>
        /* Base button style */
        div.stButton > button {
            transition: all 0.3s ease;
        }
        
        /* Selected button style */
        div.stButton > button:focus:not(:active),
        div.stButton > button.active {
            background-color: #4CAF50 !important;
            color: white !important;
            border-color: #4CAF50 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.subheader('Which Xfinity services are you interested in?')

if 'selected_services' not in st.session_state:
    st.session_state.selected_services = []

services = ['Internet', 'Mobile', 'TV', 'Home Phone', 'Home Security']

for service in services:
    btn = st.button(
        service,
        key=service,
        use_container_width=True,
        type="primary" if service in st.session_state.selected_services else "secondary"
    )
    if btn:
        if service in st.session_state.selected_services:
            st.session_state.selected_services.remove(service)
        else:
            st.session_state.selected_services.append(service)
        st.rerun()

if st.session_state.selected_services:
    st.success('Selected services: ' + ', '.join(st.session_state.selected_services))

if st.button('Next'):
    if st.session_state.selected_services:
        st.info('Proceeding with: ' + ', '.join(st.session_state.selected_services))
    else:
        st.warning('Please select at least one service before proceeding.')