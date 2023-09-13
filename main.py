from youtube_analytics import  *
import pandas as pd


def main():
    creds = authenticate_OAUTH2()
    df = get_all_video_data(creds)
    df.to_excel('output.xlsx')



if __name__ ==  "__main__":
    main()