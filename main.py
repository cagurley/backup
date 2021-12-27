import backup


if __name__ == '__main__':
    try:
        for p in backup.CONFIG['src']:
            backup.backup(p, backup.CONFIG['dst'].joinpath(p.name))
    except Exception as e:
        backup.plog(e)
    finally:
        backup.close_log()
