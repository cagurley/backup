import datetime as dt
import json
from pathlib import Path
import shutil


BPATH = None
CONFIG = None
LOG = None


def backup(src, dst):
    if dst.is_file():
        if not src.exists():
            dst.unlink()
            plog(f"Deleted destination file {dst} not represented in source.")
        elif not dst.exists():
            shutil.copy2(src, dst)
            plog(f"Created new destination file {dst} from {src}.")
        elif dst.stat().st_mtime != src.stat().st_mtime:
            shutil.copy2(src, dst)
            plog(f"Overwrote destination file {dst} with modified file {src}.")
    elif dst.is_dir():
        print(f"Backing up: {src} => {dst}")
        if not dst.exists():
            dst.mkdir()
            plog(f"Created new destination directory {dst} to mirror {src}.")
        src_names = [p.name for p in src.iterdir()]
        dst_diff = [p for p in dst.iterdir() if p.name not in src_names]
        for item in src.iterdir():
            backup(item, dst.joinpath(item.name))
        for item in dst_diff:
            backup(src.joinpath(item.name), item)
        if not src.exists():
            dst.rmdir()
            plog(f"Deleted destination directory {dst} not represented in source.")
    return None


def close_log():
    """
    :return: None

    MUST be called in finally clause after module import
    """
    global LOG
    end = dt.datetime.now()
    plog(f"Backup ended at {end.strftime('%I:%M:%S %p')} on {end.strftime('%d %b %Y')}.")
    LOG.close()
    return None


def init_log():
    global LOG
    start = dt.datetime.now()
    LOG = open(BPATH.joinpath('log', f"{start.strftime('%Y%d%m%H%M%S')}.txt"), 'w')
    plog(f"Backup begun at {start.strftime('%I:%M:%S %p')} on {start.strftime('%d %b %Y')}.")
    return None


def load_config():
    global CONFIG
    with open(BPATH.joinpath('config.json')) as f:
        CONFIG = json.load(f)
    CONFIG['src'] = [Path(s).resolve() for s in CONFIG['src']]
    CONFIG['dst'] = Path(CONFIG['dst']).resolve()
    return None


def log(line):
    line += '\n'
    LOG.write(line)
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
load_config()
init_log()
