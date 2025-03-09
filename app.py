import openai
from flask import Flask, redirect, url_for, session, request, render_template, jsonify
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'

openai.api_key = os.getenv('OPENAI_API_KEY')

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/login/authorized')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
    user_info = resp.json()
    session['user'] = user_info
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if user:
        return render_template('index.html', user=user)
    return redirect(url_for('login'))

@app.route('/add_components')
def add_components():
    return render_template('add_components.html')

@app.route('/submit_data', methods=['POST'])
def submit_data():
    data = request.json
    components = data.get('components', [])
    timetables = data.get('timetables', [])
    consumptions = data.get('consumptions', [])
    
    # Create a prompt for GPT-3
    prompt = "Predict the weekly energy consumption and provide suggestions based on the following data:\n\nComponents:\n"
    for component in components:
        prompt += f"- {component['type']} in {component['location']}: {component['description']}\n"
    
    prompt += "\nTimetables:\n"
    for timetable in timetables:
        prompt += f"- {timetable['classroom']} from {timetable['timeSlot']} for {timetable['className']}\n"
    
    prompt += "\nConsumptions:\n"
    for consumption in consumptions:
        prompt += f"- {consumption['department']} on {consumption['date']}: {consumption['energyConsumption']} kWh\n"
    
    print('Prompt:', prompt)
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300
    )
    
    predictions = response.choices[0].text.strip()
    print('Predictions and Suggestions:', predictions)
    return jsonify({"predictions": predictions, "suggestions": predictions})

if __name__ == '__main__':
    app.run(debug=True)