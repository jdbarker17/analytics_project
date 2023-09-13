## Youtube Analytics File
# Author: Jon Barker
# Date: 9/11/2023

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

## Get all channel videos for a designated channel ID
# INPUT: channel_id
# OUTPUT: Array of video_ids for a designated channel_ID, currently limited to 50

def get_channel_videos(channel_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50,
        type="video"
    )
    response = request.execute()

    output = []
    for item in response['items']:
        video_title = item['snippet']['title']
        video_id = item['id']['videoId']
        #video_data = get_video_data(video_id)
        #print_video_details(video_data)
        print(f"Title: {video_title}, Video ID: {video_id}")
        output.append(video_id)
    
    return output