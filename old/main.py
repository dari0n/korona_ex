import email.message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import pysftp
import paramiko
import datetime
import time
import os
import shutil
from base64 import decodebytes
import smtplib

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

def smtp_message(filename, dateTime):
    message = """
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    Subject: Обмен с ЦФТ %s

    Файл успешно отправлен.<br>\n
    Наименование файла: %s<br>\n
    Время: %s<br>\n
    """ %(dateTime, filename, dateTime)
    return message





if __name__ == '__main__':

    #paramiko.hostkeys.HostKeys('files/known_hosts')
    #paramiko.hostkeys.HostKeys.load(filename='keys/known_hosts')
    #Параметры
    host = 'gbd.ftc.ru'
    port = 11222
    username = 'cifrograd'
    private_key = 'keys/id_rsa'
    private_key_pass = 'f1n8sbOW6C38'
    key_data = b"""AAAAB3NzaC1yc2EAAAABIwAAAgEAzG68bROjTKziJkhxhFBwx4TOzb9oA9FvjalKXlYEqwgL4eHvpunaCMU7NKCSQXS5o/cBTDN5e+IBgkQhjAFsE/xliVl9q2HhT1ZV10gi2i0VbH4Qrp1bXLg0tpRv6CCDh6pz+te5lT881o07x47vkhtOPZVbDjuztCc9168F2CmKlriEH9ZhqTRWBtxaSC6t7ytTvNcvlUOGpJ0IGoAJggW9iY09AhdzU4Gt5FNMSPUkLf+DSwetxYJI5Tv3H63zUxYU1rhAkf374PbpiKc3hQiq/D3jtW7DEenqOHUPQUfCSXIadnQ87iKvaJ82/9tLyBCKHr9gReEPCc58c+pGklL8FZPbZfvxH+miOQTsXomjqdd4dhDiAERDS4srUPrD1F0GvfTU9rjpnhf3EmSjfAtLCRCJUMzpefn8Hl38ZYc/BlOY61Lz95XS0qx43yfO600rF1+iA0G5ve3PU//L9paTYe3sbb+wSzlIW36kq3OqzHPeZ7M9Z4a3OS/TfpM5CcnqZFSgbORKHt3n+6ukyubzJOGeELwMLgzUC+UnbrwuHecrWjmV3Z2O2jzwOZ1gO2RTt41JDMqaRPnmM+WeERKUYs3Op+8fkwcSPDVu9tEMWESbHyyWzoztPgTCHSvhA5XvbniLL0rDJNpIjSKYcBOmbJMi4M378Zk+b73fc7k="""
    key = paramiko.RSAKey(data=decodebytes(key_data))
    path_to_file = 'files/data.csv'
    path_to_prepared_file = 'prepared_files/'
    date_now = datetime.datetime.now()
    file_prefix = date_now.strftime("%Y%m%d%H%M") #yyyymmdd24m
    date_for_message = date_now.strftime("%d-%m-%Y %H:%M")
    newFilename = 'TK_' + file_prefix + '.csv.tmp' # Имя файла перед загрузкой
    newFilenameOnServer = 'TK_' + file_prefix + '.csv' # Имя файла после загрузки
    path_to_upload = 'in/gds-ctl_mbm_catalog/'
    path_to_download = 'out/gds-ctl_mbm_catalog/' # Возможно потом понадобится загружать ответы от удаленного сервера
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.add(host, 'ssh-rsa', key)
    #SMTP
    smtp_server = 'mail.expconsalt.ru: 587'
    msg = MIMEMultipart()
    msg['Subject'] = 'Произведена отправка файла %s' %(newFilenameOnServer)
    msg['From'] = 'exchange_bot@expconsalt.ru'
    msg['To'] = 'it@expconsalt.ru'
    smtp_password = 'Wbahjuhfl2020!@#$'
    msg.add_header('Content-Type', 'text/html')
    email_content = smtp_message(newFilenameOnServer, date_for_message)






    while True:

        #Проверка наличия файла

        if file_exist('files/202202071717.csv') == True:
            print("Файл существует. Ждем дозагрузку из 1С")
            time.sleep(2)

            # манипуляция с файлом
            # Копирование файла
            #print("Копирование файла")
            #shutil.copy(path_to_file, path_to_prepared_file + newFilename)
            #shutil.copy(path_to_file, path_to_prepared_file + newFilenameOnServer)


            # Коннект к серверу по ключу
            try:
                with Sftp_Connection(host, username=username, private_key=private_key, port=port,
                                     private_key_pass=private_key_pass, cnopts=cnopts) as sftp:
                    # Лист директорий
                    l = sftp.listdir()
                    print(l)

                    sftp.put('files/202202071717.csv', 'in/gds-ctl_mbm_catalog/202202071717.csv')

                    # Передача файла из prepared_files
                    # Отключение от сервера
                    print("Файл отправлен: "+ path_to_upload + newFilenameOnServer + ", отключение от сервера")
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


