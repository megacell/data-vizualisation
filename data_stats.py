import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#plt.style.use('ggplot')
import matplotlib
print matplotlib.__version__
#pd.options.display.mpl_style = 'default'

__author__ = 'jeromethai'


def example():
    # create a histogram of randomly generated samples from 
    # a Gaussian distribution 
    n = 10000
    data = zip(np.random.normal(size = n), np.random.normal(size = n))
    df = pd.DataFrame(data, columns = ['c1', 'c2'])
    plt.figure()
    df['c1'].plot(kind='hist', bins=20, alpha=0.7, color='r')
    plt.show()


def visualize_flow():
    # creates histogram to visualize distribution of flow
    df = pd.load('data/OSM_LA.pkl')
    plt.figure()
    df['flow'].plot(kind='hist', bins=20, alpha=0.7, color='r')
    plt.show()


if __name__ == "__main__":
    #example()
    visualize_flow()