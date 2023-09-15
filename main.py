from youtube_analytics import  *
from data_processing import *
import pandas as pd
import numpy as np


def main():
    creds = authenticate_OAUTH2()
    output_dataframe, video_ids = get_all_video_data(creds)
    output_dataframe.to_excel('output1.xlsx')
    #np.savetxt("video_ids.txt",np.array(video_ids))
    #video_ids = ['UC0bbHtdraI','l9-rnk5Hkq0']
    #output_dataframe = pd.read_excel('output.xlsx')
    visualize(output_dataframe,video_ids)

    #Processing Goes Below. Data Processing, Database management, Optimizations probably down the road.

if __name__ ==  "__main__":
    main()