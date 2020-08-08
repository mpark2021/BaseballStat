def _create_fg():
    sa_names = []

    with open('data/new_playerdata.csv', encoding='utf-8') as f:
        title = f.readline().split(',')
        fg_name_idx = title.index('FANGRAPHSNAME')
        fg_id_idx = title.index('IDFANGRAPHS')

        with open('data/players_fg.txt', 'w') as fg:
            while True:
                data = f.readline()
                if len(data) == 0:
                    break

                data = data.split(',')

                if len(data[fg_name_idx]) > 0:
                    if 'sa' not in data[fg_id_idx]:
                        if data[fg_name_idx] != 'Last Player':
                            fg.write(data[fg_name_idx] + "\t" + data[fg_id_idx] + "\n")
                    else:
                        sa_names.append(data[fg_name_idx])

    with open('data/minors.txt', 'w') as minor:
        for sa in sa_names:
            minor.write(sa + '\t')


def load_pid():
    with open('data/players_fg.txt') as f:
        while True:
            data = f.readline()
            if len(data) == 0:
                break

            data = data.split('\t')

            if data[0] in _pid:
                print(f'Duplicate: {data[0]}')

            _pid[data[0]] = int(data[1].strip())

    # special cases
    _pid['Pat Venditte'] = 7108
    _pid['Will Smith'] = 8048
    _pid['Chris Carpenter'] = 1292
    _pid['David Carpenter'] = 3959
    _pid['Miguel Gonzalez'] = 7024
    _pid['Matt Reynolds'] = 8887


def get_pid(name, is_batter):
    if len(_pid) == 0:
        load_pid()
    if name == "Chris Young":
        if is_batter:
            return 3882
        else:
            return 3196
    return _pid[name]


def is_minor(name):
    if len(_minor_names) == 0:
        _minor_names.append('.')  # this is for preventing REAL empty minor names
        with open('data/minors.txt') as f:
            _minor_names.extend(f.readline().split('\t'))
    return name in _minor_names


def espn_to_fangraph(name):
    espn_map = {
        'B.J. Upton': 'Melvin Upton Jr.',
        'Dewayne Wise': 'DeWayne Wise',
        'Norichika Aoki': 'Nori Aoki',
        'ByungHo Park': 'Byung-ho Park',
        'Thomas Milone': 'Tommy Milone',
        'JT Riddle': 'J.T. Riddle',
        'Mike Gonzalez': 'Michael Gonzalez',
        'Juan Carlos Oviedo': 'Juan Oviedo',

    }
    return espn_map.get(name, name)


def care_special_names(name):
    special = {
        'Rickie Weeks Jr.': 'Rickie Weeks',
        'Nathan Karns': 'Nate Karns',
    }
    return special.get(name, name)

_pid = {}
_minor_names = []


if __name__ == "__main__":
    load_pid()