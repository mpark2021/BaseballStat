import numpy as np


def load(_start, _end, _ratio, _stat_suffix):
    path = f'./data/fa_data_{_stat_suffix}_{_start}_{_end}_{str(_ratio)}'
    _data = np.load(path + '.npy', allow_pickle=True)
    _data_bat = np.load(path + '_bat.npy', allow_pickle=True)
    _data_pit = np.load(path + '_pit.npy', allow_pickle=True)

    return _data, _data_bat, _data_pit, path


def modify_contract_by_median(_data):
    first = _data[0,0]
    last = _data[-1,0]
    index = []
    last_index = 0
    year_array = list(_data[:, 0])

    for year in range(first+1, last+1):
        curr_index = year_array.index(year)
        index.append(range(last_index, curr_index))
        last_index = curr_index

    index.append(range(last_index, len(_data)))

    medians = []

    for idx in index:
        yearly_data = get_iql(_data[idx, -1])
        medians.extend([np.median(yearly_data)] * len(idx))

    medians = np.asarray(medians) / medians[0]
    _data[:, -1] = _data[:, -1] / medians

    return _data


def modify_contract_by_mean(_data):
    first = _data[0,0]
    last = _data[-1,0]
    index = []
    last_index = 0
    year_array = list(_data[:, 0])

    for year in range(first+1, last+1):
        curr_index = year_array.index(year)
        index.append(range(last_index, curr_index))
        last_index = curr_index

    index.append(range(last_index, len(_data)))

    means = []

    for idx in index:
        yearly_data = get_iql(_data[idx, -1])
        means.extend([np.mean(yearly_data)] * len(idx))

    means = np.asarray(means) / means[0]
    _data[:, -1] = _data[:, -1] / means

    return _data


def get_iql(_contract):
    _contract = np.sort(_contract)
    return _contract[int(len(_contract)*0.25):int(len(_contract)*0.75)]


def save(_data, _data_pit, _data_bat, path):

    np.save(f'{path}_mod.npy', _data)
    np.save(f'{path}_pit_mod.npy', _data_pit)
    np.save(f'{path}_bat_mod.npy', _data_bat)


if __name__ == "__main__":
    start = 2012
    end = 2019
    ratio = [5.0, 3.0, 2.0]
    stat_suffix = 'all'
    data, data_bat, data_pit, path = load(start, end, ratio, stat_suffix)
    data = modify_contract_by_mean(data)
    data_pit = modify_contract_by_mean(data_pit)
    data_bat = modify_contract_by_mean(data_bat)
    save(data, data_pit, data_bat, path)