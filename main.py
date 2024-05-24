# -*- coding: utf-8 -*-
import paramiko
import pysftp
import os
import time
import datetime
import shutil
from base64 import decodebytes


filepath_directory = '/home/nt_exchange/exchange/korona_ex/files/files/'
path_to_prepared_file = '/home/nt_exchange/exchange/korona_ex/prepared_files/'
prepared_file_type = '.tmp'
host = ''
port = 11222
username = ''
private_key = '/home/nt_exchange/exchange/korona_ex/keys/id_rsa'
private_key_pass = ''
key_data = b"""AAAA"""
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

    """ Смотри существуют ли файлы, если да, переименовываем в tmp и кладем prepared_files """

    def prepare_exists(filepath_directory, path_to_prepared_file, file_type):

        for root, dirs, files in os.walk(filepath_directory):
            if files:
                for file in files:
                    fullpath = filepath_directory + file
                    shutil.copy(fullpath, path_to_prepared_file + file + file_type)
                    # перемещение файла
                    shutil.move(fullpath, '/home/nt_exchange/exchange/korona_ex/files/send/' + file)
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
                        print(current_time(), 'Текущее состояние каталога OUT' ,l)
                        for file in files:
                            print(current_time(),'Загрузка файла', path_to_upload + file)
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
                print(current_time()," Проверка каталога out", l)

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
                        sftp.get(path + rfile, '/home/nt_exchange/exchange/korona_ex/files/out/' + rfile)
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





