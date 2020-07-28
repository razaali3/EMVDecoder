# Program to show various ways to read and 
# Read data in a file. 

simpleTags = {}

class SimpleTag():
    def __init__(self, name):
        self.name = name

    def writeTagData(self, tag, desc):
        simpleTags[tag] = SimpleTag( desc )

file1 = open("SimpleTags.txt","r+") 

print ("Output of Readline function is ")
lines = file1.readlines()
for line in lines:
    if ( ( line.isspace() == False ) and ( line.find('*') == -1 ) and ( line.find('#') == -1 ) and ( line.find('/') == -1 )) :
        lineList = line.split(':')

        tagID = lineList[0].strip('\n\t ')
        tagDesc = lineList[1].strip('\n\t ')

        st = SimpleTag('')
        st.writeTagData(tagID, tagDesc)
        tag_data = simpleTags[tagID]
        print(tagID, tag_data.name)

file1.seek(0) 
file1.close()