def decode_hdb3(encoded_string):
    binary_list = ['']*len(encoded_string)
    last_polarity = None
    
    for i, char in enumerate(encoded_string):
        # '+' or '-' char
        if char != '0':
            # repeated polarity == 4 zeros sequence
            if char == last_polarity:
                #detect B00V type sequence
                if binary_list[i-3] != '0':
                    binary_list[i-3] = '0'
                # 000V type sequence
                binary_list[i] = '0'
            else:
                binary_list[i] = '1'
            last_polarity = char
        # '0' char
        else:
            binary_list[i] = '0'

    return ''.join(binary_list)


input_strings = [
    '+0−000−0+−+00+−+−00−000+',
    '+0-000-+000+-+-00-+-+000+-+-+-00-+0-+00+',
    '+-00-+00+00'
]

expected_strings = [
    '101000001100001100000001',
    '1010000100001100001110000111100001010000',
    '10000000000'
]

i = 0
for input, expected in zip(input_strings, expected_strings):
    decoded = decode_hdb3(input).strip()

    print(f"\n TEST {i}\n")
    print(decoded)
    print(expected)
    print()
    if decoded == expected:
        print("decoded == expected: SUCCESS")
