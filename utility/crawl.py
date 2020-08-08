from utility.parser import parse_contract, pos
from utility.fangraphs_wrapper import *
from utility.pid_helper import get_pid, is_minor, care_special_names
import numpy as np
from utility.corrector import *

header_size = len(['season', 'name', 'age']) + len(pos)


def read_batter(season_list: list, ratio: list):
    playerdata_by_season = {}
    for season in season_list:
        result_batting = parse_contract(season)
        pd = []
        for player_data in result_batting:
            if player_data.is_signed() and player_data.is_batter():
                pd.append(player_data)
        playerdata_by_season[season] = pd

    # defensive stat check
    has_def_stat = count_stat('def') > 0

    # season ~ season - 2
    result_batting = None
    result_contract = None
    for season in season_list:
        pd = playerdata_by_season[season]
        season_result = np.zeros((len(pd), header_size + count_stat('bat') * 4), dtype=np.object)
        def_result = np.zeros((len(pd), header_size + count_stat('def') * 4), dtype=np.object)
        contract = np.zeros((len(pd), 1), dtype=np.object)
        counter = 0
        for player in pd:
            season_result[counter, 0] = season - 2000
            season_result[counter, 1] = player.get_name()
            season_result[counter, 2] = player.age - 2020 + season
            season_result[counter, 3 + player.get_position()] = 1
            if has_def_stat:

                def_result[counter, 0] = season - 2000
                def_result[counter, 1] = player.get_name()
                def_result[counter, 2] = player.age - 2020 + season
                def_result[counter, 3 + player.get_position()] = 1
            contract[counter, 0] = player.dollars / player.contract_years

            counter += 1
        pid = []
        for player in pd:
            if not is_minor(player.get_name()):
                pid.append(get_pid(player.get_name(), True))
        for s in range(season, season - 3, -1):
            bat_stat = batting_stats(s, s, qual=0, pid=pid)
            season_result = append_by_name(
                season_result,
                bat_stat,
                season - s,
                count_stat('bat')
            )
            if has_def_stat:
                field_stat = fielding_stats(s, s, qual=0, pid=pid)
                def_result = defensive_stat_append_by_name(
                    def_result,
                    field_stat,
                    season - s,
                    count_stat('def')
                )

        season_result = weighted_sum(season_result, ratio, create_sigmoid_2_corrector(qual=502))

        if has_def_stat:
            def_result = weighted_sum(def_result, ratio, create_one_corrector())
            season_result = np.concatenate((season_result, def_result[:, 2 + len(pos):]), axis=1)

        if result_batting is None:
            # first season in season_list
            result_batting = season_result
        else:
            result_batting = np.concatenate((result_batting, season_result))

        if result_contract is None:
            result_contract = contract
        else:
            result_contract = np.concatenate((result_contract, contract))

        print(f'{season} done - batter')

    return result_batting, result_contract


def read_pitcher(season_list: list, ratio: list):
    playerdata_by_season = {}
    for season in season_list:
        result_pitcher = parse_contract(season)
        pd = []
        for player_data in result_pitcher:
            if player_data.is_signed() and player_data.is_pitcher():
                pd.append(player_data)
        playerdata_by_season[season] = pd

    # season ~ season - 2
    result_pitcher = None
    result_contract = None
    for season in season_list:
        pd = playerdata_by_season[season]
        season_result = np.zeros((len(pd), header_size + (count_stat('pit')) * 4), dtype=np.object)
        contract = np.zeros((len(pd), 1), dtype=np.object)
        counter = 0
        for player in pd:
            season_result[counter, 0] = season - 2000
            season_result[counter, 1] = player.get_name()
            season_result[counter, 2] = player.age - 2020 + season
            season_result[counter, 3 + player.get_position()] = 1
            contract[counter, 0] = player.dollars / player.contract_years
            counter += 1
        pid = []
        for player in pd:
            if not is_minor(player.get_name()):
                pid.append(get_pid(player.get_name(), False))
        for s in range(season, season - 3, -1):
            pit_stat = pitching_stats(s, s, qual=0, pid=pid)
            season_result = append_by_name(
                season_result,
                pit_stat,
                season - s,
                count_stat('pit')
            )

        if result_pitcher is None:
            # first season in season_list
            result_pitcher = season_result
        else:
            result_pitcher = np.concatenate((result_pitcher, season_result))

        if result_contract is None:
            result_contract = contract
        else:
            result_contract = np.concatenate((result_contract, contract))

        print(f'{season} done - pitcher')

    result_pitcher = weighted_sum(result_pitcher, ratio, create_sigmoid_2_corrector(162))

    return result_pitcher, result_contract


