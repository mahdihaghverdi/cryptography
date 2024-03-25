from affine_break import keys, decrypt, encrypt

cipher_text = 'طخلهمذهاعهذسذتذعضفخگسمدطشلذیذدطعهسصهص'
for key in keys:
    print(decrypt(cipher_text, key))

plain_text = 'تبریکمیگویمشماموفقبهشکستنرمزمستویشدید'


def find_key():
    for key in keys:
        if decrypt(cipher_text, key) == plain_text:
            return key


key = find_key()
print(key)
assert encrypt(plain_text, key) == cipher_text
