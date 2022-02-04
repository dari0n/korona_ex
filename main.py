import pysftp
import os.path
import os
import time
import datetime
from pathlib import Path


# Проверка наличия файла
def file_exist(path):
    return os.path.exists(path)


def os_walk():
    return os.walk('files')


# Подключение по sftp
def connection():
    srv = pysftp.Connection('192.168.0.20', username='nt_exchange', private_key='keys/test_sftp',
                            private_key_pass='9R1mapkl!@#')
    return srv


if __name__ == '__main__':
    while True:
        PATH = 'files/data.csv'
        preparedFilesPath = 'prepared_files/'
        # print(type(connection()))
        fex: bool = file_exist(PATH)

        if fex == True:
            date = datetime.datetime.now()
            filenamePrefix = str(date.year) + str(date.month) + str(date.day) + str(date.hour) + str(date.minute) \
                             + str(date.second)
            filename = 'data.csv'
            newFilename = filenamePrefix + '.csv.tmp'
            newFilenameOnServer = filenamePrefix + '.csv'

            print(fex)

            print('Файл существует, ждем дозагрузку файла из 1С')
            time.sleep(3)


            # переместить файл # переименовать файл в tmp
            Path('files/data.csv').rename(preparedFilesPath + newFilename)
            print('Файл переименован в ' + newFilename + ' и перемещен в каталог отправки')

            # коннект к серверу
            try:
                srv = connection()
                print(srv)
                print('Соединение с sftp сервером установлено')
            except:
                print('Ошибка соединения')

            # отправить файл
            try:
                srv.put(preparedFilesPath + newFilename, newFilename)
            except:
                print('Ошибка отправки файла')
            finally:

                Path(preparedFilesPath + newFilename).unlink()
                print('Файл отправлен')
                print('Файл удален из каталога отправки')




            # переименовать файл в data_datetimenow csv
            try:
                srv.rename(newFilename, newFilenameOnServer)
            except:
                print('Ошибка переименования файла')
            finally:
                print('Файл переименован в ' + newFilenameOnServer)




            # дисконнект от сервера
            if srv:
                srv.close()
                print('Соединение закрыто')
            else:
                print(srv)
                print('Ошибка закрытия соединения')

            # ждем 30 секунд

            print('Ждем 30 секунд')

        else:
            print('Файл отсутствует, ждем 30 секунд')
            time.sleep(3)
    # for file in file_exist():
    #   print(file)
