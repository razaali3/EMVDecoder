import re
import SimpleTagParser
from SimpleTagParser import simpleTags
import BinaryTagParser
from BinaryTagParser import binaryTags


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
    
    tag_data = binaryTags[tag]
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
    
        if tag not in binaryTags:
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
    tag_data = binaryTags[tag]
    if tag_data != None and len(value) != tag_data.field_length:
        return '%s must be %d exactly characters long' % (tag, tag_data.field_length)
    if not re.match('^[0-9a-fA-F]+$', value):
        return '%s must contain only hexadecimal characters. ie 0-9 and A-F.' % tag
    return ()

def main():
    inputList = [('9F33', 'E0F0C0'), ('57', 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'), ('95', 'FFFFFFFFFF'), ('5F2A', '0978'), ('82', '2000')]
    decodeTags(inputList)

if __name__ == "__main__":
    main()
