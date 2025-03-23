# **📰 News Sentiment Analysis & Summarization**
This project extracts **news articles**, summarizes them, performs **sentiment analysis**, and converts the **summary into Hindi speech** using **text-to-speech (TTS)**. It provides a **Flask API** for backend processing and a **Streamlit UI** for visualization.

## **🚀 Features**
✅ **Fetch latest news articles** for any company using web scraping.  
✅ **Summarize news content** using `facebook/bart-large-cnn`.  
✅ **Perform sentiment analysis** using `nlptown/bert-base-multilingual-uncased-sentiment`.  
✅ **Translate summaries to Hindi** and convert them to speech using `gTTS`.  
✅ **Streamlit frontend** to visualize news summaries and sentiment scores.  
✅ **Flask API** to serve news analysis data.  
✅ **Deployable via Docker** on **Hugging Face Spaces**.

---

## **📂 Project Structure**
```
📦 sentiment-analysis
├── 📜 README.md               # Project Documentation
├── 📜 requirements.txt        # Python dependencies
├── 📜 Dockerfile              # Deployment configuration
├── 🗂️ static/                # Stores generated MP3 files
│   ├── news_summary_1.mp3
│   ├── news_summary_2.mp3
│   └── ...
├── 📜 api.py                  # Flask backend for processing news
├── 📜 utils.py                # Utility functions (scraping, summarization, TTS)
├── 📜 app.py                  # Streamlit frontend
└── 📜 .gitignore              # Files to ignore in version control
```

---

## **📥 Dependencies**
### **Python Libraries (Install via `requirements.txt`)**
- `torch` – Required for **sentiment analysis model**.
- `requests` – Used for **news web scraping**.
- `beautifulsoup4` – Extracts **news content** from web pages.
- `transformers` – **Hugging Face models** for summarization and sentiment analysis.
- `deep-translator` – Translates summaries to **Hindi**.
- `gtts` – Converts translated text to **Hindi speech (MP3)**.
- `flask` – Backend API for news extraction and analysis.
- `flask-cors` – Handles **CORS issues** for frontend-backend communication.
- `streamlit` – Provides an **interactive UI** for the app.

---

## **⚙️ Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/srinivasp174/news-sentiment-analyzer.git
cd news-sentiment-analyzer
```

### **2️⃣ Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Start the Flask Backend**
```bash
python api.py
```
**Backend API** will be available at **`http://127.0.0.1:5000`**.

### **5️⃣ Start the Streamlit Frontend**
```bash
streamlit run app.py
```
**Frontend UI** will be available at **`http://localhost:8501`**.

---

## **🌐 API Endpoints**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/news?company=<company>` | GET | Fetches latest news articles and returns sentiment & summaries |
| `/static/<filename>` | GET | Serves the generated TTS MP3 files |

### **🔍 Example API Response**
```json
{
    "average_sentiment": 3.8,
    "articles": [
        {
            "title": "Company X Stock Surges Amid Market Rally",
            "link": "https://news.example.com/article1",
            "summary": "Company X saw a major stock increase today following a market-wide rally...",
            "sentiment_score": 4,
            "sentiment_label": "Positive",
            "audio": "/static/news_summary_1.mp3"
        },
        {
            "title": "Company X Faces New Challenges in Supply Chain",
            "link": "https://news.example.com/article2",
            "summary": "Despite recent success, Company X is struggling with supply chain disruptions...",
            "sentiment_score": 2,
            "sentiment_label": "Negative",
            "audio": "/static/news_summary_2.mp3"
        }
    ]
}
```

---

## **📝 Implementation Details**
### **1️⃣ News Extraction (`utils.py`)**
- Uses **Google News search** to fetch recent articles.
- Extracts links and titles using **BeautifulSoup**.
- Ensures at least **10 unique news articles** are returned.

### **2️⃣ News Summarization (`utils.py`)**
- Uses **Hugging Face `facebook/bart-large-cnn`** for text summarization.
- Handles long articles by truncating content to **1024 tokens**.

### **3️⃣ Sentiment Analysis (`utils.py`)**
- Uses **Hugging Face `nlptown/bert-base-multilingual-uncased-sentiment`**.
- Predicts sentiment from **1 (Very Negative) to 5 (Very Positive)**.
- Computes **average sentiment score** across articles.

### **4️⃣ Text-to-Speech & Translation (`utils.py`)**
- **Google Translator API** translates summaries to Hindi.
- **`gTTS` (Google Text-to-Speech)** converts translated text into speech.
- Saves **MP3 files** in the `/static` folder for playback.

### **5️⃣ Flask API (`api.py`)**
- Calls `get_news_articles()` to fetch news.
- Calls `extract_article_details()` to scrape content & summarize.
- Calls `sentiment_score()` to analyze sentiment.
- Calls `text_to_speech()` to generate Hindi audio.

### **6️⃣ Streamlit Frontend (`app.py`)**
- Takes **user input for company name**.
- Calls **Flask API** to fetch news and sentiment.
- Displays:
  - Article **Title & Link**
  - **Summary & Sentiment Score**
  - **Hindi Audio Playback**
- Provides an **interactive user interface**.

---

## **🐳 Docker Deployment (Hugging Face Spaces)**
### **1️⃣ Create `Dockerfile`**
```dockerfile
FROM python:3.9

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user . /app
CMD ["python", "api.py"]
```

### **2️⃣ Build & Run Docker Locally**
```bash
docker build -t sentiment-analysis .
docker run -p 5000:5000 sentiment-analysis
```

### **3️⃣ Push to Hugging Face**
```bash
git push huggingface main
```

---

## **📌 Future Enhancements**
- ✅ **Improve news article scraping** by integrating multiple sources.
- ✅ **Enhance sentiment analysis** with more fine-tuned models.
- ✅ **Deploy using Kubernetes** for better scalability.
- ✅ **Add real-time monitoring** for API performance.

---

## **📜 License**
This project is licensed under the **MIT License**.  

Feel free to contribute! 🚀✨  

---

### **🔗 Project Links**
- **GitHub Repo:** [news-sentiment-analyzer](https://github.com/srinivasp174/news-sentiment-analyzer)
- **Hugging Face Space:** [news-sentiment-analyzer](https://huggingface.co/spaces/srinivasp174/news-sentiment-analyzer)

---

This **README.md** is now **fully detailed**, making it easy for users to **install, use, and contribute**! 🚀
