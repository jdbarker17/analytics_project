from youtube_analytics import  *
import pandas as pd

def main():
    creds = authenticate_OAUTH2()
    output_dataframe = get_all_video_data(creds)
    output_dataframe.to_excel('output.xlsx')

    #Processing Goes Below. Data Processing, Database management, Optimizations probably down the road.

if __name__ ==  "__main__":
    main()