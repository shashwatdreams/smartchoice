import streamlit as st
import pandas as pd
import spacy
import matplotlib.pyplot as plt

# spacy model
nlp = spacy.load("en_core_web_sm")

# xfinity data
data = {
    "Category": [
        "Internet", "Internet", "Internet", "Internet", "Internet",
        "Mobile", "Mobile", "Mobile",
        "TV", "TV", "TV", "TV",
        "Home Phone",
        "Home Security", "Home Security"
    ],
    "Plan": [
        "150 Mbps Plan", "300 Mbps Plan", "500 Mbps Plan", "1000 Mbps Plan", "1200 Mbps Plan",
        "Unlimited Plan", "Unlimited Plus Plan", "By the Gig Plan",
        "Choice TV", "Sports & News TV", "Popular TV", "Ultimate TV",
        "Xfinity Voice Premier",
        "Self Protection Plan", "Xfinity Home Security Plan"
    ],
    "Price (Per Month)": [
        19.99, 25.00, 60.00, 70.00, 80.00,
        40.00, 50.00, 20.00,
        51.15, 70.00, 83.05, 112.75,
        30.00,
        10.00, 45.00
    ],
    "Features": [
        "Browsing, streaming music & movies", "Downloading, HD streaming",
        "Quick downloads, remote work", "Large file downloads, ultra-low lag, Amazon Gift Card",
        "4K streaming, unlimited data, Amazon Gift Card",
        "30GB premium data, unlimited talk & text", "50GB premium data, HD video, 15GB 5G hotspot",
        "Pay-per-GB shared data, 4G/5G speeds",
        "10+ channels, basic networks", "50+ channels, live sports, news, Peacock, 300h DVR",
        "125+ channels, diverse content", "185+ channels, movies, sports, entertainment",
        "Unlimited nationwide & international calling",
        "Live & recorded video access, no contract", "24/7 professional monitoring, smart home integration"
    ]
}

df = pd.DataFrame(data)


st.set_page_config(page_title='Xfinity AI-Powered Recommender', layout='wide')
st.title('Xfinity AI-Powered Personalized Recommendation System')

def extract_requirements(user_input):
    doc = nlp(user_input.lower())
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ"]]
    return keywords

def recommend_plans(user_input, df):
    extracted_keywords = extract_requirements(user_input)

    relevant_categories = []
    if "internet" in extracted_keywords:
        relevant_categories.append("Internet")
    if "mobile" in extracted_keywords:
        relevant_categories.append("Mobile")
    if "tv" in extracted_keywords:
        relevant_categories.append("TV")
    if "home phone" in extracted_keywords:
        relevant_categories.append("Home Phone")
    if "security" in extracted_keywords:
        relevant_categories.append("Home Security")

    filtered_df = df[df["Category"].isin(relevant_categories)]


    filtered_df = filtered_df.sort_values("Price (Per Month)").reset_index(drop=True)

    return filtered_df

st.subheader("Describe what you need:")
user_input = st.text_area("Enter details (e.g., 'Unlimited Data for Mobile & Cost-effective Internet for 4 devices')")

if st.button("Get Recommendations"):
    recommended_plans = recommend_plans(user_input, df)
    if not recommended_plans.empty:
        st.subheader("Best Plans for You:")
        st.dataframe(recommended_plans)
    else:
        st.warning("No matching plans found. Try refining your input.")
        
def plot_recommendations(df):
    plt.figure(figsize=(8, 5))
    plt.barh(df["Plan"], df["Price (Per Month)"], color='skyblue')
    plt.xlabel("Price ($)")
    plt.ylabel("Plans")
    plt.title("Cost Comparison of Recommended Plans")
    st.pyplot(plt)

if not user_input.strip() == "":
    st.subheader("Price Comparison:")
    plot_recommendations(recommended_plans)
