# Отправка письма
smtp_stream = smtplib.SMTP('mail.expconsalt.ru: 587')
smtp_stream.starttls()
smtp_stream.login(msg['From'], smtp_password)
file_to_send = (path_to_prepared_file + newFilenameOnServer)
ctype, encoding = mimetypes.guess_type(file_to_send)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"
maintype, subtype = ctype.split("/", 1)
fp = open(file_to_send, 'r', 'cp1251')
print(fp)
attachment = MIMEText(fp.read().decode('cp1251'), _subtype=subtype)
fp.close()
attachment.add_header("Content-Disposition", "attachment", filename=file_to_send)
msg.attach(attachment)

smtp_stream.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))
smtp_stream.quit()