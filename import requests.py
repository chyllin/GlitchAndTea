import requests
from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# API Key (replace with environment variable for production)
NEWS_API_KEY = "d3c125ec71b140cf897a88a1f1b2f622"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-6">
        <h1 class="text-4xl font-bold mb-6 text-center">📰 My News Portal</h1>
        <form method="get" class="mb-8 grid grid-cols-1 sm:grid-cols-3 gap-4">
            <input name="query" type="text" placeholder="Search news..." value="{{ query }}"
                   class="p-3 border border-gray-300 rounded w-full">
            <select name="category" class="p-3 border border-gray-300 rounded w-full">
                <option value="">All Categories</option>
                <option value="business" {% if category == 'business' %}selected{% endif %}>Business</option>
                <option value="entertainment" {% if category == 'entertainment' %}selected{% endif %}>Entertainment</option>
                <option value="health" {% if category == 'health' %}selected{% endif %}>Health</option>
                <option value="science" {% if category == 'science' %}selected{% endif %}>Science</option>
                <option value="sports" {% if category == 'sports' %}selected{% endif %}>Sports</option>
                <option value="technology" {% if category == 'technology' %}selected{% endif %}>Technology</option>
            </select>
            <button type="submit" class="bg-blue-500 text-white p-3 rounded hover:bg-blue-600">Search</button>
        </form>

        {% if loading %}
            <p class="text-center text-lg">Loading articles...</p>
        {% elif articles %}
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {% for article in articles %}
            <div class="bg-white rounded-lg shadow hover:shadow-lg transition duration-300">
                {% if article.urlToImage %}
                <img src="{{ article.urlToImage }}" alt="thumbnail" loading="lazy"
                     class="w-full h-48 object-cover rounded-t-lg">
                {% endif %}
                <div class="p-4">
                    <h2 class="text-xl font-semibold mb-2">{{ article.title }}</h2>
                    <p class="text-sm text-gray-500 mb-2">{{ article.source.name }}</p>
                    <p class="text-sm text-gray-700 mb-3">{{ article.description }}</p>
                    <a href="{{ article.url }}" target="_blank" rel="noopener noreferrer"
                       class="text-blue-600 hover:underline text-sm">Read more</a>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <p class="text-center text-lg text-gray-600">No articles found.</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def news_portal():
    query = request.args.get("query", "")
    category = request.args.get("category", "")
    loading = False
    articles = []

    try:
        params = {
            "q": query if query else "world",
            "apiKey": NEWS_API_KEY,
            "country": "us"
        }
        if category:
            params["category"] = category

        response = requests.get("https://newsapi.org/v2/top-headlines", params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
    except requests.exceptions.RequestException as e:
        print("Error fetching news:", e)

    return render_template_string(HTML_TEMPLATE, articles=articles, query=query, category=category, loading=loading)

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
