from pybaseball import pitching_leaders
from utility import pid_helper


def get_leaders(start_season, end_season=None, league='all', name_list=None):
    stats = ['Season','Name', 'ERA', 'K/9', 'IP', 'SLG', 'Def', 'SB']
    pid = []
    if name_list is not None:
        for name in name_list:
            pid.append(pid_helper.get_pid(name))
    leaders = pitching_leaders.pitching_stats(start_season, end_season, league=league, qual=0, pid=pid)
    leaders = leaders.sort_values('Season').sort_values('Name')
    leaders = leaders.reset_index()

    return leaders.loc[:, stats]