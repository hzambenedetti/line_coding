def decode_hdb3(encoded_string):
    binary_list = ['']*len(encoded_string)
    last_polarity = None
    zeros_since_one = 0

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
