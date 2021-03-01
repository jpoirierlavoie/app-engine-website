import sys
from flask import Flask, render_template, url_for
from google.cloud import datastore

app = Flask(__name__)
app.config.from_object(__name__)

def fetch_posts():
    query = datastore_client.query(kind="posts")
    posts = query.fetch()
    return posts

@app.route('/')
@app.route('/index')
def index():
    posts = fetch_posts
    return render_template('index.html', posts=posts)

@app.route('/manifest.webmanifest')
def manifest():
    return app.send_static_file('manifest.webmanifest'), 200, {'Content-Type': 'application/manifest+json'}

@app.route('/service-worker.js')
def worker():
    return app.send_static_file('service-worker.js'), 200, {'Content-Type': 'text/javascript'}

@app.route('/robots.txt')
def crawler():
    return app.send_static_file('robots.txt'), 200, {}

@app.route('/sitemap.xml')
def sitemap():
    return app.send_static_file('sitemap.xml'), 200, {'Content-Type': 'text/xml; charset=utf-8'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
