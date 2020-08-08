from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


stat = {}


def count_stat(t):
    return len(stat.get(t, '').split(',')) - 1


def get_soup(start_season, end_season, league, qual, ind, stat, pid, position):
    pid_str = ""
    for id in pid:
        pid_str += str(id)
        pid_str += ","
    pid_str = pid_str[:-1]

    url =  'http://www.fangraphs.com/leaders.aspx?pos=all&stats={}&lg={}&qual={}&type={}&season={}&month=0&season1={}&ind={}&team=&rost=&age=&filter=&players={}&page=1_100000'
    url = url.format(position, league, qual, stat, end_season, start_season, ind, pid_str)
    s=requests.get(url).content
    return BeautifulSoup(s, "lxml")


def get_table(soup, ind):
    table = soup.find('table', {'class': 'rgMasterTable'})
    data = []
    # pull heading names from the fangraphs tables
    headings_raw = table.find_all('th')[1:]
    headings = []
    for row in headings_raw:
        r = row.text.strip()
        if r in headings:
            r += f'({headings.count(r)+1})'
        headings.append(r)

    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols[1:]])

    data = pd.DataFrame(data=data, columns=headings)

    # replace empty strings with NaN
    data.replace(r'^\s*$', '0', regex=True, inplace=True)

    # remove '%' from all data and convert them to numeric
    cols_including_percent = [col for col in data.columns if '%' in col or col == 'HR/FB']
    for col in cols_including_percent:
        data[col] = data[col].str.replace('%', '')

    # convert everything except name and team to numeric
    cols_to_numeric = [col for col in data.columns if col not in ['Name', 'Team']]
    data[cols_to_numeric] = np.nan_to_num(data[cols_to_numeric].astype(float))
    return data.to_numpy()


# batting + fielding stat
def batting_stats(start_season, end_season=None, league='all', qual='y', ind=1, pid=None):
    if start_season is None:
        raise ValueError("You need to provide at least one season to collect data for. Try pitching_leaders(season) or pitching_leaders(start_season, end_season).")
    if end_season is None:
        end_season = start_season
    if pid is None:
        pid = []

    soup = get_soup(stat=stat['bat'], start_season=start_season, end_season=end_season, league=league, qual=qual, ind=ind, pid=pid, position='bat')
    table = get_table(soup, ind)
    return table


def fielding_stats(start_season, end_season=None, league='all', qual='y', ind=1, pid=None):

    if start_season is None:
        raise ValueError("You need to provide at least one season to collect data for. Try pitching_leaders(season) or pitching_leaders(start_season, end_season).")
    if end_season is None:
        end_season = start_season
    if pid is None:
        pid = []

    soup = get_soup(stat=stat['def'], start_season=start_season, end_season=end_season, league=league, qual=qual, ind=ind,
                    pid=pid, position='fld')
    table = get_table(soup, ind)
    return table


def pitching_stats(start_season, end_season=None, league='all', qual='y', ind=1, pid=None):
    if start_season is None:
        raise ValueError("You need to provide at least one season to collect data for. Try batting_leaders(season) or batting_leaders(start_season, end_season).")
    if end_season is None:
        end_season = start_season
    if pid is None:
        pid = []

    soup = get_soup(stat=stat['pit'], start_season=start_season, end_season=end_season, league=league, qual=qual, ind=ind, pid=pid, position='pit')
    table = get_table(soup, ind)
    return table
