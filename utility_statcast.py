from pybaseball import playerid_lookup
from pybaseball import statcast_pitcher

_pid_lookup = {}
_pitcher_lookup = {}

def get_playerid(lname, fname):
    name = (lname + " " + fname).lower

    if name in _pid_lookup:
        return _pid_lookup[name]

    pid = playerid_lookup(lname, fname)
    key = list(pid)
    print(pid)
    # key [2] = key_mlbam
    pid_list = list(pid[key[2]])
    _pid_lookup[name] = pid_list
    return pid_list


def get_pitcher_stat(start_dt, end_dt, arg1, arg2=None):
    if arg2 is not None:
        if not (type(arg1) == str and type(arg2) == str):
            print("Type mismatched:", type(arg1), type(arg2))
            return

        name = (arg1 + " " + arg2).lower()
        pid = _get_pid(name)
    else:
        if not type(arg1) == int:
            print("Type mismatched:", type(arg1))
            return
        pid = arg1

    return statcast_pitcher(start_dt=start_dt, end_dt=end_dt, player_id=pid)


def _get_pid(name):
    if name in _pid_lookup:
        return _get_pid[name]
    else:
        [lname, fname] = name.split()
        return get_playerid(lname, fname)


