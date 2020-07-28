# Program to show various ways to read and 
# Read data in a file. 

binaryTags = {}

class BinaryTag():
    def __init__(self, acronym, name, field_length, bit_list):
        self.acronym = acronym
        self.name = name
        self.field_length = field_length
        self.bit_list = bit_list

    def writeTagData(self, tagID, tagName, tagDescription, tagSize, bitList ):
        binaryTags[tagID] = BinaryTag( tagName, tagDescription, tagSize, bitList )

file1 = open("BinaryTags.txt","r+") 

lines = file1.readlines()

tagID = ""
tagName = ""
tagDescription = ""
tagSize = 0
hexaCode = ""
hexaCodeDesc = ""
megahexaTagList = []

for line in lines:
    if ( ( line.isspace() == False ) and ( line.find('*') == -1 ) and ( line.find('#') == -1 ) and ( line.find('/') == -1 )) :
        lineList = line.split(':')
        keyStr = lineList[0].strip('\n\t ')

        if ( keyStr == "TagID" ) :
            tagID = lineList[1].strip('\n\t ')
        elif  ( keyStr == "TagName" ) :
            tagName = lineList[1].strip('\n\t ')
        elif  ( keyStr == "TagDescription" ) :
            tagDescription = lineList[1].strip('\n\t ')
        elif  ( keyStr == "TagSize" ) :
            tagSize = int(lineList[1].strip('\n\t '))
        else :
            hexaTagList = line.split(',')
            hexaCode = hexaTagList[0].strip('\n\t ')
            hexaCodeDesc = hexaTagList[1].strip('\n\t ')
            megahexaTagList.append(( int(hexaCode, 16), hexaCodeDesc ))

    elif ( line.find('*') == 0 ) :
        st = BinaryTag('','','',[])
        st.writeTagData(tagID, tagName, tagDescription, tagSize, megahexaTagList.copy() )
        megahexaTagList.clear()

file1.seek(0) 
file1.close()
