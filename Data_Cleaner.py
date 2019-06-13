import numpy as np
import pandas as pd

MR_filepath = 'Hot_100_Chart_Lyrics.csv'
MR_df = pd.read_csv(MR_filepath)
MR_df.columns = \
    ["Artist", "Song", "Date", "Current Rank", "Last Weeks Position", "Weeks on Chart", "Peak Position", "Lyrics"]

NR_df = pd.DataFrame()


def f(x):
    first_week_index = x["Date"].index.min()
    first_week = x["Date"][first_week_index]
    last_week_index = x["Date"].index.max()
    last_week = x["Date"][last_week_index]

    weeks_on_chart = len(x)

    peak_position = x["Current Rank"].min()

    lyrics = x["Lyrics"].min()

    return pd.Series({"First Week Charted": first_week, "Last Week Charted": last_week, "Weeks on Chart": weeks_on_chart, "Peak Position": peak_position, "Lyrics": lyrics})


NR_df = MR_df.groupby(["Artist", "Song"]).apply(f)
NR_df.to_csv("Crisper.csv")
