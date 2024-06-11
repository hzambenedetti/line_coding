

def encode_ascii(string):
    string_ascii = [0]*len(string)
    
    for i, char in enumerate(string):
        string_ascii[i] = ord(char)

    return string_ascii


def encode_binary(string):
    string_ascii = encode_ascii(string)
    bin_list = ['']*len(string_ascii)
    
    for i, char in enumerate(string_ascii):
        bin_list[i] = '{0:08b}'.format(char)

    bin_string = ''.join(bin_list)
    
    return bin_string



def opposite(polarity):
    if polarity == '+':
        return '-'
    return '+'

def encode_hdb3(bits_string):
    #initial assumptions:
    # The previous 1 bit was '-'
    # The last violation bit was an even number of 1 bits ago
    next_polarity = '+'
    ones_count = 1
    
    consecutive_zeros = 0
    encoded_list = ['']*len(bits_string)

    for i, bit in enumerate(bits_string):
        if bit == '1':
            ones_count += 1
            consecutive_zeros = 0
            encoded_list[i] = next_polarity
            next_polarity = opposite(next_polarity)
        
        else:
            consecutive_zeros += 1
            # 4 consecutive zeros found requires bit substitution
            if consecutive_zeros == 4:
                consecutive_zeros = 0
                
                #Even number of ones since last violation
                if ones_count % 2 == 0:
                    #substitute '0000' by 'B00V' B and V will be the opposite of the last used polarity (and thus the next_polarity) 
                    encoded_list[i-3] = next_polarity
                    encoded_list[i] = next_polarity
                    next_polarity = opposite(next_polarity)
                else:
                    #substitute '0000' by '000V' where V is the current next next_polarity
                    # we repeat the last polarity
                    encoded_list[i] = opposite(next_polarity)

                ones_count = 0
            else:
                encoded_list[i] = '0'

    return ''.join(encoded_list)

string ='1010000100001100001110000111100001010000' 
expected ='+0-000-+000+-+-00-+-+000+-+-+-00-+0-+00+' 
encoded = encode_hdb3(string).strip()

print(encoded)
print(expected)

print(len(encoded))
print(len(expected))

if encoded == expected: 
    print('aaaa')


