import re
import FileParser
from FileParser import simpleTags
        
class Tag():
    def __init__(self, acronym, name, field_length, bit_list):
        self.acronym = acronym
        self.name = name
        self.field_length = field_length
        self.bit_list = bit_list

tags = {
    '95': Tag('TVR', 'Terminal Verification Results', 10, (
    (0x8000000000, '(Byte 1 Bit 8) Offline data authentication was not performed'),
    (0x4000000000, '(Byte 1 Bit 7) SDA failed'),
    (0x2000000000, '(Byte 1 Bit 6) ICC data missing'),
    (0x1000000000, '(Byte 1 Bit 5) Card appears on terminal exception file'),
    (0x0800000000, '(Byte 1 Bit 4) DDA failed'),
    (0x0400000000, '(Byte 1 Bit 3) CDA failed'),
    (0x0200000000, '(Byte 1 Bit 2) SDA selected'),
    (0x0080000000, '(Byte 2 Bit 8) ICC and terminal have different application versions'),
    (0x0040000000, '(Byte 2 Bit 7) Expired application'),
    (0x0020000000, '(Byte 2 Bit 6) Application not yet effective'),
    (0x0010000000, '(Byte 2 Bit 5) Requested service not allowed for card product'),
    (0x0008000000, '(Byte 2 Bit 4) New card'),
    (0x0000800000, '(Byte 3 Bit 8) Cardholder verification was not successful'),
    (0x0000400000, '(Byte 3 Bit 7) Unrecognised CVM'),
    (0x0000200000, '(Byte 3 Bit 6) PIN try limit exceeded'),
    (0x0000100000, '(Byte 3 Bit 5) PIN entry required and PIN pad not present or not working'),
    (0x0000080000, '(Byte 3 Bit 4) PIN entry required, PIN pad present, but PIN was not entered'),
    (0x0000040000, '(Byte 3 Bit 3) Online PIN entered'),
    (0x0000008000, '(Byte 4 Bit 8) Transaction exceeds floor limit'),
    (0x0000004000, '(Byte 4 Bit 7) Lower consecutive offline limit exceeded'),
    (0x0000002000, '(Byte 4 Bit 6) Upper consecutive offline limit exceeded'),
    (0x0000001000, '(Byte 4 Bit 5) Transaction selected randomly for online processing'),
    (0x0000000800, '(Byte 4 Bit 4) Merchant forced transaction online'),
    (0x0000000080, '(Byte 5 Bit 8) Default TDOL used'),
    (0x0000000040, '(Byte 5 Bit 7) Issuer authentication failed'),
    (0x0000000020, '(Byte 5 Bit 6) Script processing failed before final GENERATE AC'),
    (0x0000000010, '(Byte 5 Bit 5) Script processing failed after final GENERATE AC'),
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

def decodeSimpleTags( tag, value ):    
    if tag not in simpleTags:
        print('%s tag is not valid or not supported' % tag)
        return []

    tag_data = simpleTags[tag]

    return [value, tag_data.name]
    
def decodeBinaryTags( tag, value ):
    
    errors = isValidValue(tag, value)
    if len(errors) != 0:
        print(errors)
        return []
    
    tag_data = tags[tag]
    set_bits = []
    
    int_value = int(value, 16)
    for bit in tag_data.bit_list:
        if int_value & bit[0] == bit[0]:
            set_bits.append( ('%0' + str(tag_data.field_length) + 'X' + ' ' + bit[1] ) % bit[0] )
        
    return [value, tag_data.name, set_bits]

def decodeTags( inputList ):
    super_set_bits = {}
    for x in inputList:
        tag = x[0]
        value = x[1]
        tag = tag.upper()
    
        if tag not in tags:
            tagInfoStr = decodeSimpleTags( tag, value )
            if tagInfoStr != []:
                super_set_bits[tag] = tagInfoStr
            continue
        
        tagInfoList = decodeBinaryTags( tag, value )
        if len( tagInfoList ) != 0:
            super_set_bits[tag] = tagInfoList
        continue
        
    print(super_set_bits)
    
    
def isValidValue(tag, value):
    tag_data = tags[tag]
    if tag_data != None and len(value) != tag_data.field_length:
        return '%s must be %d exactly characters long' % (tag, tag_data.field_length)
    if not re.match('^[0-9a-fA-F]+$', value):
        return '%s must contain only hexadecimal characters. ie 0-9 and A-F.' % tag
    return ()

def main():
    inputList = [('9F33', 'E0F0C0'), ('57', 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'), ('95', 'FFFFFFFFFF'), ('5F2A', '0978')]
    decodeTags(inputList)

if __name__ == "__main__":
    main()
