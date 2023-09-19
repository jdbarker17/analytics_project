## Youtube Analytics File
# Author: Jon Barker
# Date: 9/11/2023

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

## Get all channel videos for a designated channel ID
# INPUT: channel_id
# OUTPUT: Array of video_ids for a designated channel_ID, currently limited to 60
def get_channel_videos(channel_id,creds):
    youtube = build('youtube', 'v3', credentials=creds)
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=60,
        type="video"
    )
    response = request.execute()

    video_details = []
    
    for item in response['items']:
        video_title = item['snippet']['title']
        video_id = item['id']['videoId']
        video_details.append([video_id,video_title])
    
    
    return video_details

# Code to authenticate via OAUTH2
def authenticate_OAUTH2():
    # Load client secrets
    # Desktop PC
    client_secrets_path = 'client_secret_534787313401-a3pac8r6quq2khmchdhvrbpsfdcqhc3a.apps.googleusercontent.com.json'
    # Mac
    #client_secrets_path = 'client_secret_534787313401-id0vari9sbmphcke6h0lg0n5o8rhm3om.apps.googleusercontent.com.json'
    scopes = ['https://www.googleapis.com/auth/yt-analytics.readonly', 'https://www.googleapis.com/auth/youtube.readonly']

    # Authenticate and get credentials
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, scopes)
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


#Code to convert a json_respone from the API call to a dataframe
def convert_to_df(video_id,json_response):
    column_headers = [header['name'] for header in json_response['columnHeaders']]
    rows = json_response['rows']
    df = pd.DataFrame(rows, columns=column_headers)
    df['video_id'] = video_id[0]
    df['title'] = video_id[1]
    #Compute Rolling Sum per video:
    df['rolling_sum'] = df['views'].cumsum()

    df = df[['video_id','title','day','views','rolling_sum','likes','dislikes','comments']]
    return df


#Code to aggregate two dataframes together
def aggregate_df(df1,df2):
    aggregated_df = pd.concat([df1,df2], ignore_index=True)
    return aggregated_df


# Method to make the video data call.
def get_all_video_data(creds):
    # Build the YouTube Analytics API client
    youtube_analytics = build('youtubeAnalytics', 'v2', credentials=creds)

    # Get the channel ID
    youtube = build('youtube', 'v3', credentials=creds)
    #channel_response = youtube.channels().list(part='id', mine=True).execute()

    #Code to retreive all videos from a given channel
    try:
        channel_response = youtube.channels().list(part='id', mine=True).execute()
        channel_id = channel_response['items'][0]['id']
        videos = get_channel_videos(channel_id,creds)
        video_ids = videos[0:15]
        print(f"Channel Id = {channel_id}")
        print(f"Video ID = {video_ids}")

        #Each video makes an API call to retreive data for a given timeframe. Data is then aggregated into one rolling dataframe
        rolling_df = pd.DataFrame()
        for video_id in video_ids:
            print(f"Channel Id = {channel_id}")
            print(f"Video ID = {video_id[0]}")
            
            # Make an API request to YouTube Analytics
            response = youtube_analytics.reports().query(
                ids='channel=={}'.format(channel_id),
                startDate='2023-01-01',
                endDate='2023-08-31',
                metrics='views,likes,dislikes,comments',
                dimensions='day',
                sort='day',
                filters = f'video=={video_id[0]}'
            ).execute()

            rolling_df = aggregate_df(rolling_df,convert_to_df(video_id, response))

    except HttpError as e:
        print(e.content) 

    return rolling_df,video_ids 
    
    

