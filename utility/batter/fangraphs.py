from pybaseball import batting_leaders
from utility import pid_helper, fangraphs_wrapper as batting_leaders


def get_leaders(start_season, end_season=None, league='all', name_list=None):
    stats = ['Season','Name', 'PA', 'AVG', 'OBP', 'SLG', 'Def', 'SB']
    pid = []
    if name_list is not None:
        for name in name_list:
            pid.append(pid_helper.get_pid(name))
    leaders = batting_leaders.batting_stats(start_season, end_season, league=league, qual=0, pid=pid)
    leaders = leaders.sort_values('Season').sort_values('Name')
    leaders = leaders.reset_index()

    return leaders.loc[:, stats]


if __name__ == "__main__":
    import os
    os.chdir("../..")
    result = get_leaders(2016, 2019, name_list=['Anthony Rendon', 'Mike Trout', 'Josh Donaldson'])
    print(result)

