from flask import Flask, render_template, request
from transformers import pipeline
import nltk
from collections import Counter
import re

# Download NLTK stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords

app = Flask(__name__)

# Load Hugging Face pipelines (first run may take time to download models)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analyzer = pipeline("sentiment-analysis")

def extract_keywords(text, num_keywords=5):
    # Basic keyword extraction (bag of words + frequency count + TF-IDF)
    words = re.findall(r'\w+', text.lower())
    filtered_words = [w for w in words if w not in stopwords.words('english')]
    common = Counter(filtered_words).most_common(num_keywords)
    return [word for word, freq in common]

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    if request.method == "POST":
        user_text = request.form["user_text"]

        # Summarisation
        summary = summarizer(user_text, max_length=100, min_length=25, do_sample=False)
        result["summary"] = summary[0]['summary_text']

        # Sentiment
        sentiment = sentiment_analyzer(user_text)
        result["sentiment"] = sentiment[0]['label']

        # Keywords
        result["keywords"] = extract_keywords(user_text)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
