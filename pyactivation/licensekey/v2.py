import random
import string
from datetime import date
import os


def generate_randomkey(product_number, expiration_date):
    """
    generates a unique activation key for a specific product using random numbers
    product_number: number id of the product
    expiration date: "mm/dd/yyyy" or "mm-dd-yyyy" 
    """
    if product_number < 99 and product_number >= 1:
        if "/" in expiration_date:
            date = list("".join(expiration_date.split("/")))
        elif "-" in expiration_date:
            date = list("".join(expiration_date.split("-")))
        else:
            return None
        alphabet = string.ascii_uppercase
        key = ""
        if product_number < 10:
            product_number = list("0" + str(product_number))
        else:
            product_number = list(str(product_number))
        b_key = "{}{}{}{}-{}{}{}{}-{}{}{}{}-{}{}{}{}".format(
            product_number[0], 
            product_number[1],
            date[-2],
            date[-1],
            random.randint(0, 9),
            random.randint(0, 9),
            date[-8],
            date[-7],
            random.randint(0, 9),
            random.randint(0, 9),
            date[-6],
            date[-5],
            random.randint(0, 9),
            random.randint(0, 9),
            date[-4],
            date[-3],)
        for i in b_key:
            if i == "-":
                key += i
            elif random.randint(0, 1) == 0:
                key += alphabet[int(i)]
            else:
                key += i
        return key
    else:
        return None

def generate_incrementedkey(key_num: int, product_number: int, expiration_date: str):
    """
    generates a unique activation key for a specific product using increments
    key_num: number of the key to start on
    product_number: number id of the product
    expiration date: "mm/dd/yyyy" or "mm-dd-yyyy" 
    """
    if product_number < 99 and product_number >= 1:
        if "/" in expiration_date:
            date = list("".join(expiration_date.split("/")))
        elif "-" in expiration_date:
            date = list("".join(expiration_date.split("-")))
        else:
            return None
        alphabet = string.ascii_uppercase
        key = ""
        if product_number < 10:
            product_number = list("0" + str(product_number))
        else:
            product_number = list(str(product_number))
        oldkey_num = str(key_num)
        key_len = len(oldkey_num)
        if key_len < 6:
            key_num = ""
            for _ in range(6 - key_len):
                key_num += "0"
            key_num += oldkey_num
        b_key = "{}{}{}{}-{}{}{}{}-{}{}{}{}-{}{}{}{}".format(
            product_number[0], 
            product_number[1],
            date[-2],
            date[-1],
            int(key_num[0]),
            int(key_num[1]),
            date[-8],
            date[-7],
            int(key_num[2]),
            int(key_num[3]),
            date[-6],
            date[-5],
            int(key_num[4]),
            int(key_num[5]),
            date[-4],
            date[-3],)
        for i in b_key:
            if i == "-":
                key += i
            elif random.randint(0, 1) == 0:
                key += alphabet[int(i)]
            else:
                key += i
        return key
    else:
        return None

def validate(key: str):
    """
    checks to see if key is expired
    key: activation key
    """
    try:
        today = date.today()
        b_key = ""
        alphabet = string.ascii_uppercase
        for i in key:
            if i == "-":
                b_key += i
            elif i in alphabet:
                b_key += str(alphabet.index(i))
            else:
                b_key += i
        split = b_key.split("-")
        exp = date(int(split[3][-2] + split[3][-1] + split[0][-2] + split[0][-1]), int(split[1][-2] + split[1][-1]), int(split[2][-2] + split[2][-1]))
        if (exp - today).days >= 0:
            return today < exp, (exp - today).days
        else:
            return today < exp, 0
    except:
        return None, None

def generate_randomkeys(expiration_date: str, amount: int, product_number:int = 1, previous_keys: list = [], output_file: str = "keys.csv"):
    """
    generates a unique activation key for a specific product using random increments
    expiration date: "mm/dd/yyyy" or "mm-dd-yyyy"
    amount: how many keys you need
    product_number: number id of the product
    previous_keys: list of all keys already generated
    output_file: location to put keys in
    """
    added = 0
    previous_keys = list(map(lambda s: s.replace(" ", "").split(",")[0], list(map(lambda s: s.strip(), previous_keys))))
    if not os.path.exists(output_file):
        open(output_file, "w").close()
    with open(output_file, "a+") as csvfile:
        for _ in range(amount):
            k = generate_randomkey(product_number, expiration_date)
            if k not in previous_keys:
                previous_keys.append(k)
                csvfile.write("{}, {}\n".format(k, expiration_date))
                added += 1
        csvfile.close()
        return previous_keys, added

def generate_incrementedkeys(expiration_date, amount, product_number = 1, previous_keys = [], output_file = "v2_keys.csv"):
    """
    generates a unique activation key for a specific product at an increment
    expiration date: "mm/dd/yyyy" or "mm-dd-yyyy"
    amount: how many keys you need
    product_number: number id of the product
    previous_keys: list of all keys already generated
    output_file: location to put keys in
    """
    added = 0
    previous_keys = list(map(lambda s: s.replace(" ", "").split(",")[0], list(map(lambda s: s.strip(), previous_keys))))
    key_num = len(previous_keys) + 1
    if not os.path.exists(output_file):
        open(output_file, "w").close()
    with open(output_file, "a+") as csvfile:
        for _ in range(amount):
            k = generate_incrementedkey(key_num, product_number, expiration_date)
            if k not in previous_keys:
                previous_keys.append(k)
                csvfile.write("{}, {}\n".format(k, expiration_date))
                added += 1
        csvfile.close()
        return previous_keys, added
    
def getkeys(key_file = "v2_keys.csv"):
    """ 
    retrieves all the keys from a key file
    key_file: file your keys are in
    """
    return list(map(lambda s: s.replace(" ", "").split(",")[0], list(map(lambda s: s.strip(),  open(key_file, "r").readlines()))))

