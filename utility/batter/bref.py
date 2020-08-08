from pybaseball import batting_stats_range
import os

stat = batting_stats_range("2019-03-28", "2019-09-29")


def calc_aging(start_season=None, end_season=None):
    if start_season is None:
        start_season = 2008
    if end_season is None:
        end_season = 2019

    if end_season < start_season:
        return

    path = "data/aging_curve"
    done = []
    if os.path.exists(path):
        with open(path) as f:
            done.extend(map(int, f.readline().split()))
        print(done)



