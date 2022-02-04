from os import listdir
from os.path import isfile
from os.path import join as joinpath

def dirs():
    files = listdir('files')
    csv = filter(lambda x: x.endswitch('.csv'), files)
    return csv

def list_files():



if __name__ == '__main__':
