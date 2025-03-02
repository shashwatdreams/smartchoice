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
    .savings-box {
        background-color: #f0f8ff;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        color: black !important;
    }
    .center-container {
        max-width: 600px;
        margin: auto;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

if 'selected_services' not in st.session_state:
    st.session_state.selected_services = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

for service in ['Internet', 'Mobile', 'TV', 'Home Phone', 'Home Security']:
    normalized_key = service.replace(' ', '_').lower()
    if normalized_key not in st.session_state:
        st.session_state[normalized_key] = None

OPTIONS = {
    'Internet': [
        ("Basic Browsing", "Just checking emails and light web surfing", 30),
        ("Family Streaming", "Streaming movies and music in HD", 50),
        ("Home Office", "Video calls and large file transfers", 70),
        ("Power User", "Gaming and 4K streaming", 90),
        ("Gamer/Streamer", "Multiple 4K streams and competitive gaming", 110)
    ],
    'Mobile': [
        ("Unlimited Plan", "Lots of streaming, social media, and calls", 40),
        ("Unlimited Plus Plan", "Heavy use with video streaming and gaming", 60),
        ("By the Gig Plan", "Occasional use, mostly WiFi", 20)
    ],
    'TV': [
        ("Choice TV", "Basic channels and minimal viewing", 30),
        ("Sports & News TV", "Keeping up with live sports and news", 70),
        ("Popular TV", "A wide variety of shows and movies", 80),
        ("Ultimate TV", "All channels, including premium content", 100)
    ],
    'Home Phone': [
        ("Xfinity Voice Premier", "Nationwide and international calling", 30),
        ("Basic Calling", "Mostly emergency and occasional calls", 15)
    ],
    'Home Security': [
        ("Self Protection Plan", "Simple monitoring of home", 10),
        ("Xfinity Home Security Plan", "24/7 professional monitoring", 45),
        ("Ultimate Home System", "Full security setup with cameras and sensors", 60)
    ]
}

COMPETITOR_PRICES = {
    'Internet': [("AT&T", 85), ("Verizon", 90), ("Spectrum", 80)],
    'Mobile': [("T-Mobile", 55), ("Verizon", 60), ("AT&T", 65)],
    'TV': [("DirecTV", 90), ("Dish", 88), ("FuboTV", 85)],
    'Home Phone': [("AT&T", 35), ("Verizon", 30), ("Ooma", 28)],
    'Home Security': [("ADT", 60), ("Ring", 55), ("Vivint", 70)]
}

SERVICES = list(OPTIONS.keys())

st.markdown('<div class="center-container">', unsafe_allow_html=True)

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
            st.rerun()

elif st.session_state.current_step > 1 and st.session_state.current_step <= len(st.session_state.selected_services) + 1:
    service = st.session_state.selected_services[st.session_state.current_step - 2]
    st.subheader(f'How do you primarily use {service}?')
    for option, desc, price in OPTIONS[service]:
        normalized_key = service.replace(' ', '_').lower()
        if st.button(
            f"**{option}**  \n{desc}",
            key=f"{service}-{option}",
            use_container_width=True,
            type="primary" if st.session_state[normalized_key] == option else "secondary"
        ):
            st.session_state[normalized_key] = option
            st.session_state[f"{normalized_key}_price"] = price
            st.session_state.current_step += 1
            st.rerun()

elif st.session_state.current_step > len(st.session_state.selected_services) + 1:
    st.subheader('Your Recommended Plan')
    for service in st.session_state.selected_services:
        normalized_key = service.replace(' ', '_').lower()
        selected_plan = st.session_state.get(normalized_key)
        selected_price = st.session_state.get(f"{normalized_key}_price", 0)
        competitors = COMPETITOR_PRICES.get(service, [])
        savings_text = ""
        
        for competitor, competitor_price in competitors:
            savings = competitor_price - selected_price
            savings_text += f"💰 Xfinity beats {competitor} by **${savings} per month**<br>"
        
        st.markdown(f"### {service} Plan: {selected_plan if selected_plan else 'Not selected'}")
        st.markdown(
            f"<div class='savings-box' style='color: black !important;'>{savings_text}</div>",
            unsafe_allow_html=True
        )
    
    if st.button('Start Over'):
        st.session_state.clear()
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
