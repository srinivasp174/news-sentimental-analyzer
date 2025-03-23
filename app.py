import streamlit as st
import requests
import os

# Set up Streamlit page
st.set_page_config(page_title="News Sentiment Analysis", layout="wide")

st.title("📰 News Sentiment & Summarization")

# Detect if running on Hugging Face Spaces
BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:7860")  # Default to local

# User input for company name
company = st.text_input("Enter the company name:", "")

if st.button("Fetch News"):
    if company:
        api_url = f"{BASE_URL}/news?company={company}"  # Use correct API URL

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                news_data = response.json()

                # Display Average Sentiment Score
                avg_sentiment = news_data.get("average_sentiment", "N/A")
                st.subheader(f"📊 Average Sentiment Score: {avg_sentiment}")

                articles = news_data["articles"]
                
                if not articles:
                    st.warning("⚠️ No articles found for this company.")
                else:
                    # Loop through each article and display info
                    for article in articles:
                        st.subheader(article["title"])
                        st.write(f"🔗 [Read more]({article['link']})")
                        st.write(f"📝 **Summary:** {article['summary']}")
                        st.write(f"📊 **Sentiment Score:** {article['sentiment_score']} / 5")
                        st.write(f"🗣️ **Sentiment Label:** {article['sentiment_label']}")

                        # Play Hindi TTS audio
                        st.audio(f"{BASE_URL}{article['audio']}", format="audio/mp3")

            else:
                st.error("⚠️ Failed to fetch news articles.")

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Backend is not reachable! Check if Flask is running.")
    else:
        st.warning("⚠️ Please enter a company name.")
