import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Xfinity Personalized Recommendation System", layout="wide")

PURCHASE_LINKS = {
    "Internet": "https://www.xfinity.com/shop/internet",
    "Mobile": "https://www.xfinity.com/mobile",
    "TV": "https://www.xfinity.com/tv",
    "Home Phone": "https://www.xfinity.com/home-phone",
    "Home Security": "https://www.xfinity.com/home-security"
}

if "selected_services" not in st.session_state:
    st.session_state.selected_services = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

OPTIONS = {
    "Internet": [
        ("150 Mbps Plan", "Suitable for browsing and streaming", 19.99),
        ("300 Mbps Plan", "HD streaming and medium downloads", 25.00),
        ("500 Mbps Plan", "2-year price guarantee", 60.00),
        ("1000 Mbps Plan", "Amazon $200 gift card", 70.00),
        ("1200 Mbps Plan", "4K streaming on all devices", 80.00)
    ],
    "Mobile": [
        ("Unlimited Plan", "30GB data, SD streaming", 40),
        ("Unlimited Plus Plan", "50GB data, HD streaming", 50),
        ("By the Gig Plan", "Pay per GB used", 20)
    ],
    "TV": [
        ("Choice TV", "10+ channels", 51.15),
        ("Sports & News TV", "50+ sports channels", 70),
        ("Popular TV", "125+ channels", 83.05),
        ("Ultimate TV", "185+ channels", 112.75)
    ],
    "Home Security": [
        ("Self Protection Plan", "No contract", 10),
        ("Xfinity Home Security", "24/7 monitoring", 45),
        ("Ultimate Home System", "Full security setup", 60)
    ]
}

col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.subheader("Which Xfinity services are you interested in?")
    for service in OPTIONS:
        if st.button(service, key=service, use_container_width=True):
            st.session_state.selected_services.append(service)
            st.rerun()

with col2:
    st.subheader("Or chat with an assistant")
    if st.session_state.chat_messages:
        for msg in st.session_state.chat_messages:
            st.write(f"**{msg['role'].capitalize()}:** {msg['content']}")
    if prompt := st.chat_input("Ask about Xfinity plans..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        st.rerun()

if st.session_state.selected_services:
    st.write("### Your Selected Plans")
    total_cost = 0
    for service in st.session_state.selected_services:
        plan = OPTIONS[service][0]
        name, desc, price = plan
        total_cost += price
        st.write(f"**{service}:** {name} - ${price}/mo")
        competitors = [("Xfinity", price), ("AT&T", 85), ("Verizon", 90), ("Spectrum", 80)]
        df = pd.DataFrame(competitors, columns=["Provider", "Price"])
        fig = px.bar(df, x="Provider", y="Price", color="Provider", title=f"{service} Price Comparison")
        st.plotly_chart(fig)
    st.write(f"## Total Monthly Cost: ${total_cost:.2f}")
    if st.button("Start Over", use_container_width=True):
        st.session_state.clear()
        st.rerun()
