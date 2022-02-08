import paramiko
import pysftp
import os
import time
import datetime
import shutil
from base64 import decodebytes


# Параметры
filepath_directory = 'files/'
path_to_prepared_file = 'prepared_files/'
prepared_file_format = '.tmp'
host = 'gbd.ftc.ru'
port = 11222
username = 'cifrograd'
private_key = 'keys/id_rsa'
private_key_pass = 'f1n8sbOW6C38'
key_data = b"""AAAAB3NzaC1yc2EAAAABIwAAAgEAzG68bROjTKziJkhxhFBwx4TOzb9oA9FvjalKXlYEqwgL4eHvpunaCMU7NKCSQXS5o/cBTDN5e+IBgkQhjAFsE/xliVl9q2HhT1ZV10gi2i0VbH4Qrp1bXLg0tpRv6CCDh6pz+te5lT881o07x47vkhtOPZVbDjuztCc9168F2CmKlriEH9ZhqTRWBtxaSC6t7ytTvNcvlUOGpJ0IGoAJggW9iY09AhdzU4Gt5FNMSPUkLf+DSwetxYJI5Tv3H63zUxYU1rhAkf374PbpiKc3hQiq/D3jtW7DEenqOHUPQUfCSXIadnQ87iKvaJ82/9tLyBCKHr9gReEPCc58c+pGklL8FZPbZfvxH+miOQTsXomjqdd4dhDiAERDS4srUPrD1F0GvfTU9rjpnhf3EmSjfAtLCRCJUMzpefn8Hl38ZYc/BlOY61Lz95XS0qx43yfO600rF1+iA0G5ve3PU//L9paTYe3sbb+wSzlIW36kq3OqzHPeZ7M9Z4a3OS/TfpM5CcnqZFSgbORKHt3n+6ukyubzJOGeELwMLgzUC+UnbrwuHecrWjmV3Z2O2jzwOZ1gO2RTt41JDMqaRPnmM+WeERKUYs3Op+8fkwcSPDVu9tEMWESbHyyWzoztPgTCHSvhA5XvbniLL0rDJNpIjSKYcBOmbJMi4M378Zk+b73fc7k="""
key = paramiko.RSAKey(data=decodebytes(key_data))
cnopts = pysftp.CnOpts()
cnopts.hostkeys.add(host, 'ssh-rsa', key)
file_type = ".tmp"


if __name__ == "__main__":

    for root, dirs, files in os.walk(filepath_directory):
        if files:
            for file in files:
                fullpath = filepath_directory + file
                shutil.copy(fullpath, path_to_prepared_file + file + file_type)
                # удаление файла, отправка файла

                old_file = file

        else:
            print("Файлы отсуствуют, ожидание")
            time.sleep(3)


    for root, dirs, files in os.walk(path_to_prepared_file):
        if files:
            for file in files:
                fullpath = path_to_prepared_file + file
                shutil.copy(path_to_prepared_file + file, "out/" + file[:4])
                print("out/" + file[:-4])
                # удаление файла, отправка файла



        else:
            print("Файлы отсуствуют, ожидание")
            time.sleep(3)