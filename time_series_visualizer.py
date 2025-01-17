import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
from matplotlib import dates as mpl_dates
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',parse_dates=True,index_col=0)
df.index=pd.to_datetime(df.index)

# Clean data
df = df[(df['value']>=df['value'].quantile(0.025))&(df['value']<=df['value'].quantile(0.975))]
#df[df['value']<=df['value'].quantile(0.025)].index)


def draw_line_plot():
    # Draw line plot
    plt.figure(figsize=(10,6))
    fig=sns.lineplot(data=df, x=df.index.values, y='value')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    fig=fig.figure


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Year']=pd.DatetimeIndex(df_bar.index).year
    df_bar['Month']=pd.DatetimeIndex(df_bar.index).month_name()
    month_organize = ['January', 'February', 'March', 'April', 'May', 
                 'June', 'July', 'August', 'September', 'October', 
                 'November', 'December']
    df_bar['Month'] = pd.Categorical(df_bar['Month'], categories=month_organize, ordered=True)
    df_bar['Month']=df_bar['Month'].sort_values()
    df_bar['Month'] = pd.Categorical(df_bar['Month'],ordered=True)
    df_bar=df_bar.groupby(['Year','Month']).mean()
    df_bar=df_bar.dropna()
    df_bar = df_bar.unstack()
    # Draw bar plot
    plt.figure(figsize=(9,6))
    fig = df_bar.plot(kind ="bar", figsize=(9,6)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(labels=month_organize,title='Month')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes=plt.subplots(nrows=1,ncols=2,figsize=(11,6))
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[0].set_title('Year-wise Box Plot (Trend)')
    sns.boxplot(data=df_box,x='year', y='value', palette='bright',ax=axes[0])
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    sns.boxplot(data=df_box,x='month', y='value', palette='bright',order=['Jan','Feb','Mar','Apr','May',
                                                                               'Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
                                                                               ax=axes[1])
    plt.tight_layout(pad=2)
    fig=fig.figure

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
