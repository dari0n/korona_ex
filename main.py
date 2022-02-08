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
prepared_file_type = '.tmp'
host = 'gbd.ftc.ru'
port = 11222
username = 'cifrograd'
private_key = 'keys/id_rsa'
private_key_pass = 'f1n8sbOW6C38'
key_data = b"""AAAAB3NzaC1yc2EAAAABIwAAAgEAzG68bROjTKziJkhxhFBwx4TOzb9oA9FvjalKXlYEqwgL4eHvpunaCMU7NKCSQXS5o/cBTDN5e+IBgkQhjAFsE/xliVl9q2HhT1ZV10gi2i0VbH4Qrp1bXLg0tpRv6CCDh6pz+te5lT881o07x47vkhtOPZVbDjuztCc9168F2CmKlriEH9ZhqTRWBtxaSC6t7ytTvNcvlUOGpJ0IGoAJggW9iY09AhdzU4Gt5FNMSPUkLf+DSwetxYJI5Tv3H63zUxYU1rhAkf374PbpiKc3hQiq/D3jtW7DEenqOHUPQUfCSXIadnQ87iKvaJ82/9tLyBCKHr9gReEPCc58c+pGklL8FZPbZfvxH+miOQTsXomjqdd4dhDiAERDS4srUPrD1F0GvfTU9rjpnhf3EmSjfAtLCRCJUMzpefn8Hl38ZYc/BlOY61Lz95XS0qx43yfO600rF1+iA0G5ve3PU//L9paTYe3sbb+wSzlIW36kq3OqzHPeZ7M9Z4a3OS/TfpM5CcnqZFSgbORKHt3n+6ukyubzJOGeELwMLgzUC+UnbrwuHecrWjmV3Z2O2jzwOZ1gO2RTt41JDMqaRPnmM+WeERKUYs3Op+8fkwcSPDVu9tEMWESbHyyWzoztPgTCHSvhA5XvbniLL0rDJNpIjSKYcBOmbJMi4M378Zk+b73fc7k="""
key = paramiko.RSAKey(data=decodebytes(key_data))
cnopts = pysftp.CnOpts()
cnopts.hostkeys.add(host, 'ssh-rsa', key)
path_to_upload = 'in/gds-ctl_mbm_catalog/'
path_to_download = 'out/gds-err-ctl_mbm_catalog/'


class Sftp_Connection(pysftp.Connection):
    def __init__(self, *args, **kwargs):
        try:
            if kwargs.get('cnopts') is None:
                kwargs['cnopts'] = pysftp.CnOpts()
        except pysftp.HostKeysException as e:
            self._init_error = True
            raise paramiko.ssh_exception.SSHException(str(e))
        else:
            self._init_error = False

        self._sftp_live = False
        self._transport = None
        super().__init__(*args, **kwargs)

    def __del__(self):
        if not self._init_error:
            self.close()







if __name__ == '__main__':


    def current_time():
        date_now = datetime.datetime.now()
        result = date_now.strftime("%d-%m-%Y %H:%M:%S")
        message = "[%s]"%(result)
        return message

    # Смотри существуют ли файлы, если да, переименовываем в tmp и кладем prepared_files
    def prepare_exists(filepath_directory, path_to_prepared_file, file_type):

        for root, dirs, files in os.walk(filepath_directory):
            if files:
                for file in files:
                    fullpath = filepath_directory + file
                    shutil.copy(fullpath, path_to_prepared_file + file + file_type)
                    # удаление файла
                    os.remove(fullpath)
                    print(current_time(), "Файл удален + " + fullpath)
                    return True
            else:
                print(current_time(), "Файлы отсуствуют")
                return False
                pass


    def send_prepared(prepared_files, path_to_upload):
        for root, dirs, files in os.walk('prepared_files/'):
            if files:
                # Открываем соединение
                try:
                    with Sftp_Connection(host, username=username, private_key=private_key, port=port,
                                         private_key_pass=private_key_pass, cnopts=cnopts) as sftp:
                        # Лист директорий
                        l = sftp.listdir(remotepath=path_to_upload)
                        print(l)
                        for file in files:
                            print(current_time(), path_to_upload + file)
                            sftp.put(prepared_files + file, path_to_upload + file)

                            print(current_time(), 'Файл отправлен: ' + path_to_upload + file)
                            # Переименовываем файлы на сервере
                            sftp.rename(path_to_upload + file, path_to_upload + file[:-4])
                            print(current_time(), 'Файл переименован: ' + path_to_upload + file[:-4])
                            # Проверяем наименования файлов на сервере
                            l = sftp.listdir(remotepath=path_to_upload)
                            print(l)
                            os.remove(prepared_files + file)
                        # Закрываем соединение
                        sftp.__del__()
                        return True
                except paramiko.ssh_exception.SSHException as e:
                    print(current_time(), 'Публичный ключ отсутствует в known_hosts', e)
                    pass

            else:

                print(current_time(), "Подготовленные файлы отсутствуют (Что-то пошло не так)")
                pass

        # Опциональная проверка на наличие файлов в каталоге указать @Path
    def check_path(path):
        try:
            with Sftp_Connection(host, username=username, private_key=private_key, port=port,
                                 private_key_pass=private_key_pass, cnopts=cnopts) as sftp:
                # Лист директорий
                l = sftp.listdir(remotepath=path)
                print(l)

        except paramiko.ssh_exception.SSHException as e:
            print(current_time(), 'Публичный ключ отсутствует в known_hosts', e)
            pass

    def get_errors(path):
        try:
            with Sftp_Connection(host, username=username, private_key=private_key, port=port,
                                 private_key_pass=private_key_pass, cnopts=cnopts) as sftp:

                l = sftp.listdir(remotepath=path)
                print(l)
                for rfile in l:
                    if "tmp" in rfile:
                        print("Пропуск папки tmp")
                        pass
                    else:
                        print(current_time(), rfile)
                        sftp.get(path + rfile, 'out/' + rfile)
                        sftp.remove(path + rfile)
                sftp.__del__()
                return True
        except paramiko.ssh_exception.SSHException as e:
            print(current_time(), 'Публичный ключ отсутствует в known_hosts', e)
            pass



    while True:
        # Подготовка файлов
        if prepare_exists(filepath_directory, path_to_prepared_file, prepared_file_type) == True:
            send_prepared(path_to_prepared_file, path_to_upload)
            check_path(path_to_upload)
            check_path(path_to_download)
            get_errors(path_to_download)
            print(current_time(), 'Файлы отправлены')
        else:
            print(current_time(), "Ожидание файлов для отправки....")
            time.sleep(900)
            check_path(path_to_download)
            get_errors(path_to_download)





