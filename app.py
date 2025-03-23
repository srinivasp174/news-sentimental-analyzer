import streamlit as st
import requests

# ✅ Set up Streamlit page
st.set_page_config(page_title="News Sentiment Analysis", layout="wide")

st.title("📰 News Sentiment & Summarization")

# ✅ User input for company name
company = st.text_input("Enter the company name:", "")

if st.button("Fetch News"):
    if company:
        api_url = f"http://127.0.0.1:5000/news?company={company}"  # ✅ Call Flask API

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                news_data = response.json()

                # ✅ Display Average Sentiment Score
                avg_sentiment = news_data.get("average_sentiment", "N/A")
                st.subheader(f"📊 Average Sentiment Score: {avg_sentiment}")

                articles = news_data["articles"]
                
                if not articles:
                    st.warning("⚠️ No articles found for this company.")
                else:
                    # ✅ Loop through each article and display info
                    for article in articles:
                        st.subheader(article["title"])
                        st.write(f"🔗 [Read more]({article['link']})")
                        st.write(f"📝 **Summary:** {article['summary']}")
                        st.write(f"📊 **Sentiment Score:** {article['sentiment_score']} / 5")
                        st.write(f"🗣️ **Sentiment Label:** {article['sentiment_label']}")

                        # ✅ Play Hindi TTS audio
                        st.audio(f"http://127.0.0.1:5000{article['audio']}", format="audio/mp3")

            else:
                st.error("⚠️ Failed to fetch news articles.")

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Flask backend is not running! Start it using `python api.py`.")
    else:
        st.warning("⚠️ Please enter a company name.")
