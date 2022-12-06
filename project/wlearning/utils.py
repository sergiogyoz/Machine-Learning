import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns


def percentiles(df=pd.DataFrame, label="wl", show = True, plot=True,station_name="", percents=[]):
    """Get 10% percentile distribution and plot it. Percentiles can be provided """
    q10 = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    if percents:
        q10 = percents
    p10 = df[label].quantile(q10)
    if show:
        print(station_name+" percentile distribution of "+label)
        print(p10)
    if plot:
        plt.figure()
        plt.plot(p10,q10)
        plt.title(station_name+" "+label+" distribution")
    return p10

def custom_plot(df=pd.DataFrame, xtag="", ytag="", 
                kind="scatter",legend=None, title="",
                xlabel="time", ylabel="discharge CFS",
                s=1, xsize=8, ysize=2, date_format="",
                label=""):
    """For my repetitive plotting of dfs or series objects"""
    if date_format != "":
        date_form = DateFormatter(date_format)
    l_param={
        "kind" : kind, 
        "title" : title,
        "xlabel" : xlabel,
        "ylabel" : ylabel, 
        "legend" : legend,
        "label" : label
    }
    if type(df)==pd.DataFrame:
        l_param["x"] = xtag
        l_param["y"] = ytag
    else:
        l_param["kind"]="line"
    if l_param["kind"]=="scatter":
        l_param["s"]=s
    print(l_param)
    ax = df.plot(**l_param)
    if date_format != "":
        ax.xaxis.set_major_formatter(date_format)
    plt.gcf().set_size_inches(xsize,ysize)

def cross_corr( df1=pd.DataFrame, df2=pd.DataFrame,
                tag1="", tag2="",
#                start_date, end_date,  # mmm read data?
#                window_size=365,       # should I just use the bounds of the data? 
                shift_range=(-10,10),
                plot = True):
    """
    Cross correlation tool for the project. User is assumed to give dfs 
    with the same (daily time index) timezone
    """

    if df1.index[0].tz != df2.index[0].tz:
        raise(ValueError("time index zone is not the same in both dfs"))

    # get the common range between the time series
    l_date = min(df1.index[0], df2.index[0])
    h_date = max(df1.index[-1], df2.index[-1])

    # for every shift save the cross correlation    
    ccv=[]
    shifts = range(shift_range[0],shift_range[1]+1)
    for i in shifts:
        _df = pd.DataFrame()
        _df["1"] = df1[tag1]
        _df["2"] = df2[tag2].shift(-i)
        ccv.append(_df["1"].corr(_df["2"]))
    
    # plot shift vs cross correlation
    if plot:
        plt.figure()
        plt.scatter(shifts, ccv)
        plt.gca().xaxis.get_major_locator().set_params(integer=True)
        plt.title("Cross correlation function")
        plt.xlabel(f"time lag (days)")
    # save max shift
    maxcv = shifts[np.argmax(ccv)]

    return maxcv, ccv




