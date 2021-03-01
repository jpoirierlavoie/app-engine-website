from flask import Flask, render_template, make_response
from google.cloud import datastore

app = Flask(__name__)

datastore_client = datastore.Client()

def fetch_posts():
    query = datastore_client.query(kind="posts")
    posts = query.fetch()
    return posts

@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options']='DENY'
    response.headers['X-content-type-options']='nosniff'
    response.headers['Referrer-Policy']='no-referrer'
    response.headers['X-xss-protection']='1; mode=block; report=https://jpoirierlavoie.report-uri.com/r/d/xss/enforce'
    response.headers['Strict-Transport-Security']='max-age=31536000; includeSubDomains; preload'
    response.headers['Expect-CT']='max-age=31536000, enforce, report-uri=\"https://jpoirierlavoie.report-uri.com/r/d/ct/enforce\"'a
    return response

@app.route('/')
def index():
    posts = fetch_posts()
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
    app.run(host='127.0.0.1', port=5000, debug=True)