def weighted_sum(result: np.ndarray, ratio: list, corrector):
    ratio = list(map(lambda x: x / sum(ratio), ratio))

    num_features = (result.shape[1] - header_size) // 4

    for offset in range(num_features):
        if offset == 0:
            f = create_one_corrector()
        else:
            f = corrector

        for i in range(len(ratio)):
            result[:, header_size + num_features * 3 + offset] += result[:, header_size + num_features * i + offset] \
                                                      * ratio[i] * f(result[:, header_size + num_features * i])

        return result


def read(season_list: list, ratio:list, suffix):
    season_list.sort()

    result_pit, contract_pit = read_pitcher(season_list, ratio)
    result_bat, contract_bat = read_batter(season_list, ratio)

    bat_shape = result_bat.shape
    pit_shape = result_pit.shape

    np.save(f'./data/fa_data_{suffix}_{season_list[0]}_{season_list[-1]}_{str(ratio)}_bat.npy',
            np.concatenate((result_bat, contract_bat), axis=1))
    np.save(f'./data/fa_data_{suffix}_{season_list[0]}_{season_list[-1]}_{str(ratio)}_pit.npy',
            np.concatenate((result_pit, contract_pit), axis=1))

    result_bat = np.pad(result_bat, ((0, 0), (0, pit_shape[1] - header_size)))
    result_pit = np.insert(result_pit, [header_size] * (bat_shape[1] - header_size), 0, axis=1)

    result = np.concatenate((result_bat, result_pit))
    contract = np.concatenate((contract_bat, contract_pit))

    result = np.concatenate((result, contract), axis=1)

    #idx = [x for x in range(result.shape[1])]
    #idx.remove(1)

    #save_target = result[:, idx]
    #save_target = save_target.astype(float)

    #np.save(f'./data/fa_data_{season_list[0]}_{season_list[-1]}.npy', save_target)

    np.save(f'./data/fa_data_{suffix}_{season_list[0]}_{season_list[-1]}_{str(ratio)}.npy', result)

    return result


def defensive_stat_append_by_name(result: np.ndarray, data: np.ndarray, before: int, num_stat: int):
    names = list(result[:, 1])
    names_data = list(data[:, 1])

    def find_all(_name):
        _name_data_list = []
        for _i, _v in enumerate(names_data):
            if _v == _name:
                _name_data_list.append(_i)
        return _name_data_list

    for i, name in enumerate(names):
        name_data_list = find_all(name)
        if len(name_data_list) == 0:
            continue
        innings = data[name_data_list, 3:4]
        stat = np.nan_to_num(data[name_data_list, 4:].astype(np.float))

        inn_sum = np.sum(innings)
        adjusted_stat = stat * innings

        if inn_sum > 0:
            adjusted_stat = np.sum(adjusted_stat, axis=0) / inn_sum

        start = header_size + before * num_stat
        end = header_size + (before + 1) * num_stat

        result[i, start] = inn_sum
        result[i, start + 1:end] = adjusted_stat
    return result


def append_by_name(result: np.ndarray, data: np.ndarray, before: int, num_stat: int):
    names = list(result[:, 1])
    for d in data:
        name = d[1]
        idx = names.index(care_special_names(name))
        start = header_size + before * num_stat
        end = header_size + (before + 1) * num_stat
        result[idx, start:end] = d[3:]
    return result