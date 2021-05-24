import random
import string
import uuid
import os

def generate_key(key_length: int = 16, key_pattern: str = "x#x#"):
    """
    generates a unique activation key with a length and a pattern
    key_length: length of the key (default 16)
    key_pattern: set of x's and #'s in a string (default "x#x#")
    "x": random letter
    "#": random number
    """
    if key_length % len(key_pattern) == 0:
        alphabet = string.ascii_uppercase
        key = ""
        for _ in range(key_length // len(key_pattern)):
            if _ != 0:
                key += "-"
            for t in key_pattern.lower():
                if t == "x":
                    key += str(random.choice(alphabet))
                elif t == "#":
                    key += str(random.randint(0, 9))
        return key
    return False

def activate(key: str):
    """
    encrypts key 
    key: activation key
    """
    uid = str(uuid.getnode())
    alphabet = string.ascii_uppercase
    activated_key = ""
    for i in range(len(key)):
        if key[i] in alphabet:
            activated_key += alphabet[i + int(uid[i % len(uid)])]
        elif key[i] == "-":
            activated_key += "-"
        else:
            activated_key += str(int(key[i]) + int(uid[i % len(uid)]))
    return activated_key

def generate_keys(amount: int, create_file: bool, previous_keys: list = [], output_file: str = "v1_keys.csv"):
    """
    generates a unique activation key
    amount: how many keys you need
    create_file: true | false
    previous_keys: list of all keys already generated
    output_file: location to put keys in
    """
    added = 0
    previous_keys = list(map(lambda s: s.replace(" ", "").split(",")[0], list(map(lambda s: s.strip(), previous_keys))))
    if create_file:
        if not os.path.exists(output_file):
            open(output_file, "w").close()
        with open(output_file, "a+") as csvfile:
            for _ in range(amount):
                k = generate_key()
                if k not in previous_keys:
                    previous_keys.append(k)
                    csvfile.write(k + "\n")
                    added += 1
            csvfile.close()
    else:
        for _ in range(amount):
            k = generate_key()
            if k not in previous_keys:
                previous_keys.append(k)
                added += 1
    return previous_keys, added

def getkeys(key_file = "v1_keys.csv"):
    """
    retrieves all the keys from a key file
    key_file: file your keys are in
    """
    return list(map(lambda s: s.strip(),  open(key_file, "r").readlines()))
