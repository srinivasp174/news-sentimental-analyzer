# MUST be the first Streamlit command
import streamlit as st
st.set_page_config(page_title="News Sentiment Analysis", layout="wide")

# Import utilities from utils.py
from utils import (
    get_news_articles,
    extract_article_details,
    sentiment_score,
    text_to_speech,
    SENTIMENT_LABELS
)
import os
import time

# Main App UI
st.title("📰 News Sentiment & Summarization")

# Debugging Section
debug_expander = st.expander("Debug Options")
with debug_expander:
    debug_mode = st.checkbox("Enable debug mode", False)
    if debug_mode:
        st.warning("Debug mode enabled - check console for detailed logs")

# Company Input
company = st.text_input("Enter the company name:", "")
process_button = st.button("Fetch News")

if process_button and company:
    with st.spinner("Fetching and analyzing news articles..."):
        try:
            # Get articles using your original function
            articles = get_news_articles(company)
            
            if not articles:
                st.warning("⚠️ No news articles found for this company.")
            else:
                processed_articles = []
                total_sentiment = 0
                valid_articles_count = 0

                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for index, article in enumerate(articles):
                    status_text.text(f"Processing article {index+1}/{len(articles)}")
                    progress_bar.progress((index + 1) / len(articles))
                    
                    # Use your original processing functions
                    full_text, summary = extract_article_details(article["link"])
                    if not full_text or not summary:
                        continue

                    sentiment, sentiment_label = sentiment_score(summary)
                    if sentiment is None:
                        continue

                    # Generate audio using your original function
                    tts_filename = f"news_summary_{index+1}.mp3"
                    mp3_path = text_to_speech(summary, tts_filename)

                    processed_articles.append({
                        "title": article["title"],
                        "link": article["link"],
                        "summary": summary,
                        "sentiment_score": sentiment,
                        "sentiment_label": sentiment_label,
                        "audio": mp3_path
                    })

                    total_sentiment += sentiment
                    valid_articles_count += 1

                # Display results
                if valid_articles_count > 0:
                    avg_sentiment = round(total_sentiment / valid_articles_count, 2)
                    st.subheader(f"📊 Average Sentiment: {avg_sentiment}/5")
                    
                    for article in processed_articles:
                        with st.expander(article["title"]):
                            st.write(f"🔗 [Read article]({article['link']})")
                            st.write(f"📝 **Summary:** {article['summary']}")
                            st.write(f"📊 **Sentiment:** {article['sentiment_score']}/5 ({article['sentiment_label']})")
                            
                            if article["audio"] and os.path.exists(article["audio"]):
                                st.audio(article["audio"], format="audio/mp3")
                            else:
                                st.warning("Audio generation failed")
                else:
                    st.warning("No valid articles could be processed")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            if debug_mode:
                st.exception(e)
                st.code(f"Current directory: {os.getcwd()}")
                st.code(f"Static files: {os.listdir('static' if os.path.exists('static') else '.')}")

elif process_button and not company:
    st.warning("⚠️ Please enter a company name.")