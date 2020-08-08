from utility.crawl import read
import sys
import utility.fangraphs_wrapper as wrap

if __name__ == "__main__":
    suffix = 'all'
    target_stat_path = f'./data/stat_{suffix}'
    stat = {}
    with open(target_stat_path) as f:
        while True:
            line = f.readline()
            if line == '':
                break

            if 'bat:' in line:
                wrap.stat['bat'] = line.split()[-1]
            if 'def:' in line:
                wrap.stat['def'] = line.split()[-1]
            if 'pit:' in line:
                wrap.stat['pit'] = line.split()[-1]


    '''
    argv: start_season, end_season
    if no end_season : end_season = start_season
    if both are none: start_season = 2019
    '''
    if len(sys.argv) < 2:
        print('USAGE: -s START-END -r RATIO1 RATIO2 RATIO3')
    else:
        if sys.argv.count('-s') == 1:
            season_idx = sys.argv.index('-s')
            [start, end] = map(int, sys.argv[season_idx + 1].split('-'))
            season_list = [x for x in range(start, end+1)]
        else:
            print('No proper season argument found, using default value of 2019')
            season_list = [2019]
        if sys.argv.count('-r') == 1:
            ratio_idx = sys.argv.index('-r')
            ratio = list(map(float, sys.argv[ratio_idx+1:ratio_idx+4]))
        else:
            ratio = [5, 3, 2]
            print('No proper ratio argument found, using default value of [5, 3, 2]')

        read(season_list, ratio, suffix)