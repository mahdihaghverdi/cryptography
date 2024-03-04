from affine_break import keys, decode, encode

cipher_text = 'طخلهمذهاعهذسذتذعضفخگسمدطشلذیذدطعهسصهص'
for key in keys:
    print(''.join(decode(ct, key) for ct in cipher_text))

plain_text = 'تبریکمیگویمشماموفقبهشکستنرمزمستویشدید'


def find_key():
    for key in keys:
        if ''.join(decode(ct, key) for ct in cipher_text) == plain_text:
            return key


key = find_key()
assert ''.join(encode(pt, key) for pt in plain_text) == cipher_text
