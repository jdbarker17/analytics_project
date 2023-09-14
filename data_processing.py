import matplotlib as plt

def visualize(df):
    plt.pyplot.figure()
    df['views'].plot()