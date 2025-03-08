from flask import Flask, redirect, url_for, session
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'random_secret_key'
app.config['GOOGLE_ID'] = 'your_google_client_id'
app.config['GOOGLE_SECRET'] = 'your_google_client_secret'

oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=app.config['GOOGLE_ID'],
    consumer_secret=app.config['GOOGLE_SECRET'],
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/')
def index():
    if 'google_token' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token')
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (response['access_token'], '')
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run(debug=True)
