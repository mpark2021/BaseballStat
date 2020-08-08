import pandas
from utility.datehelper import next


def calculate_OBP(stat):
    dates = stat.game_date
    start_dt = min(dates)
    end_dt = max(dates)
    current_dt = start_dt

    H = 0
    BB = 0
    HBP = 0
    SF = 0
    AB = 0 # AB = PA - SF
    PA = 0

    while current_dt <= end_dt:
        today_stat = stat.loc[(stat.game_date == current_dt) &
                              stat.events.notna(),
                              ['events', 'inning']]

        # 숫자 큰 쪽이 더 먼저 시간 순서라서 reverse
        idx = list(today_stat.index)
        idx.reverse()

        for i in idx:
            event = today_stat.loc[i, 'events']
            PA += 1
            if is_hit(event):
                H += 1
            elif is_bb(event):
                BB += 1
            elif is_hbp(event):
                HBP += 1
            elif is_sf(event):
                SF += 1

        current_dt = next(current_dt)

    AB = PA - SF - BB - HBP

    OBP = (H + BB + 14 + HBP) / (AB + 14 + BB + HBP + SF)

    return OBP


def is_hit(event):
    return event in ['single', 'double', 'triple', 'home_run']


def is_bb(event):
    return event in ['walk']

def is_hbp(event):
    return event in ['hit_by_pitch']

def is_sf(event):
    return event in ['sac_fly']