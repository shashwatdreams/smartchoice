import streamlit as st

st.set_page_config(page_title='Xfinity Personalized Recommendation System', layout='centered')

st.markdown(
    '''
    <style>
    div.stButton > button:first-child {
        transition: all 0.3s ease;
    }
    div.stButton > button.active {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

if 'selected_services' not in st.session_state:
    st.session_state.selected_services = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

# Normalize service keys to match OPTIONS dictionary
for service in ['Internet', 'Mobile', 'TV', 'Home Phone', 'Home Security']:
    normalized_key = service.replace(' ', '_').lower()
    if normalized_key not in st.session_state:
        st.session_state[normalized_key] = None

OPTIONS = {
    'Internet': [
        ("Basic Browsing", "Just checking emails and light web surfing"),
        ("Family Streaming", "Streaming movies and music in HD"),
        ("Home Office", "Video calls and large file transfers"),
        ("Power User", "Gaming and 4K streaming"),
        ("Gamer/Streamer", "Multiple 4K streams and competitive gaming")
    ],
    'Mobile': [
        ("Unlimited Plan", "Lots of streaming, social media, and calls"),
        ("Unlimited Plus Plan", "Heavy use with video streaming and gaming"),
        ("By the Gig Plan", "Occasional use, mostly WiFi")
    ],
    'TV': [
        ("Choice TV", "Basic channels and minimal viewing"),
        ("Sports & News TV", "Keeping up with live sports and news"),
        ("Popular TV", "A wide variety of shows and movies"),
        ("Ultimate TV", "All channels, including premium content")
    ],
    'Home Phone': [
        ("Xfinity Voice Premier", "Nationwide and international calling"),
        ("Basic Calling", "Mostly emergency and occasional calls")
    ],
    'Home Security': [
        ("Self Protection Plan", "Simple monitoring of home"),
        ("Xfinity Home Security Plan", "24/7 professional monitoring"),
        ("Ultimate Home System", "Full security setup with cameras and sensors")
    ]
}

SERVICES = list(OPTIONS.keys())

if st.session_state.current_step == 1:
    st.subheader('Which Xfinity services are you interested in?')
    for service in SERVICES:
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

elif st.session_state.current_step > 1 and st.session_state.current_step <= len(st.session_state.selected_services) + 1:
    service = st.session_state.selected_services[st.session_state.current_step - 2]
    st.subheader(f'How do you primarily use {service}?')
    for option, desc in OPTIONS[service]:
        normalized_key = service.replace(' ', '_').lower()
        if st.button(
            f"**{option}**  \n{desc}",
            key=f"{service}-{option}",
            use_container_width=True,
            type="primary" if st.session_state[normalized_key] == option else "secondary"
        ):
            st.session_state[normalized_key] = option
            st.rerun()
    
    normalized_key = service.replace(' ', '_').lower()
    if st.session_state[normalized_key] is not None:
        if st.button('Next →'):
            st.session_state.current_step += 1

elif st.session_state.current_step > len(st.session_state.selected_services) + 1:
    st.subheader('Your Recommended Plan')
    for service in st.session_state.selected_services:
        normalized_key = service.replace(' ', '_').lower()
        selected_plan = st.session_state.get(normalized_key)
        st.markdown(f"### {service} Plan: {selected_plan if selected_plan else 'Not selected'}")
    if st.button('Start Over'):
        st.session_state.clear()
        st.rerun()
