from flask import Flask, request, redirect, session
import secret
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # for session

# Your Facebook App credentials
#Updates so secret is in separate files
CLIENT_ID = secret.FB_CLIENT_ID
CLIENT_SECRET = secret.FB_CLIENT_SECRET
REDIRECT_URI = 'http://localhost:5000/callback'

@app.route('/')
def index():
    # Redirect the user to Facebook's OAuth page for Instagram permissions
    return redirect(f'https://www.facebook.com/v12.0/dialog/oauth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=instagram_basic,instagram_manage_insights')

@app.route('/callback')
def callback():
    # Facebook redirects with an authorization code
    code = request.args.get('code')
    
    # Exchange the code for an access token
    token_url = f'https://graph.facebook.com/v12.0/oauth/access_token?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&client_secret={CLIENT_SECRET}&code={code}'
    response = requests.get(token_url)
    data = response.json()
    access_token = data['access_token']
    session['access_token'] = access_token
    
    return f'Logged in with access token: {access_token}'

# Add additional routes to make API calls for Instagram data using the access token

if __name__ == '__main__':
    app.run(debug=True)
