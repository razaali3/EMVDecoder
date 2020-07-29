import re
import SimpleTagParser
from SimpleTagParser import simpleTags
import BinaryTagParser
from BinaryTagParser import binaryTags

def decodeSimpleTags( tag, value ):    
    if tag not in simpleTags:
        return [value, '', '%s tag is not valid or not supported' %tag]

    tagData = simpleTags[tag]

    setValues = [value, tagData.name]

    if tagData.desc != '':
        setValues.append( tagData.desc )

    return setValues
    
def decodeBinaryTags( tag, value ):
    
    tagData = binaryTags[tag]
    errors = isValidValue(tag, value)
    if len(errors) != 0:
        return [value, tagData.name, errors]

    setBits = []
    
    intValue = int(value, 16)
    for bit in tagData.bitList:
        if intValue & bit[0] == bit[0]:
            setBits.append( ('%0' + str(tagData.fieldLength) + 'X' + ' ' + bit[1] ) % bit[0] )
        
    return [value, tagData.name, setBits]

def decodeTag9F34(tag, value):

    tagData = binaryTags[tag]

    errors = isValidValue( tag, value )
    if len(errors) != 0:
        return [value, tagData.name, errors]
    

    tag9F34Byte1 = {
        '5E': '5E Signature (paper)',
        '44': '44 Enciphered PIN verification performed by ICC',
        '42': '42 Enciphered PIN verified online',
        '1F': '1F No CVM required',
        '05': '05 Encrypted PIN by ICC + signature',
        '04': '04 Encrypted PIN by ICC',
        '03': '03 Plain PIN by ICC + signature',
        '02': '02 Encrypted PIN online',
        '01': '01 Plain PIN by ICC',
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
        '02': '02 Successful',
        '01': '01 Failed'
    }
    setValues = []
    
    setValues.append( tag9F34Byte1.get( value[0:2], value[0:2] + ' Unknown') )
    setValues.append( tag9F34Byte2.get( value[2:4], value[2:4] + ' Unknown') )
    setValues.append( tag9F34Byte3.get( value[4:6], value[4:6] + ' Unknown') )

    return [value, tagData.name, setValues]

def decodeTags( inputList ):
    superSetBits = {}
    for x in inputList:
        tag = x[0]
        value = x[1]
        tag = tag.upper()

        if tag == '9F34':
            superSetBits[tag] = decodeTag9F34( tag, value )
            continue

        if tag not in binaryTags:
            tagInfoStr = decodeSimpleTags( tag, value )
            superSetBits[tag] = tagInfoStr
            continue
        
        tagInfoList = decodeBinaryTags( tag, value )
        superSetBits[tag] = tagInfoList
        continue

    return superSetBits
    
    
def isValidValue(tag, value):
    tagData = binaryTags[tag]
    if tagData != None and len(value) != tagData.fieldLength:
        return '%s must be exactly %d characters long' % (tag, tagData.fieldLength)
    if not re.match('^[0-9a-fA-F]+$', value):
        return '%s must contain only hexadecimal characters. ie 0-9 and A-F.' % tag
    return ()

def main():
    inputList = [('50', '5649534120435245444954'), ('5A', 'XXXXXXXXXXXXXXXX'), ('5F24', 'XXXXXX'), ('5F25', '090701'), ('5F2A', '0840'),
    ('5F34', '01'), ('82', '5800'), ('84', 'A0000000031010'), ('8A', '3030'), ('8E', '00000000000000001E0302031F00'), 
    ('91', 'E17F5CC000800000'), ('95', '0200888000'), ('9A', '200515'), ('9B', 'E800'), ('9C', '00'), ('9F02', '000000001000'), 
    ('9F03', '000000000000'), ('9F06', 'A0000000031010'), ('9F07', 'FF00'), ('9F08', '0096'), ('9F09', '0096'), ('9F0D', 'F040008800'), 
    ('9F0E', '0010000000'), ('9F0F', 'F040009800'), ('9F10', 'XXXXXXXXXXXXXX'), ('9F11', '01'), ('9F12', '4352454449544F2044452056495341'), 
    ('9F15', '5542'), ('9F1A', '0840'), ('9F1B', '00000000'), ('9F1C', '3031393837333532'), ('9F1E', '3031393837333532'), 
    ('9F21', '115054'), ('9F26', 'DF0BC0A1BE814A49'), ('9F27','80'), ('9F33', '60D8C8'), ('9F34', '020301'), ('9F35', '25'), 
    ('9F36', '0A03'), ('9F37', '3EC4DD7E'), ('9F39', '05'), ('9F40', '6000F01001'), ('9F41', '0003'), ('9F53', '34')]
    result = decodeTags(inputList)
    print(result)

if __name__ == "__main__":
    main()
