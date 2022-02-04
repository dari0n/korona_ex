import pysftp
import paramiko
import datetime
import time
import os
import shutil


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


# Проверка наличия файла
def file_exist(path):
    return os.path.exists(path)


if __name__ == '__main__':
    #Параметры
    host = 'localhost'
    username = ''
    private_key = ''
    private_key_pass = ''
    path_to_file = 'files/data.csv'
    path_to_prepared_file = 'prepared_files/'
    date_now = datetime.datetime.now()
    file_prefix = date_now.strftime("%Y%m%d%H%M") #yyyymmdd24m
    newFilename = 'ТК_' + file_prefix + '.csv.tmp' # Имя файла перед загрузкой
    newFilenameOnServer = 'ТК_' + file_prefix + '.csv' # Имя файла после загрузки
    path_to_upload = 'in/gds-ctl_mbm_catalog/'
    path_to_download = 'out/gds-ctl_mbm_catalog/' # Возможно потом понадобится загружать ответы от удаленного сервера

    #Цикл:
    while True:
        #Проверка наличия файла
        if file_exist(path_to_file) == True:
            print("Файл существует. Ждем дозагрузку из 1С")
            time.sleep(3)

            # манипуляция с файлом
            # Копирование файла
            print("Копирование файла")
            shutil.copy(path_to_file, path_to_prepared_file + newFilename)


            # Коннект к серверу по ключу


            try:
                with Sftp_Connection(host, username=username, private_key=private_key,
                                     private_key_pass=private_key_pass) as sftp:
                    # Лист директорий
                    l = sftp.listdir()
                    print(l)
                    # Передача файла из prepared_files
                    sftp.put(path_to_prepared_file + newFilename, path_to_upload + newFilenameOnServer)
                    # Отключение от сервера
                    print("Файл отправлен, отключение от сервера")
                    sftp.__del__()
                    print("Удаление старого файла: " + path_to_file)
                    os.remove(path_to_file)
                    print("Удаление временного файла: " + path_to_prepared_file + newFilename)
                    os.remove(path_to_prepared_file + newFilename)

            except paramiko.ssh_exception.SSHException as e:
                print('Публичный ключ отсутствует в known_hosts', e)

        else:
            print("Файл отсутствует ждем 30 секунд")
            time.sleep(10)


