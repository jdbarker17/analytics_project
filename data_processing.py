import matplotlib.pyplot as plt

def visualize(df,video_ids):
    for id in video_ids:
        subset = df[df['video_id'] == id]
        plt.figure()
        plt.plot(subset['views'])
        plt.show()