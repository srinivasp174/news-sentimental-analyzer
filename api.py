from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from utils import get_news_articles, extract_article_details, sentiment_score, text_to_speech

# Initialize Flask App
app = Flask(__name__, static_folder="static")
CORS(app)  # Enable CORS for frontend-backend communication

# Serve MP3 files from the static folder
@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

# Fetch News and Process Sentiment & Summarization
@app.route("/news", methods=["GET"])
def fetch_news():
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    articles = get_news_articles(company)
    if not articles:
        return jsonify({"error": "No news articles found"}), 404

    processed_articles = []
    total_sentiment = 0
    valid_articles_count = 0

    for index, article in enumerate(articles):
        full_text, summary = extract_article_details(article["link"])

        if not full_text or not summary:
            continue  

        sentiment, sentiment_label = sentiment_score(summary)
        if sentiment is None:
            continue  

        # Generate and store TTS file in static/
        tts_filename = f"news_summary_{index+1}.mp3"
        mp3_path = text_to_speech(summary, tts_filename)

        processed_articles.append({
            "title": article["title"],
            "link": article["link"],
            "summary": summary,
            "sentiment_score": sentiment,
            "sentiment_label": sentiment_label,
            "audio": f"/static/{tts_filename}"  # Correct MP3 path
        })

        total_sentiment += sentiment
        valid_articles_count += 1  

    avg_sentiment = round(total_sentiment / valid_articles_count, 2) if valid_articles_count > 0 else None

    return jsonify({
        "average_sentiment": avg_sentiment,
        "articles": processed_articles
    })

# Run Flask App (Ensuring Docker Compatibility)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)  