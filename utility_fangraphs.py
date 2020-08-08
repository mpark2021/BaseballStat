from pybaseball import pitching_stats_range as _pitching_stats_range
from pybaseball import batting_stats_range as _batting_stats_range


def pitching_range(start_dt, end_dt, name):
    stat = _pitching_stats_range(start_dt=start_dt, end_dt=end_dt)
    if name is None:
        return stat

    index = _find_index_by_name(stat, name)
    return stat.head(index + 1).tail(1)


#Y
def get_trainable_data(stat):
    era = stat.ERA
    babip = stat.BAbip


    return [era, babip]


#X
def batter_range(start_dt, end_dt, team):
    stat = _batting_stats_range(start_dt=start_dt, end_dt=end_dt)
    if team is None:
        return stat

    stat = find_team(stat, team)
    ab = stat.ab
    ba = stat.ba

    print(sum(ab * ba) / sum (ab))

    return stat


def find_team(stat, team):
    return stat.loc[stat.index.map(lambda i: stat.loc[i, 'Tm'] == team)]


def _find_index_by_name(stat, name):
    names = list(map(lambda x: x.lower(), list(stat.Name)))
    return names.index(name.lower())