import torch
import requests
from bs4 import BeautifulSoup
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import time

# Load sentiment model
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

# Load Hugging Face summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Sentiment Labels
SENTIMENT_LABELS = {
    1: "Very Negative",
    2: "Negative",
    3: "Neutral",
    4: "Positive",
    5: "Very Positive"
}

# Function to compute sentiment score
def sentiment_score(text):
    if not text.strip():
        return None, None  

    tokens = tokenizer.encode(text[:512], return_tensors='pt', truncation=True)
    with torch.no_grad():
        result = model(tokens)

    score = torch.argmax(result.logits).item() + 1  
    truncated_score = round(score, 2)  
    sentiment_label = SENTIMENT_LABELS.get(score, "Unknown")  

    return truncated_score, sentiment_label

# Function to extract news articles (ENSURES at least 10)
def get_news_articles(company):
    search_queries = [f"{company} news", f"latest {company} news", f"{company} breaking news"]
    articles = []
    seen_links = set()
    headers = {'User-Agent': 'Mozilla/5.0'}

    for query in search_queries:
        if len(articles) >= 10:
            break  

        search_url = f'https://www.google.com/search?q={query}&tbm=nws'
        req = requests.get(search_url, headers=headers)
        if req.status_code != 200:
            print(f'Error: Unable to fetch news (Status Code: {req.status_code})')
            continue  

        soup = BeautifulSoup(req.text, 'html.parser')

        for item in soup.find_all('a'):
            link = item.get('href')
            title_tag = item.find('div', class_='BNeawe vvjwJb AP7Wnd')

            if not link or not title_tag:
                continue

            title = title_tag.get_text()
            link = f'https://www.google.com{link}' if link.startswith('/url?') else link

            if link not in seen_links:
                articles.append({'title': title, 'link': link})
                seen_links.add(link)

            if len(articles) >= 10:
                break  

        time.sleep(2)  # Avoid getting blocked by Google

    return articles[:10]  

# Function to extract details from news articles
def extract_article_details(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        req = requests.get(url, headers=headers)
        if req.status_code != 200:
            print(f'Error: Unable to fetch article (Status Code: {req.status_code})')
            return None, None
    except requests.exceptions.RequestException as e:
        print(f'Request for {url} failed: {e}')
        return None, None

    soup = BeautifulSoup(req.text, 'html.parser')
    paragraphs = soup.find_all('p')
    full_text = ' '.join([p.get_text() for p in paragraphs])

    if not full_text or len(full_text) < 50:
        return None, None

    translated_text = translate_text(full_text)  

    try:
        summary = summarizer(translated_text[:1024], max_length=150, min_length=50, do_sample=False)[0]['summary_text']
    except Exception as e:
        print(f'Summarization failed for {url}: {e}')
        return translated_text, translated_text  

    return translated_text, summary

# Function to translate text to English
def translate_text(text):
    if not text:
        return text
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print(f'Translation failed: {e}')
        return text

# Function to Convert Summary to Hindi Speech
STATIC_FOLDER = "static"
os.makedirs(STATIC_FOLDER, exist_ok=True)

def text_to_speech(summary, filename):
    hindi_summary = translate_text_hindi(summary)  
    try:
        filepath = os.path.join(STATIC_FOLDER, filename)
        tts = gTTS(text=hindi_summary, lang='hi')  
        tts.save(filepath)
        print(f"Speech saved as {filename}")
        return filepath
    except Exception as e:
        print(f"TTS failed: {e}")
        return None

# function for Hindi translation
def translate_text_hindi(text):
    if not text:
        return text
    try:
        return GoogleTranslator(source='auto', target='hi').translate(text)  
    except Exception as e:
        print(f'Translation failed: {e}')
        return text