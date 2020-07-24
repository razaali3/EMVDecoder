import re
        
class Tag():
    def __init__(self, acronym, name, field_length, bit_list):
        self.acronym = acronym
        self.name = name
        self.field_length = field_length
        self.bit_list = bit_list

tags = {
    '95': Tag('TVR', 'Terminal Verification Results', 10, (
    (0x8000000000, 'Offline data authentication was not performed'),
    (0x4000000000, 'SDA failed'),
    (0x2000000000, 'ICC data missing'),
    (0x1000000000, 'Card appears on terminal exception file'),
    (0x0800000000, 'DDA failed'),
    (0x0400000000, 'CDA failed'),
    (0x0080000000, 'ICC and terminal have different application versions'),
    (0x0040000000, 'Expired application'),
    (0x0020000000, 'Application not yet effective'),
    (0x0010000000, 'Requested service not allowed for card product'),
    (0x0008000000, 'New card'),
    (0x0000800000, 'Cardholder verification was not successful'),
    (0x0000400000, 'Unrecognised CVM'),
    (0x0000200000, 'PIN try limit exceeded'),
    (0x0000100000, 'PIN entry required and PIN pad not present or not working'),
    (0x0000080000, 'PIN entry required, PIN pad present, but PIN was not entered'),
    (0x0000040000, 'Online PIN entered'),
    (0x0000008000, 'Transaction exceeds floor limit'),
    (0x0000004000, 'Lower consecutive offline limit exceeded'),
    (0x0000002000, 'Upper consecutive offline limit exceeded'),
    (0x0000001000, 'Transaction selected randomly for online processing'),
    (0x0000000800, 'Merchant forced transaction online'),
    (0x0000000080, 'Default TDOL used'),
    (0x0000000040, 'Issuer authentication failed'),
    (0x0000000020, 'Script processing failed before final GENERATE AC'),
    (0x0000000010, 'Script processing failed after final GENERATE AC'),
    )),
    '9B': Tag('TSI', 'Terminal Status Indicator', 4, (
    (0x8000, 'Offline data authentication was performed'),
    (0x4000, 'Cardholder verification was performed'),
    (0x2000, 'Card risk management was performed'),
    (0x1000, 'Issuer authentication was performed'),
    (0x0800, 'Terminal risk management was performed'),
    (0x0400, 'Script processing was performed'),
    )),
    '82': Tag('AIP', 'Application Interchange Profile', 4, (
    (0x4000, 'SDA supported'),
    (0x2000, 'DDA supported'),
    (0x1000, 'Cardholder verification is supported'),
    (0x0800, 'Terminal risk management is to be performed'),
    (0x0400, 'Issuer authentication is supported'),
    (0x0100, 'CDA supported'),
    )),
    '9F33' : Tag('TC', 'Terminal Capabilities', 6, (
    (0x800000, 'Manual key entry'),
    (0x400000, 'Magnetic stripe'),
    (0x200000, 'IC with contacts'),
    (0x008000, 'Plaintext PIN for ICC verification'),
    (0x004000, 'Enciphered PIN for online verification'),
    (0x002000, 'Signature (paper)'),
    (0x001000, 'Enciphered PIN for offline verification'),
    (0x000800, 'No CVM Required'),
    (0x000080, 'SDA'),
    (0x000040, 'DDA'),
    (0x000020, 'Card capture'),
    (0x000008, 'CDA')
    ))
}

class SimpleTag():
    def __init__(self, name, field_length):
        self.name = name
        self.field_length = field_length
    
simpleTags = {
    '57' : SimpleTag('Track 2 Equivalent Data', 38)
}

def decodeSimpleTags( tag, value ):
    errors = isSimpleValidValue( tag, value )
    if len(errors) != 0:
        print(errors)
        return
    
    if tag not in simpleTags:
        print('%s tag is not valid or not supported' % tag)
        return
    
    tag_data = simpleTags[tag]
    print(tag)
    print(value)
    print(tag_data.name)
    
    
def isSimpleValidValue(tag, value):
    tag_data = simpleTags[tag]
    if tag_data != None and len(value) > tag_data.field_length:
        return '%s must be within %d characters' % (tag, tag_data.field_length)
    if not re.match('^[0-9a-fA-F]+$', value):
        if re.match('^[X]+$', value):
            return '%s contains masked data %s' % (tag, value)
        return '%s must contain only hexadecimal characters. ie 0-9 and A-F.' % tag
    return ()
    
def decode( tag, value ):
    tag = tag.upper()
    
    if tag not in tags:
        decodeSimpleTags( tag, value )
        return
    
    errors = isValidValue(tag, value)
    if len(errors) != 0:
        print(errors)
        return
    
    tag_data = tags[tag]
    set_bits = []
    int_value = int(value, 16)
    for bit in tag_data.bit_list:
        if int_value & bit[0] == bit[0]:
            set_bits.append((('%0' + str(tag_data.field_length) + 'X') % bit[0], bit[1]))
    print(set_bits)
    print(tag)
    print(value)
    print(tag_data.name)
    return
    
    
def isValidValue(tag, value):
    tag_data = tags[tag]
    if tag_data != None and len(value) != tag_data.field_length:
        return '%s must be %d exactly characters long' % (tag, tag_data.field_length)
    if not re.match('^[0-9a-fA-F]+$', value):
        return '%s must contain only hexadecimal characters. ie 0-9 and A-F.' % tag
    return ()

def main():
    decode( '9F33', 'E0F0C0' )
    decode('57', 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

if __name__ == "__main__":
    main()
