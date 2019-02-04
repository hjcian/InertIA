import sys
import json

def loadConfig(fpath):
    try:
        with open(fpath, 'r') as fp:
            config = json.load(fp)
            return config
    except Exception as err:
        print('Error when loading config.json ({})'.format(err))
        sys.exit(1)