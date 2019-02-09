import os
import sys
import json
import traceback

DEFAULT_CONFIG = {
    "database": "ft.db",
}

def loadConfig(fpath):
    try:
        if os.path.isfile(fpath):
            with open(fpath, 'r') as fp:
                config = json.load(fp)
                return config
        else:
            os.makedirs(os.path.dirname(fpath))
            with open(fpath, 'w') as fp:
                json.dump(DEFAULT_CONFIG, fp)
            return DEFAULT_CONFIG
    except Exception:
        print('Error when loading/writing config ({})'.format(traceback.format_exc()))
        return DEFAULT_CONFIG