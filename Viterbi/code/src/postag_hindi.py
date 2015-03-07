#------------------------------------------- Import libraries here -----------------------------------------------

import operator
from collections import OrderedDict
import re,sys,copy


if(len(sys.argv) != 2):
	print "Please give proper file as input"
	exit(0)

#-------------------------------------------------------------------------------------------------------------------

#----------------------------------------------- Data initialization ------------------------------------------------

training_file=open("./../src/hindi.txt")
training_lines = training_file.readlines()


emission={}
transmission_unigram={}
transmission_bigram={}
transmission_trigram={}

transmission_unigram['*'] = len(training_lines)
transmission_unigram["STOP"] = len(training_lines)

transmission_trigram_laplace={}
emission_laplace = {}

unicount={}
bicount={}
tricount={}
N_transmission = len(transmission_unigram.keys())
N_emission = 0

unique_tags={}
S={}
tags={}

punctuation = ['.',';',':','-','_','(',')','{','}','[',']','\'','"','?','!','/','|',',','%','$','#','@','^','&','*','+','=' ]

#----------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------  Function used to obatain all distinct TAGS from training data ---------
def prepare_tags():
    for line in training_lines:
    	temp = line[line.find("\"")+2:-2]
        if(len(temp)==0):
		break
    	if(temp[-1] == '"'):
		temp = temp[:-1]
	word_tag1 = temp.split(" ")
        word_tag=[]


        for i in word_tag1:
            if(len(i.split("_")) == 2):
                word_tag.append(i)

        for iter in range(len(word_tag)):
            temp_tag = word_tag[iter].split("_")
            TAG = temp_tag[1]
            try:
                unique_tags[TAG] = 1
            except:
                unique_tags[TAG] += 1
    s=[]
    for i in unique_tags.keys():
        s.append(i)
    for i in range(100):
        S[str(i)] = s
    S["-1"] = ["*"]
    S["-2"] = ["*"]

#-----------------------------------------------------------------------------------------------------------------------------

#---------------------------------- Functions to be used while buliding transition and emission probabilites -----------------


def insert_emission(word,tag):
    emission[word][tag] += 1


def insert_transmissionUnigram(tag):
    try:
        transmission_unigram[tag] += 1
    except:
        transmission_unigram[tag] = 1

def insert_transmissionBigram(before_tag,tag):
    transmission_bigram[before_tag][tag] += 1

def insert_transmissionTrigram(before_tags,tag):
    transmission_trigram[before_tags][tag] += 1

#--------------------------------------------------------------------------------------------------------------------------------------



prepare_tags()  #------------------------------ Function call for getting all the distict Tags in the training data -----------------


#--------------------------------------- Initializing datastructures used to compute the transition and emission probabilities ------

tag_set = S['0'] + ["*","STOP"]
for i in tag_set:
    tags[i]=[]


for i in tag_set:
    transmission_trigram[i] = {}
    for j in tag_set:
        for k in tag_set:
            transmission_trigram[i][j + " " + k]=0

for i in tag_set:
    transmission_bigram[i] = {}
    for j in tag_set:
        transmission_bigram[i][j] = 0


def dic_tags():
    dic={}
    for i in tag_set:
        dic[i]=0
    return dic
#----------------------------------------------------------------------------------------------------------------------------------------------



#--------------------------------------------- Getting the training data and storing it ----------------------------------------------------------
for line in training_lines:
    temp = line[line.find("\"")+2:-2]
    if(len(temp)==0):
	    break
    if(temp[-1] == '"'):
	    temp = temp[:-1]


    #print temp
    #temp = line.split(" \" ")[1][:-2]
    word_tag1 = temp.split(" ")
    word_tag=[]


    for i in word_tag1:
        if(len(i.split("_")) == 2):
            word_tag.append(i)

    for iter in range(len(word_tag)):
        temp_tag = word_tag[iter].split("_")
        WORD = temp_tag[0]
        TAG = temp_tag[1]

        try:
            emission[WORD]
        except:
            emission[WORD]=dic_tags()
        insert_emission(WORD,TAG)  # recording training data pertaining to emission probability

        insert_transmissionUnigram(TAG)

        #------------------------ Recording training data pertaining to transition probability ----------------------------

        if(iter==0):
            tags["*"].append(TAG)
            insert_transmissionBigram("*",TAG)
        else:
            tags[word_tag[iter-1].split("_")[1]].append(TAG)
            insert_transmissionBigram(word_tag[iter-1].split("_")[1],TAG)

        #-----------------------------------------------------------------------------------------------------------------

    tags[word_tag[iter-1].split("_")[1]].append("STOP")
    insert_transmissionBigram(word_tag[iter-1].split("_")[1],"STOP")

#--------------------------------------------------------------------------------------------------------------------------------


#---------------------------------- Computing the transition probabilites and storing them in a 2D array "transmission_bigram" --------
for i in transmission_bigram:
    transmission_bigram[i]['sum'] = 0
    for j in transmission_bigram[i]:
        transmission_bigram[i]['sum'] += transmission_bigram[i][j]



for i in transmission_bigram:
    for j in transmission_bigram[i]:
        try:
            transmission_bigram[i][j] = transmission_bigram[i][j] / float(transmission_unigram[i] * 1.0)
        except:
            transmission_bigram[i][j] = 0

