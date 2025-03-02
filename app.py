import streamlit as st
import pandas as pd
import plotly.express as px
import openai

st.set_page_config(page_title='Xfinity Personalized Recommendation System', layout='centered')

openai.api_key = st.secrets["OPENAI_API_KEY"]

PURCHASE_LINKS = {
    'Internet': 'https://www.xfinity.com/shop/internet',
    'Mobile': 'https://www.xfinity.com/mobile',
    'TV': 'https://www.xfinity.com/tv',
    'Home Phone': 'https://www.xfinity.com/home-phone',
    'Home Security': 'https://www.xfinity.com/home-security'
}

SYSTEM_PROMPT = """
You are an Xfinity expert assistant. Use ONLY this product info:

[MOBILE PLANS]
- Unlimited Plan: $40/month (1 line), 30GB data, SD streaming, +$20/line
- Unlimited Plus: $50/month (1 line), 50GB data, HD streaming, +$30/line 
- By the Gig: $20/GB shared data, 4G hotspot

[TV PACKAGES]
- Choice TV: $51.15/mo + $31.15 broadcast fee
- Sports & News TV: $70/mo (50+ channels, Peacock included)
- Popular TV: $83.05/mo + $1.90 regional sports fee
- Ultimate TV: $112.75/mo + $13.10 regional fee

[HOME SECURITY]
- Self Protection: $10/mo (no equipment)
- Home Security Plan: $45/mo (professional monitoring)
- Equipment packages: $15-$25/mo

[INTERNET PLANS]
- 150Mbps: $19.99
- 300Mbps: $25
- 500Mbps: $60 (2-year price guarantee)
- 1Gbps: $70 (Amazon $200 gift card)
- 1200Mbps: $80 (4K streaming)

[PURCHASE LINKS]
Internet: https://www.xfinity.com/shop/internet
Mobile: https://www.xfinity.com/mobile
TV: https://www.xfinity.com/tv
Home Security: https://www.xfinity.com/home-security

Guidelines:
1. Recommend specific plans with pricing
2. Compare options when relevant
3. Always include purchase links
4. Mention hidden fees when applicable
5. Use bullet points and bold headers
6. Keep responses under 300 words
"""

if 'selected_services' not in st.session_state:
    st.session_state.selected_services = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

OPTIONS = {
    'Internet': [
        ("150 Mbps Plan", "Suitable for browsing and streaming", 19.99),
        ("300 Mbps Plan", "HD streaming and medium downloads", 25.00),
        ("500 Mbps Plan", "2-year price guarantee", 60.00),
        ("1000 Mbps Plan", "Amazon $200 gift card", 70.00),
        ("1200 Mbps Plan", "4K streaming on all devices", 80.00)
    ],
    'Mobile': [
        ("Unlimited Plan", "30GB data, SD streaming", 40),
        ("Unlimited Plus Plan", "50GB data, HD streaming", 50),
        ("By the Gig Plan", "Pay per GB used", 20)
    ],
    'TV': [
        ("Choice TV", "10+ channels", 51.15),
        ("Sports & News TV", "50+ sports channels", 70),
        ("Popular TV", "125+ channels", 83.05),
        ("Ultimate TV", "185+ channels", 112.75)
    ],
    'Home Phone': [
        ("Xfinity Voice Premier", "90+ countries calling", 30),
        ("Basic Calling", "Essential features", 15)
    ],
    'Home Security': [
        ("Self Protection Plan", "No contract", 10),
        ("Xfinity Home Security", "24/7 monitoring", 45),
        ("Ultimate Home System", "Full security setup", 60)
    ]
}

COMPETITOR_PRICES = {
    'Internet': [("Xfinity", 30), ("AT&T", 85), ("Verizon", 90), ("Spectrum", 80)],
    'Mobile': [("Xfinity", 40), ("T-Mobile", 55), ("Verizon", 60), ("AT&T", 65)],
    'TV': [("Xfinity", 30), ("DirecTV", 90), ("Dish", 88), ("FuboTV", 85)],
    'Home Security': [("Xfinity", 10), ("ADT", 60), ("Ring", 55), ("Vivint", 70)]
}

SERVICES = list(OPTIONS.keys())

if st.session_state.current_step == 1:
    col1, col2 = st.columns([3, 2])
    
    with col1:
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

    with col2:
        st.subheader("Or chat with an assistant")
        
        # Display chat history
        for msg in st.session_state.chat_messages[1:]:  # Skip system message
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"], unsafe_allow_html=True)

        if prompt := st.chat_input("Ask about Xfinity plans..."):
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    full_response = ""
                    message_placeholder = st.empty()
                    
                    # Generate streaming response
                    for response in openai.ChatCompletion.create(
                        model="gpt-4o",
                        messages=st.session_state.chat_messages,
                        stream=True,
                        temperature=0.7,
                        max_tokens=500
                    ):
                        chunk = response.choices[0].delta.get("content", "")
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                    st.session_state.chat_messages.append({"role": "assistant", "content": full_response})
                
                except Exception as e:
                    st.error(f"Error communicating with AI: {str(e)}")

elif st.session_state.current_step > 1 and st.session_state.current_step <= len(st.session_state.selected_services) + 1:
    service = st.session_state.selected_services[st.session_state.current_step - 2]
    st.subheader(f'Choose your {service} plan')
    for option, desc, price in OPTIONS[service]:
        normalized_key = service.replace(' ', '_').lower()
        if st.button(
            f"**{option}**  \n{desc} - ${price}/mo",
            key=f"{service}-{option}",
            use_container_width=True,
            type="primary" if st.session_state.get(normalized_key) == option else "secondary"
        ):
            st.session_state[normalized_key] = option
            st.session_state[f"{normalized_key}_price"] = price
            st.session_state.current_step += 1
            st.rerun()

elif st.session_state.current_step > len(st.session_state.selected_services) + 1:
    st.subheader('Your Recommended Plan')
    total = 0
    for service in st.session_state.selected_services:
        normalized_key = service.replace(' ', '_').lower()
        selected_plan = st.session_state.get(normalized_key)
        selected_price = st.session_state.get(f"{normalized_key}_price", 0)
        total += selected_price
        
        st.markdown(f"### {service}: {selected_plan}")
        st.markdown(f"**${selected_price}/month**")
        if service in PURCHASE_LINKS:
            st.link_button(
                f"Purchase {service}",
                PURCHASE_LINKS[service],
                use_container_width=True
            )

        competitor_data = COMPETITOR_PRICES.get(service, [])
        df = pd.DataFrame(competitor_data, columns=['Provider', 'Price'])
        fig = px.bar(df, x='Provider', y='Price', 
                     title=f"{service} Price Comparison",
                     color='Provider',
                     color_discrete_map={'Xfinity': '#0044ff'})
        st.plotly_chart(fig)
    
    st.markdown(f"## Total Monthly Cost: ${total:.2f}")
    
    if st.button('Start Over'):
        st.session_state.clear()
        st.rerun()

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)