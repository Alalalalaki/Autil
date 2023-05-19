import pickle
import dill
from urllib.request import urlopen


def write_file(file, file_path):
    try:
        with open(file_path, 'wb') as f:
            pickle.dump(file, f)
    except Exception:
        with open(file_path, 'wb') as f:
            dill.dump(file, f)


def read_file(file_path):
    try:
        if file_path.startswith('http'):
            with urlopen(file_path,) as f:
                file = pickle.load(f)
        else:
            with open(file_path, 'rb') as f:
                file = pickle.load(f)
    except Exception:
        if file_path.startswith('http'):
            with urlopen(file_path,) as f:
                file = dill.load(f)
        else:
            with open(file_path, 'rb') as f:
                file = dill.load(f)
    return file
