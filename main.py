from flask import Flask, render_template, url_for, redirect
from forms import ContactForm
from google.cloud import datastore

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")
print(f'ENV is set to: {app.config["ENV"]}')

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
    response.headers['Permissions-Policy']='geolocation=(), microphone=()'
    response.headers['X-xss-protection']='1; mode=block; report=https://jpoirierlavoie.report-uri.com/r/d/xss/enforce'
    response.headers['Strict-Transport-Security']='max-age=31536000; includeSubDomains; preload'
    response.headers['Expect-CT']='max-age=31536000, enforce, report-uri=\"https://jpoirierlavoie.report-uri.com/r/d/ct/enforce\"'
    response.headers['Report-To']='{"group":"default","max_age":31536000,"endpoints":[{"url":"https://jpoirierlavoie.report-uri.com/a/d/g"}],"include_subdomains":true}'
    response.headers['NEL']='{"report_to":"default","max_age":31536000,"include_subdomains":true}'
    response.headers['Content-Security-Policy']='default-src \'none\'; frame-src \'self\' www.google.com; connect-src \'self\' www.gstatic.com www.google.com stats.g.doubleclick.net www.google-analytics.com northamerica-northeast1-jpoirierlavoie-ca.cloudfunctions.net www.googletagmanager.com; img-src www.google-analytics.com www.google.ca www.google.com \'self\'; script-src-elem \'unsafe-inline\' www.gstatic.com www.google.com www.google-analytics.com www.googletagmanager.com \'self\'; style-src-elem \'unsafe-inline\' \'self\'; font-src \'self\'; manifest-src \'self\'; worker-src \'self\'; report-uri https://jpoirierlavoie.report-uri.com/r/d/csp/enforce'
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    posts = fetch_posts()
    form = ContactForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('home.html', posts=posts, form=form)

@app.route('/blog')
def blog():
    posts = fetch_posts()
    return render_template('post.html', posts=posts)

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
