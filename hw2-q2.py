import random

def generate_subkeys(key, num_rounds=16):
    subkeys = []
    left_key = key[:64]
    right_key = key[64:]
    
    for i in range(num_rounds):
        left_key = left_key[1:] + left_key[:1]
        right_key = right_key[-1:] + right_key[:-1]
        
        subkey = left_key + right_key
        subkeys.append(subkey[:64])
    
    return subkeys

def s_box(input_bits):
    s_box_table = [
        [0x0, 0x4, 0x8, 0xC],
        [0x1, 0x5, 0x9, 0xD],
        [0x2, 0x6, 0xA, 0xE],
        [0x3, 0x7, 0xB, 0xF]
    ]
    output_bits = ""
    for i in range(0, len(input_bits), 4):
        row = int(input_bits[i:i+2], 2)
        col = int(input_bits[i+2:i+4], 2)
        output_bits += format(s_box_table[row][col], '04b')
    return output_bits

def p_box(input_bits):
    p_box_table = [15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 
                   1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24]
    output_bits = ''.join([input_bits[i] for i in p_box_table])
    return output_bits

def round_function(right, subkey):
    right_expanded = right * 2 
    xored = format(int(right_expanded, 2) ^ int(subkey, 2), '064b')
    substituted = s_box(xored)
    permuted = p_box(substituted)
    return permuted[:32]

def feistel_encrypt(plain_text, key, num_rounds=16):
    subkeys = generate_subkeys(key, num_rounds)
    left = plain_text[:32]
    right = plain_text[32:]
    
    for i in range(num_rounds):
        temp_right = right
        right = format(int(left, 2) ^ int(round_function(right, subkeys[i]), 2), '032b')
        left = temp_right
    
    return left + right

def feistel_decrypt(cipher_text, key, num_rounds=16):
    subkeys = generate_subkeys(key, num_rounds)
    left = cipher_text[:32]
    right = cipher_text[32:]
    
    for i in range(num_rounds-1, -1, -1):
        temp_left = left
        left = format(int(right, 2) ^ int(round_function(left, subkeys[i]), 2), '032b')
        right = temp_left
    
    return left + right

def generate_random_key():
    return ''.join([str(random.randint(0, 1)) for _ in range(128)])

def generate_random_plaintext():
    return ''.join([str(random.randint(0, 1)) for _ in range(64)])

key = generate_random_key()
plain_text = generate_random_plaintext()
cipher_text = feistel_encrypt(plain_text, key)
decrypted_text = feistel_decrypt(cipher_text, key)

print(f"key :  {key}")
print(f"plain_text {plain_text}")
print(f"encrypted_msg :  {cipher_text}")
print(f"decrypted_msg : {decrypted_text}")
