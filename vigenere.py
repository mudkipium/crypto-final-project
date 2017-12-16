def get_shifts(key):
    char_list = list(key.lower())
    shifts = []
    for c in char_list:
        shifts.append(c - 'a')
    return shifts


def vigenere_encrypt(key, filepath):
    key = get_shifts(key)
