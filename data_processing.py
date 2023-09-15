import matplotlib.pyplot as plt
import numpy as np

def visualize(df,video_ids):
    fig, axs = plt.subplots(len(video_ids))
    ticks = np.array([15,45,73,104,134,165,195,226])
    labels = ['Jan','Feb','Mar','April','May','June','July','Aug']
    print(f"Video IDs = {video_ids}")
    for id in enumerate(video_ids):
        print(f"Id = {id}")
        subset = df[df['video_id'] == id[1][0]]
        #subset['cumsum'] = subset['views'].cumsum()
        subset.head()
        axs[id[0]].plot(subset['views'])
        #axs[id[0]].plot(subset['views'].cumsum())
        axs[id[0]].set_title(f"Video_Title: {id[1][1]}")
        axs[id[0]].set_xticks(ticks, minor=False)
        axs[id[0]].set_xticklabels(labels, fontdict=None, minor=False)
        ticks = ticks + 241
        #axs[id[0]].xticks(ticks= ticks, labels=labels, **kwargs)
    
    plt.show()