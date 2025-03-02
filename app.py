import streamlit as st

st.set_page_config(page_title='Xfinity Personalized Recommendation System', layout='centered')

st.markdown("""
    <style>
    div.stButton > button:first-child {
        transition: all 0.3s ease;
    }
    div.stButton > button.active {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

if 'selected_services' not in st.session_state:
    st.session_state.selected_services = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'internet_speed' not in st.session_state:
    st.session_state.internet_speed = None

INTERNET_PLANS = {
    "Basic Browsing": {
        "speed": "150 Mbps",
        "price": "$19.99/month",
        "desc": "Suitable for browsing & streaming music",
        "source": "HIGHSPEEDINTERNET.COM"
    },
    "Family Streaming": {
        "speed": "300 Mbps", 
        "price": "$25.00/month",
        "desc": "HD streaming & medium file downloads",
        "source": "HIGHSPEEDINTERNET.COM"
    },
    "Home Office": {
        "speed": "500 Mbps",
        "price": "$60.00/month",
        "desc": "Work from home & quick downloads",
        "offers": ["2-year price guarantee", "WiFi equipment included"]
    },
    "Power User": {
        "speed": "1000 Mbps",
        "price": "$70.00/month",
        "desc": "Large file downloads & 4K streaming",
        "offers": ["$200 Amazon gift card", "Peacock Premium included"]
    },
    "Gamer/Streamer": {
        "speed": "1200 Mbps",
        "price": "$80.00/month",
        "desc": "4K streaming on all devices & ultra-low lag",
        "offers": ["Unlimited data", "Premium streaming package"]
    }
}

if st.session_state.current_step == 1:
    st.subheader('Which Xfinity services are you interested in?')
    
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
        st.success(f'Selected: {", ".join(st.session_state.selected_services)}')
    
    if st.button('Next →'):
        if not st.session_state.selected_services:
            st.warning('Please select at least one service')
        else:
            st.session_state.current_step = 2

elif st.session_state.current_step == 2 and 'Internet' in st.session_state.selected_services:
    st.subheader("How do you primarily use the internet?")
    
    speed_options = [
        ("Basic Browsing", "Just checking emails and light web surfing"),
        ("Family Streaming", "Streaming movies and music in HD"),
        ("Home Office", "Video calls and large file transfers"),
        ("Power User", "Gaming and 4K streaming"),
        ("Gamer/Streamer", "Multiple 4K streams and competitive gaming")
    ]
    
    for option, desc in speed_options:
        if st.button(
            f"**{option}**  \n{desc}",
            key=option,
            use_container_width=True,
            type="primary" if st.session_state.internet_speed == option else "secondary"
        ):
            st.session_state.internet_speed = option
            st.rerun()
    
    if st.session_state.internet_speed:
        selected_plan = INTERNET_PLANS[st.session_state.internet_speed]
        st.markdown(f"""
        ### Selected Plan: {st.session_state.internet_speed}
        - **Speed**: {selected_plan['speed']}
        - **Price**: {selected_plan['price']}
        - **Best for**: {selected_plan['desc']}
        {'- **Includes**: ' + ', '.join(selected_plan.get('offers', [])) if 'offers' in selected_plan else ''}
        """)
        
        if st.button('Confirm Selection →'):
            st.session_state.current_step = 3
    else:
        st.info("Select your primary internet usage to see recommended plans")

elif st.session_state.current_step == 3:
    st.subheader("Your Recommended Plan")
    
    if 'Internet' in st.session_state.selected_services:
        selected_plan = INTERNET_PLANS[st.session_state.internet_speed]
        st.markdown(f"""
        ### Internet Plan: {st.session_state.internet_speed}
        - **Speed**: {selected_plan['speed']}
        - **Monthly Cost**: {selected_plan['price']}
        - **Ideal For**: {selected_plan['desc']}
        """)
        
        if 'offers' in selected_plan:
            st.markdown("**Special Offers:**")
            for offer in selected_plan['offers']:
                st.markdown(f"- {offer}")
        
    if st.button('Start Over'):
        st.session_state.clear()
        st.rerun()