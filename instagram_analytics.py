# Code to authenticate and pull analytics from a users instagram
# FB account must be linked to instagram
# Author: Jon Barker
# Date 9-23-23

from flask import Flask, request, redirect, session
import secret
import requests
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # for session

# Your Facebook App credentials
# Updates so secret is in separate files
# Secret Modified to Integrate with Analytics App 2 - Functioning verification and ready for API usage.
#Additional Understanding of FB Security, non functioning STILL


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
    print(f'Logged in with access token: {access_token}')

    return redirect('/get_instagram_id')
    #return f'Logged in with access token: {access_token}'

# Add additional routes to make API calls for Instagram data using the access token

@app.route('/get_instagram_id')
def get_instagram_id():
    access_token = session.get('access_token')
    print(f'Access Token = {access_token}')
    if not access_token:
        return "Access token not found. Please authenticate first."

    # Fetch the User's Pages
    pages_url = f'https://graph.facebook.com/v12.0/me/accounts?access_token={access_token}'
    response = requests.get(pages_url)
    data = response.json()
    print(json.dumps(data))

    if 'data' in data:
        debug_info = []  # List to store debug information
        for page in data['data']:
            page_id = page['id']
            page_access_token = page['access_token']

            # For each Page, try to fetch the associated Instagram account ID
            instagram_url = f'https://graph.facebook.com/v12.0/{page_id}?fields=instagram_business_account&access_token={page_access_token}'
            insta_response = requests.get(instagram_url)
            insta_data = insta_response.json()

            debug_info.append(insta_data)  # Append the response to debug info

            if 'instagram_business_account' in insta_data:
                instagram_id = insta_data['instagram_business_account']['id']
                return f'Instagram Creator Account ID: {instagram_id}'
                #return instagram_id
                #return redirect('/get_instagram_data')

        # Return the debug information for inspection
        return f"No associated Instagram Creator Account found. Debug Info: {debug_info}"
    else:
        error_message = data.get('error', {}).get('message', 'Unknown error.')
        return f"Error fetching User's Pages: {error_message}"
    
    

@app.route('/get_instagram_data')
def get_instagram_data():
    access_token = session.get('access_token')
    if not access_token:
        return "Access token not found. Please authenticate first."

    # Fetch the Instagram Business Account ID
    #me_url = f'https://graph.facebook.com/v12.0/me?fields=instagram_business_account&access_token={access_token}'
    #response = requests.get(me_url)
    #data = response.json()
    #print(json.dumps(data))
    #instagram_id = data['instagram_business_account']['id']
    instagram_id = get_instagram_id()
    # Fetch recent media objects from the Instagram Business Account
    media_url = f'https://graph.facebook.com/v12.0/{instagram_id}/media?access_token={access_token}'
    media_response = requests.get(media_url)
    media_data = media_response.json()

    return media_data

# ... [Your existing code to run the app]


if __name__ == '__main__':
    app.run(debug=True)
