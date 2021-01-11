import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import numpy as np
import os
import pandas
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MaxNLocator

fontP = FontProperties()
fontP.set_size('xx-small')
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.pyplot.title(r'ABC123 vs $\mathrm{ABC123}^{123}$')
figsize = (16,8)

def parse_args():
    import argparse
    parser = argparse.ArgumentParser() 
    # parser.add_argument("--models", type=str, help="Choose model to run", required=True)
    parser.add_argument("--models", nargs="+", default=["base"])

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    models = args.models
    
    for model in models:
        folderpath = 'data/{}/c19s.results.summary.tsv'.format(model)
        df = pandas.read_csv(folderpath, sep = '\t')
        parameters = ['susceptible', 'severe', 'exposed', 'ICU','infectious', 'weeklyFatality']

        with plt.style.context('fivethirtyeight'):
            fig, ax = plt.subplots(figsize = figsize)
            x = df['time']
            for i in parameters:
                y = df[i + ' (total) median']
                y1 = df[i + ' (total) upper bound']
                y2 = df[i + ' (total) lower bound']
                ax.set_yscale('log')
                ax.fill_between(x,y2,y1,interpolate=True, alpha = 0.3)
                ax.plot(x, y, label = str(i))
                ax.xaxis.set_major_locator(MaxNLocator(nbins = 12))
                ax.yaxis.set_label_text('Number of people (log scale)', fontsize=14)
                ax.set_title('Trajectories of all compartments', fontsize=18)

            # Shrink current axis's height by 10% on the bottom
            box = ax.get_position()
            ax.set_position([box.x0, box.y0 + box.height * 0.1,
                            box.width, box.height * 0.9])

            # Put a legend below current axis
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                    fancybox=True, shadow=True, ncol=5)
            fig.savefig('plots/{}_trajectories.png'.format(model), dpi=300) #save the figure

        x1 = df['cumulative recovered (total) median'].values
        x2 = df['cumulative hospitalized (total) median'].values
        x3 = df['cumulative ICU (total) median'].values
        x4 = df[ 'cumulative fatality (total) median'].values


        # Exclude mild cases to check strain on the healthcare system

        with plt.style.context('fivethirtyeight'):
            fig, ax = plt.subplots(figsize = (10,8))
            labels = ['Severe: ' + f"{x2[-1]:,}"  , 'Critical: ' + f"{x3[-1]:,}", 'Fatal: ' + f"{x4[-1]:,}"]
            sizes = [x2[-1], x3[-1], x4[-1]]
            ax.pie(sizes, shadow=False, startangle=90, autopct='%1.1f%%', explode = (0.1, 0, 0))
            ax.legend(labels, loc="best")
            ax.axis('equal')
            ax.set_title('Summary of outcomes excluding mild cases', fontsize=18)

            fig.savefig('plots/{}_piechart.png'.format(model), dpi=300) #save the figure





