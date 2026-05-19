#import sqlite3
from random import randint


def gen_username(lastname, firstname):

    #for word in firstname:
    #    for letter in word:
    #        if not letter.isalpha():
    #            word = word.replace(letter, '')
    #            print('q')

    dict = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'jo', 'ж': 'zh', 'з': 'z',
            'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
            'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}

    username = ''
    print(lastname)
    for i in lastname:
        #print(i)
        if i.isalpha():
            username += dict[i]
        else:
            continue
    print('username ', username)
    print('lastname ', lastname)
    print('firstname ', firstname)
    username += '_' + dict[firstname[0][0]] + dict[firstname[1][0]] + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
    return username


def gen_password():
    letters = 'qwertyuiopasdfghjklzxcvbnm'
    password = str(randint(0, 9)) + letters[randint(0, 25)].upper() + letters[randint(0, 25)] + str(randint(0, 9)) + letters[randint(0, 25)].upper() + letters[randint(0, 25)] + '-' + str(randint(0, 9)) + letters[randint(0, 25)].upper() + letters[randint(0, 25)]
    return password


def generate(lastname, firstname):
        firstname = firstname.lower().split()
        lastname = lastname.lower()
        username = gen_username(lastname, firstname)
        password = gen_password()
        return username, password

