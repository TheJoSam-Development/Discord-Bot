"""Generates an UUID in the TheJoSam Development custom style"""

import secrets
import string

CHARSET = string.ascii_letters + string.digits

# Combinations: 62^53 = 9.9256634029802911934e+94

def generate():
    """Generates an UUID in the TheJoSam Development custom style"""
    unique = False
    id_list = open('data/tuuids.dat', 'a+', encoding='utf-8')
    ids = id_list.readlines()

    while unique is False:
        tuuid = ''
        for i in range(10):
            tuuid += secrets.choice(CHARSET)
        tuuid += '-'
        for i in range(5):
            tuuid += secrets.choice(CHARSET)
        tuuid += '-'
        for i in range(15):
            tuuid += secrets.choice(CHARSET)
        tuuid += '-'
        for i in range(15):
            tuuid += secrets.choice(CHARSET)
        tuuid += '-'
        for i in range(3):
            tuuid += secrets.choice(CHARSET)
        tuuid += '-'
        for i in range(5):
            tuuid += secrets.choice(CHARSET)

        if tuuid not in ids:
            unique = True

    id_list.write(tuuid + '\n')
    id_list.close()
    return tuuid
