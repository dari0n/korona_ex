# Open File

def ffunctions():
    filepath = 'files/test.txt'
    file = open(filepath, 'a', encoding='utf-8')
    return file


if __name__ == '__main__':
    # Read
    # print(ffunctions().read())

    # Seek
    # Если 0 то курсор переходит к началу файла
    #ffunctions().seek(0)

    # Readline считывает строку
    #print(ffunctions().readline())

    #Обход всех символов строки
    #for row in ffunctions():
        # Строка по символам
    #   for letter in row:
            # print(letter)

    # Список строк
    #s = ffunctions().readlines()
    #print(s)

    #Запись в файл
    ffunctions().write('test\n')

