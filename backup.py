import json
from pathlib import Path


def load_config():
    with open(BPATH.joinpath('config.json')) as f:
        return json.load(f)


def log(line):
    try:
        with open(BPATH.joinpath('dummy.log'), 'a') as log:
            line += '\n'
            log.write(line)
    except OSError:
        print('Log file could not be accessed.')
    finally:
        return None


def plog(line):
    print(line)
    log(line)
    return None


def set_backup_path():
    global BPATH
    BPATH = Path.home().joinpath('.backup')
    return None


set_backup_path()