#----------------------------- Computing the emission probabilities and storing them in a 2D array "emission" ---------------------
for i in emission:
    for j in emission[i]:
        emission[i][j] = emission[i][j] / float(transmission_unigram[j] * 1.0)
#---------------------------------------------------------------------------------------------------------------------------------


#------------------------------------------ Initializations for viterbi ----------------------------------------------------
tags1 = S['0']
TAGS = S['0']
emis = emission
trans = transmission_bigram
#----------------------------------------------------------------------------------------------------------------------------


#--------------------------- Functions used in the viterbi algorithms -------------------------------------------------------
def MAXTAG_transmission(before_tag):
        tmp = ""
        maax  = 0.0
        for tag in tags1:
            if(maax <= trans[before_tag][tag]):
                maax = trans[before_tag][tag]
                tmp = tag
        return tmp

def MAXTAG_v(v,word):
            mx = 0.0
            for tt in tags1:
                if(mx <= v[word][tt]):
                    mx = v[word][tt]
                    tmp_tg = tt
            return tmp_tg

def create_path(before_tag,tag,path):
    a=[]
    for j in path[before_tag]:
        a.append(j)
    a.append(tag)
    return a
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------ Viterbi Algorithm -----------------------------------------------------------

def viterbi(obs,tags,start_p,trans,emis,path):
    v = dict()
    v[obs[0]] = copy.deepcopy(start_p)
    for i in range(1,len(obs)):
        a = dict()
        temp_path = dict()
        if obs[i] not in emis:

            tmp_tg = MAXTAG_v(v,obs[i-1])

            temp = MAXTAG_transmission(tmp_tg)


            for tt in tags1:
                if(tt!=temp):
                    a[tt] = 0.0
                else:
                    a[tt] = v[obs[i-1]][tmp_tg]*trans[tmp_tg][temp]*(1.0/(len(emission.keys())*1.0));


                temp_path[tt] = []
                for j in path[tmp_tg]:
                    temp_path[tt].append(j)
                temp_path[tt].append(tt)
            v[obs[i]] = copy.deepcopy(a)
            path = copy.deepcopy(temp_path)
        else:
            for tag in tags1:
                maax = 0.0
                temp_tag = copy.deepcopy(tag)
                for tag1 in tags1:
                    if(maax <= v[obs[i-1]][tag1]*trans[tag1][tag]*emis[obs[i]][tag] ):
                        maax = v[obs[i-1]][tag1]*trans[tag1][tag]*emis[obs[i]][tag];
                        temp_tag = copy.deepcopy(tag1);
                a[tag] = maax
                temp_path[tag] = []
                for j in path[temp_tag]:
                    temp_path[tag].append(j)
                temp_path[tag].append(tag)
            flag = 0
            for pp in a:
                if(a[pp]!=0):
                    flag = 1
            if(flag==0):
                flag = 0
                for pp in v[obs[i-1]]:
                    if(v[obs[i-1]][pp]!=0):
                        flag = 1
                if(flag == 1):
                    maax = 0.0
                    for x in v[obs[i-1]]:
                        if(maax <= v[obs[i-1]][x]):
                            maax = v[obs[i-1]][x]
                            er = x
                    temp_path = dict()
                    for qwe in tags1:
                        temp_path[qwe]=[]
                        for df in path[er]:
                            temp_path[qwe].append(df)
                        temp_path[qwe].append(qwe)
            v[obs[i]] = copy.deepcopy(a)
            path = copy.deepcopy(temp_path)
    maax = 0.0
    q = v[obs[len(obs)-1]]
    flag = 0
    for asd in q:
        if(q[asd]!=0):
            flag = 1
        for s in q:
            if(maax <= q[s]):
                maax = q[s];
                final_tag = s
        return path[final_tag]

#-------------------------------------------------------------------------------------------------------------------------------------------

def output_ans(line,ans):
    temp = line[:line.find("\"")]
    temp=temp.replace("test_","")
    print temp+ans



#----------------------------------- Running test data on viterbi algorithm ------------------------------------------------------------------



test = open(str(sys.argv[1]),"r")
test_lines = test.readlines()
for line in test_lines:
    line1=line
    temp=line
    if(len(temp) <= 2 ):
	    break
    if(temp[-1] == "\n"):
	    temp=temp[:-1]
    temp = line[line.find("\"")+2:-2]
    if(temp[-1] == ' ' or temp[-1] == '"'):
        	temp=temp[:-1]
    line = temp.split()
    temp_line = copy.deepcopy(line)
    start_p = dict()
    path = dict()
    if line[0] not in emis:
        #		print "no "+line[0]
        tmp = ""

        tmp=MAXTAG_transmission("*")
        for tag in tags1:
            if(tag == tmp):
                start_p[tag] = trans['*'][tag]*(1.0/(len(emission.keys())*1.0))
            else:
                start_p[tag] = 0.0
            path[tag] = [tag]
        emis[line[0]] = start_p
    else:
        for tag in tags1:
            start_p[tag] = trans['*'][tag]*emis[line[0]][tag]
            path[tag] = [tag]
    p = viterbi(line,tags,start_p,trans,emis,path);
    output="\" "
    for i in range(0,len(p)):
        if(line[i] in  punctuation):
            output += line[i]+"_SYM "
        else:
            output += line[i]+"_"+p[i] + " "
    output += "\""
    output_ans(line1,output)
test.close()

#---------------------------------------------------------------------------------------------------------------------------------------------------------
