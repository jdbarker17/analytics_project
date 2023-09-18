import requests

# Get long-lived access token (this lasts for about 60 days)
# NOTE: This requires your app to be in Live mode.
access_token = 'YOUR_ACCESS_TOKEN'

# Get the media objects (photos, videos) of the authenticated user
media_url = f'https://graph.instagram.com/v12.0/me/media?fields=id,caption,media_type,thumbnail_url,media_url,timestamp&access_token={access_token}'
media_response = requests.get(media_url)
media_data = media_response.json()

# For each media item, if it's a video, get its insights
for item in media_data['data']:
    if item['media_type'] == 'VIDEO':
        video_id = item['id']
        insights_url = f'https://graph.instagram.com/v12.0/{video_id}/insights?metric=engagement,impressions,reach,saved,video_views&access_token={access_token}'
        insights_response = requests.get(insights_url)
        insights_data = insights_response.json()
        print(insights_data)
