"""Generates an UUID in the TheJoSam Development custom style"""

import secrets
import string

CHARSET = string.ascii_letters + string.digits

# Combinations: 62^53 = 9,9256634029802911933839693889845e+94 (type 0)
#               62^43 = 1,1826129992021603432356715832488e+77 (type 1)
#               62^22 = 2,7078036478026604002902615371853e+39 (type 2)

def generate(type:int = 0):
    """Generates an UUID in the TheJoSam Development custom styles\n
    TYPES:\n
    0) Standart TUID version (xxxxxxxxxx-xxxxx-xxxxxxxxxxxxxxx-xxxxxxxxxxxxxxx-xxx-xxxxx)
    1) an internal version for saving data (xxxxxxxxxxxxxxxxxxxx-xxxxx-xxxxxxxxxxxxxxx-xxx)
    2) an very short version (not recommended) (xxxxxxxxxx-xxxxx-xxxxxxx)
    """
    unique = False
    output = str()
    if type == 0:
        id_list = open('data/type0_tuids.dat', 'a+', encoding='utf-8')
        ids = id_list.readlines()

        while unique is False:
            output = ''
            for i in range(10):
                output += secrets.choice(CHARSET)
            output += '-'
            for i in range(5):
                output += secrets.choice(CHARSET)
            output += '-'
            for i in range(15):
                output += secrets.choice(CHARSET)
            output += '-'
            for i in range(15):
                output += secrets.choice(CHARSET)
            output += '-'
            for i in range(3):
                output += secrets.choice(CHARSET)
            output += '-'
            for i in range(5):
                output += secrets.choice(CHARSET)
            if output not in ids:
                unique = True

    if type == 1:
        id_list = open('data/type1_tuids.dat', 'a+', encoding='utf-8')
        ids = id_list.readlines()
        while unique is False:
            output = ''
            for i in range(20):
                output += secrets.choice(CHARSET)
            output += '-'
            for i in range(5):
                output += secrets.choice(CHARSET)
            output += '-'
            for i in range(15):
                output += secrets.choice(CHARSET)
            output += '-'
            for i in range(3):
                output += secrets.choice(CHARSET)
            if output not in ids:
                unique = True

    if type == 1:
        id_list = open('data/type1_tuids.dat', 'a+', encoding='utf-8')
        ids = id_list.readlines()
        while unique is False:
            output = ''
            for i in range(10):
                output += secrets.choice(CHARSET)
            output += '-'
            for i in range(5):
                output += secrets.choice(CHARSET)
            output += '-'
            for i in range(7):
                output += secrets.choice(CHARSET)

            if output not in ids:
                unique = True

    id_list.write(output + '\n')
    id_list.close()
    return output
