"""
Team : Havish Chennamaraj(201201131) and Maripi Pradeep (201201108)
Module :-
"""

import sys


#--------------------------------------- Initializations ----------------------------------------------------------

chunking = []
chunking_word = []
test_lines=[]

#-------------------------------------------------------------------------------------------------------------------



# CFG Rules built from the training data stored in the list "rules"

#rules=["PRP", "NNP", "DT NN NN", "DT NN", "WDT NN", "DT NNS", "CD RB", "DT", "CD", "PRP NN", "PRP NN POS NN", "JJ NN NN", "EX", "VBP", "VBZ", "TO VB", "MD VB", "MD VP", "VB CC VB", "IN NP"]
rules=['NP VP', 'PRP', 'VP PP', 'IN NP', 'TO NP', 'DT NN NN', 'NNP', 'VBZ', 'DT NN', 'DT NNS', 'VBP NP PP', 'IN CD RB', 'TO VB', 'VP S', 'VBP', 'VB', 'VBD', 'VBN', 'MD VP', 'VB CC VB', 'PRP$ NN NN', 'PRP$ NN', 'PRP$ NN POS NN', 'VP', 'VP NP', 'VP RB VP', 'VP RB RB VP', 'VBG', 'NN', 'NNS', 'VP ADJP', 'JJ S', 'NP PP', 'JJ NN NN', 'VP EX', 'WP VP', 'VP RB NP', 'EX VP', 'VB CD', 'WDT NP VP', 'DT VP', 'JJ']

#---------------------------------------------------------------------------------------------------------------------


#-------------------------------------------- Function to return the chunks in the test sentences ------------------------

def return_tag(tag):
    temp=tag.split(" ")
    returntag=temp[0]
    for i in range(1,len(temp)-1):
        returntag += " "+temp[i]
    return returntag

#-----------------------------------------------------------------------------------------------------------------------------


#----------------------------------------- Chunking the test sentence ---------------------------------------------------------

if(len(sys.argv) != 2):
	print "Error : Give proper filename as input !"
	exit(0)

#f=open("./Test/English/Chunking/English_Test_Chunking.txt")
f=open(sys.argv[1])
lines=f.readlines()
for line in lines:
    try:
        temp=line[:-1]
        temp=temp.split(" ")
        test_lines.append(temp)
        build_chunk=""
        build_word=""
        chunking1=[]
        chunking2=[]
        for i in range(len(temp)):
            word_tag=temp[i].split("_")
            word=word_tag[0]
            tag=word_tag[1]
            if(build_chunk==""):
                build_chunk = tag
                build_word = word
            else:
                build_chunk += " " + tag
                build_word += " " + word

            if(build_chunk not in rules):
                #print build_chunk
                if(len(build_chunk.split(" ")) > 1):
                    prev_tag=return_tag(build_chunk)
                    prev_word = return_tag(build_word)
                    build_chunk = tag
                    build_word = word
                else:
                    prev_tag=tag
                    prev_word = word
                    build_chunk = ""
                    build_word = ""
                chunking1.append(prev_tag)
                chunking2.append(prev_word)


        chunking1.append(build_chunk)

        chunking2.append(build_word)
        chunking.append(chunking1)
        chunking_word.append(chunking2)
    except:
        continue
#-----------------------------------------------------------------------------------------------------------------------



#----------------------------------------- Printing the chunked sentence -----------------------------------------------

for i in range(len(chunking_word)):
    for j in chunking_word[i]:
        print "[" + j + "]",
    print

#-----------------------------------------------------------------------------------------------------------------------







