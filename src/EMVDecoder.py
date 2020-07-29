import re
import SimpleTagParser
from SimpleTagParser import simpleTags
import BinaryTagParser
from BinaryTagParser import binaryTags

def decodeSimpleTags( tag, value ):    
    if tag not in simpleTags:
        return [value, '', '%s tag is not valid or not supported' %tag]

    tag_data = simpleTags[tag]

    setValues = [value, tag_data.name]

    if tag_data.desc != '':
        setValues.append( tag_data.desc )

    return setValues
    
def decodeBinaryTags( tag, value ):
    
    tag_data = binaryTags[tag]
    errors = isValidValue(tag, value)
    if len(errors) != 0:
        return [value, tag_data.name, errors]

    set_bits = []
    
    int_value = int(value, 16)
    for bit in tag_data.bit_list:
        if int_value & bit[0] == bit[0]:
            set_bits.append( ('%0' + str(tag_data.field_length) + 'X' + ' ' + bit[1] ) % bit[0] )
        
    return [value, tag_data.name, set_bits]

def decodeTag9F34(tag, value):

    tag_data = binaryTags[tag]

    errors = isValidValue( tag, value )
    if len(errors) != 0:
        return [value, tag_data.name, errors]
    

    tag9F34Byte1 = {
        '5E': '5E Signature (paper)',
        '44': '44 Enciphered PIN verification performed by ICC',
        '42': '42 Enciphered PIN verified online',
        '1F': '1F No CVM required',
        '00': '00 Fail'
    }   

    tag9F34Byte2 = {
        '09': '09 If transaction in application currency and >= Y',
        '08': '08 If transaction in application currency and < Y',
        '07': '07 If transaction in application currency and >= X',
        '06': '06 If transaction in application currency and < X',
        '05': '05 If purchase + cash',
        '04': '04 If manual cash',
        '03': '03 If terminal supports CVM',
        '02': '02 If not (unattended cash, manual cash, purchase + cash)',
        '01': '01 If unattended cash'
    }

    tag9F34Byte3 = {
        '01': '01 Failed',
        '02': '02 Sucessful'
    }
    setValues = []
    
    setValues.append( tag9F34Byte1.get( value[0:2], value[0:2] + ' Unknown') )
    setValues.append( tag9F34Byte2.get( value[2:4], value[2:4] + ' Unknown') )
    setValues.append( tag9F34Byte3.get( value[4:6], value[4:6] + ' Unknown') )

    return [value, tag_data.name, setValues]

def decodeTags( inputList ):
    super_set_bits = {}
    for x in inputList:
        tag = x[0]
        value = x[1]
        tag = tag.upper()

        if tag == '9F34':
            super_set_bits[tag] = decodeTag9F34( tag, value )
            continue

        if tag not in binaryTags:
            tagInfoStr = decodeSimpleTags( tag, value )
            super_set_bits[tag] = tagInfoStr
            continue
        
        tagInfoList = decodeBinaryTags( tag, value )
        super_set_bits[tag] = tagInfoList
        continue

    print(super_set_bits)
    
    
def isValidValue(tag, value):
    tag_data = binaryTags[tag]
    if tag_data != None and len(value) != tag_data.field_length:
        return '%s must be exactly %d characters long' % (tag, tag_data.field_length)
    if not re.match('^[0-9a-fA-F]+$', value):
        return '%s must contain only hexadecimal characters. ie 0-9 and A-F.' % tag
    return ()

def main():
    inputList = [('9F33', 'E0F0C0'), ('57', 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'), ('95', 'FFFFFFFFFF'), ('5F2A', '0978'), ('82', '2000'), ('9F34', '1F0002'), ('8E', '00000000000000004201410342031E031F00')]
    decodeTags(inputList)

if __name__ == "__main__":
    main()
