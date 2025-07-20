from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

mock_db = []
next_id = 1
last_search_results = []

@app.route("/")
def home():
    return render_template("index.html")

# More routes will be added later
if __name__ == "__main__":
    app.run(debug=True)
