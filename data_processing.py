import matplotlib.pyplot as plt
import numpy as np
import math


def visualize(df, video_ids):
    # Calculate number of rows and columns for the grid
    n = len(video_ids)
    rows = int(math.sqrt(n))
    cols = int(math.ceil(n / rows))
    
    fig, axs = plt.subplots(rows, cols, figsize=(15, 15))
    
    # Check if we have a single row or column
    if rows == 1 or cols == 1:
        axs = np.reshape(axs, (-1, ))
    
    #Ticks to set Lower Axis
    ticks = np.array([15, 45, 73, 104, 134, 165, 195, 226])
    labels = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'Aug']
    print(f"Video IDs = {video_ids}")
    
    for idx, (video_id, video_title) in enumerate(video_ids):
        subset = df[df['video_id'] == video_id]
        row = idx // cols
        col = idx % cols
        
        axs[row, col].plot(subset['views'])
        axs[row, col].set_title(f"Video_Title: {video_title}")
        axs[row, col].set_xticks(ticks, minor=False)
        axs[row, col].set_xticklabels(labels, fontdict=None, minor=False)
        
        # Update ticks for the next plot
        ticks = ticks + 243
        
    # Remove any unused subplots
    for i in range(idx + 1, rows * cols):
        row = i // cols
        col = i % cols
        fig.delaxes(axs[row, col])
    
    plt.tight_layout()
    plt.show()
