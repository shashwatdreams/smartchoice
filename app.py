import streamlit as st
import pandas as pd
import plotly.express as px

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
    .center-container {
        max-width: 800px;
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
        ("150 Mbps Plan", "Suitable for browsing the web and streaming music and movies with ease.", 19.99),
        ("300 Mbps Plan", "Ideal for downloading medium files, streaming in HD quality, and downloading music and podcasts.", 25.00),
        ("500 Mbps Plan", "Quick downloads of medium files, low lag when streaming, includes 2-year price guarantee.", 60.00),
        ("1000 Mbps (1 Gbps) Plan", "Download large files in seconds, ultra-low lag, Peacock Premium for 24 months.", 70.00),
        ("1200 Mbps Plan", "Lightning-fast speeds, ultra-low lag, 4K streaming, includes Amazon Gift Card.", 80.00)
    ],
    'Mobile': [
        ("Unlimited Plan", "30 GB premium data, unlimited hotspot, SD streaming, $20 per additional line.", 40),
        ("Unlimited Plus Plan", "50 GB premium data, 15 GB 5G hotspot, HD streaming, $30 per additional line.", 50),
        ("By the Gig Plan", "$20 per GB, unlimited mobile hotspot, HD streaming, pay only for data used.", 20)
    ],
    'TV': [
        ("Choice TV", "10+ channels, basic selection of local and popular networks.", 51.15),
        ("Sports & News TV", "50+ channels, live games, 300 hours DVR, Peacock subscription included.", 70),
        ("Popular TV", "125+ channels, wide variety of shows and movies, regional sports fee applies.", 83.05),
        ("Ultimate TV", "185+ channels, includes sports, movies, news, and entertainment.", 112.75)
    ],
    'Home Phone': [
        ("Xfinity Voice Premier", "Unlimited calls nationwide and to over 90 international destinations.", 30),
        ("Basic Calling", "Emergency and occasional calls with essential features.", 15)
    ],
    'Home Security': [
        ("Self Protection Plan", "Live and recorded video access, no contract required, equipment sold separately.", 10),
        ("Xfinity Home Security Plan", "24/7 professional monitoring, smart home integration, expert installation.", 45),
        ("Ultimate Home System", "Full security setup with cameras, sensors, and professional monitoring.", 60)
    ]
}

COMPETITOR_PRICES = {
    'Internet': [("Xfinity", 30), ("AT&T", 85), ("Verizon", 90), ("Spectrum", 80)],
    'Mobile': [("Xfinity", 40), ("T-Mobile", 55), ("Verizon", 60), ("AT&T", 65)],
    'TV': [("Xfinity", 30), ("DirecTV", 90), ("Dish", 88), ("FuboTV", 85)],
    'Home Phone': [("Xfinity", 15), ("AT&T", 35), ("Verizon", 30), ("Ooma", 28)],
    'Home Security': [("Xfinity", 10), ("ADT", 60), ("Ring", 55), ("Vivint", 70)]
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
        description = next((desc for opt, desc, price in OPTIONS[service] if opt == selected_plan), "")

        st.markdown(f"### {service} Plan: {selected_plan if selected_plan else 'Not selected'}")
        st.info(f"You're getting the best value with Xfinity's {selected_plan} plan! Enjoy top-notch service at unbeatable prices.")
        st.markdown(f"**Price:** ${selected_price:.2f} per month")
        st.markdown(f"**Features:**")
        st.markdown(f"- {description}")

        competitor_data = COMPETITOR_PRICES.get(service, [])
        df = pd.DataFrame(competitor_data, columns=['Provider', 'Price'])
        df = df.sort_values(by='Price', ascending=False)
        df['Color'] = df['Provider'].apply(lambda x: 'green' if x == 'Xfinity' else 'red')
        fig = px.bar(df, x='Provider', y='Price', color='Color',
                     color_discrete_map={'green': 'green', 'red': 'red'},
                     title=f'{service} Price Comparison',
                     labels={'Price': 'Monthly Cost ($)', 'Provider': 'Service Provider'})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

    if st.button('Start Over'):
        st.session_state.clear()
        st.rerun()
