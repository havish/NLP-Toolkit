import re

import operator
import re


#--------------------------- File name assigning -----------------------------------

input_file="TEL_TOY.txt"
ff=open('TEL_TOY.txt')
unigram_file=open('Telugu_unigrams.txt','r')
bigram_file=open('Telugu_bigrams.txt','r')
trigram_file= open('Telugu_trigrams.txt','r')
eng_sent = open("tel_sent.txt",'r')

#----------------------------------------------------------------------------

# abbv - (?:[A-Z]\.)+
# decimal - [-+$]?\d*\.\d+|\d+
# URL - https?://[^\s<>\"]+|www\.[^\s<>\"]+

abbv=re.compile(r'(?:[A-Z]\.)+')
decimal = re.compile(r'[-+$]?\d*\.\d+|\d+')
URL=re.compile(r'https?://[^\s<>\"]+|www\.[^\s<>\"]+')
final_split=re.compile(r"\w+(?:[-']\w+)*|'|\"|[-.(]+|\S\w*")

punctuations=[',','!','(',')','|',';','?','"','[',']','{','}','_','\\','>','<']

# Exceptional cases
# . , : , ' ,

result = {}
exceptional_cases = ['.',':']
bow=[]

result1={}
result2={}

def insert(word):
    if(word != ""):
       bow.append(word)


def insert_dic(word):
    try:
        result[word] += 1
    except:
        result[word] = 1

def insert_dic1(word):
    try:
        result1[word] += 1
    except:
        result1[word] = 1

def insert_dic2(word):
    try:
        result2[word] += 1
    except:
        result2[word] = 1


f=open(input_file)
lines=f.readlines()

#tel_sent=open('hin_sent.txt','w')


quote="'"

sent_uni=[]
sent_bi=[]
sent_tri=[]


for line in lines:
    temp=line.replace("\n","")

    for i in punctuations:
            temp=temp.replace(i," "+i+" ")

    temp=" " + temp + " "
    token=""
    for i in range(len(temp)):
        if(temp[i] == "."):
            if((temp[i-1].isalpha() and temp[i+1].isalpha()) or (temp[i-1].isdigit() and temp[i+1].isdigit())):
                token += temp[i]
            elif(i>=2 and temp[i-2]=='.'):
                token += temp[i]
            else:
                token += " " + temp[i] + " "
        elif(temp[i]==':'):
            if(token.find('http')!=-1 or token.find('www')!=-1):
                token+=temp[i]
            elif((temp[i-1].isdigit()) and ( temp[i+1].isdigit())):
                token+=temp[i]
            else:
                token += " " + temp[i] + " "
        elif(temp[i] == '-'):
            if((temp[i-1].isalpha() or temp[i-1].isdigit()) and (temp[i+1].isalpha() or temp[i+1].isdigit())):
                token+=temp[i]
            else:
                token += " " + temp[i] + " "
        elif(temp[i]==quote):
            if((temp[i-1].isalpha() or temp[i-1].isdigit()) and (temp[i+1].isalpha() or temp[i+1].isdigit())):
                token+=temp[i]
            else:
                token += " " + temp[i] + " "
        elif(temp[i] == '*'):
            if(temp[i-1].isalpha() or temp[i-1].isdigit() or temp[i+1].isalpha() or temp[i+1].isdigit()):
                token += temp[i]
            else:
                token += " " + temp[i] + " "
        else:
            token += temp[i]
    token = token.split(' ')

    for i in token:
        insert(i)
        #tel_sent.write(str(i) + " ")
    #tel_sent.write("\n")

for i in bow:
    insert_dic(i)
Unigram = sorted(result.iteritems(), key=operator.itemgetter(1),reverse=True)


for i in range(len(bow)-1):
    insert_dic1(bow[i] + " " + bow[i+1])
Bigram = sorted(result1.iteritems(), key=operator.itemgetter(1),reverse=True)


for i in range(len(bow) - 2):
    insert_dic2(bow[i] + " " + bow[i+1] + " " + bow[i+2])
Trigram = sorted(result2.iteritems(), key=operator.itemgetter(1),reverse=True)



#--------------------------------------------------------- ^Tokenizer^ --------------------------------------------------------------



#---------------------------------------- Initializations -----------------------


unique_unigrams =0
unique_bigrams = 0
unique_trigrams = 0
N=0
N_bi = 0
N_tri = 0

a_uni=0
a_bi=0
a_tri=0

unicount={}
unigram_mle={}

bicount={}
bigram_mle={}

tricount={}
trigram_mle={}



for line in unigram_file:
    temp=line.split(" ")
    a_uni= int(temp[2])
    break

for line in bigram_file:
    temp=line.split(" ")
    a_bi = int(temp[3])
    break

for line in trigram_file:
    temp=line.split(" ")
    a_tri = int(temp[4])
    break

#-------------------------------------------------------------------------------------------------------------------

#------------------------------------------ Preparing Training Data ------------------------------------------------------------------------


unigram_turing={}
bigram_turing = {}
trigram_turing = {}

for i in range(1,a_uni+2):
    unigram_turing[str(i)]=0

for i in range(1,a_bi+2):
    bigram_turing[str(i)] = 0

for i in range(1,a_tri+2):
    trigram_turing[str(i)] = 0



unigram_file.seek(0)
bigram_file.seek(0)
trigram_file.seek(0)

for line in unigram_file:
    unique_unigrams += 1
    temp=line.split(' ')
    unicount[temp[1]]=int(temp[2])
    N += int(temp[2])
    unigram_turing[str(int(temp[2]))] += 1


for line in bigram_file:
    unique_bigrams += 1
    temp=line.split()
    bicount[temp[1]+' '+temp[2]]=int(temp[3])
    N_bi += int(temp[3])
    bigram_turing[str(int(temp[3]))] += 1


for line in trigram_file:
    unique_trigrams += 1
    temp=line.split()
    tricount[temp[1]+' '+temp[2]+' '+temp[3]]=int(temp[4])
    N_tri += int(temp[4])
    trigram_turing[str(temp[4])] += 1



#-------------------------------------------------- Laplace Smoothing--------------------------------------------------------

unigram_file.seek(0)
unigram_laplace = {}


for i in range(len(Unigram)):
    temp=Unigram[i][0]
    try:
        unigram_laplace[temp] = (float(unicount[temp]) + 1 )/ (float(N) + float(unique_unigrams))
    except:

        unigram_laplace[temp] = 1/(float(N) + float(unique_unigrams))



bigram_file.seek(0)
bigram_laplace={}

for i in range(len(Bigram)):
    temp=Bigram[i][0]
    temp1 = temp.split(" ")[0]
    try:
        bigram_laplace[temp] = (float(bicount[temp]) + 1 )/ (float(unicount[temp1]) + unique_unigrams )
    except:
        try:
            bigram_laplace[temp] = ( 1 )/ (float(unicount[temp1]) + unique_unigrams )
        except:
            bigram_laplace[temp] = (1) / (float(unique_unigrams))



trigram_file.seek(0)
trigram_laplace={}



for i in range(len(Trigram)):
    temp=Trigram[i][0]
    temp1 = temp.split(" ")
    temp1 = temp1[0] + temp1[1]
    try:
        trigram_laplace[temp] = (float(tricount[temp]) + 1 )/ (float(bicount[temp1]) + unique_unigrams )
    except:
        try:
            trigram_laplace[temp] = ( 1 )/ (float(bicount[temp1]) + unique_unigrams )
        except:
            trigram_laplace[temp] = 1 / (float(unique_unigrams))




#---------------------------------Good Turing smoothing -----------------------------------#


"""B_uni = float(unigram_turing['2']) / float(unigram_turing['1'])
A_uni = float(unigram_turing['1']) / float(B_uni)

print A_uni , B_uni"""

unigram_turing1={}
bigram_turing1={}
trigram_turing1={}


for i in range(len(Unigram)):
    word=Unigram[i][0]
    try:
        c = unicount[word]
        numerator = unigram_turing[str(c+1)]
        if(numerator == 0):
            for j in range(c+2 , a_uni + 1):
                if(unigram_turing[str(j)] !=0 ):
                    numerator = unigram_turing[str(j)]
                    break
        c_rev = (float(numerator) / float(unigram_turing[str(c)])) * (c+1)
        unigram_turing1[word] = float(c_rev) / float(N)
    except:
        unigram_turing1[word] = float(unigram_turing['1']) / float (N)

for i in range(len(Bigram)):
    word=Bigram[i][0]
    try:
        c=bicount[word]
        numerator = bigram_turing[str(c+1)]
        if(numerator == 0):
            for j in range(c+2 , a_bi + 1):
                if(bigram_turing[str(j)] != 0):
                    numerator = bigram_turing[str(j)]
                    break
        c_rev = ( float(numerator) / float(bigram_turing[str(c)]) ) * (c+1)
        bigram_turing1[word] = float(c_rev) / float(N_bi)
    except:
        bigram_turing1[word] = float(bigram_turing['1']) / float(N_bi)


for i in range(len(Trigram)):
    word=Trigram[i][0]
    try:
        c=tricount[word]
        numerator = trigram_turing[str(c+1)]
        if(numerator == 0):
            for j in range(c+2 , a_tri + 1):
                if(trigram_turing[str(j)] != 0):
                    numerator = trigram_turing[str(j)]
                    break
        c_rev = ( float(numerator) / float(trigram_turing[str(c)]) ) * (c+1)
        trigram_turing1[word] = float(c_rev) / float(N_tri)
    except:
        trigram_turing1[word] = float(trigram_turing['1']) / float(N_tri)



#--------------------------------- Calculating Likelihood of sentences -----------------------------



lines=eng_sent.readlines()
for line in lines:
    line1=line.strip()
    temp1=line1.split(" ")
    temp=[]
    for x in temp1:
        if(x!=""):
            temp.append(x)
    sent_uni.append(temp)
    bow=[]
    for i in range(len(temp)-1):
        bow.append(temp[i] + " " + temp[i+1])
    sent_bi.append(bow)
    bow=[]
    for i in range(len(temp) - 2):
        bow.append(temp[i] + " " + temp[i+1] + " " + temp[i+2])
    sent_tri.append(bow)


laplace_uni=[]
turing_uni=[]
laplace_bi=[]
turing_bi=[]
laplace_tri=[]
turing_tri=[]



for i in sent_uni:
    p=1
    q=1
    for j in i:
        p *= unigram_turing1[j]
        q *= unigram_laplace[j]
    laplace_uni.append(q)
    turing_uni.append(p)

for i in sent_bi:
    p=1
    q=1
    for j in i:
        p *=  bigram_turing1[j]
        q *=  bigram_laplace[j]
    laplace_bi.append(q)
    turing_bi.append(p)

backoff_lap=[]
backoff_turing=[]

for i in sent_tri:
    p=1
    q=1
    t=1
    s=1
    for j in i:
        test = j.split()
        bigram_word = test[1] + " "  +test[2]
        unigram_word = test[0]
        p *= trigram_turing1[j]
        q *= trigram_laplace[j]
        t = t*(0.5*trigram_laplace[j] + 0.3*bigram_laplace[bigram_word] + 0.2*unigram_laplace[unigram_word])
        s = s*(0.5*trigram_turing1[j] + 0.3*bigram_turing1[bigram_word] + 0.2*unigram_turing1[unigram_word])
    laplace_tri.append(p)
    turing_tri.append(q)
    backoff_lap.append(t)
    backoff_turing.append(s)


#------------------------------------ Printing Likelihood ------------------------------------------------



print_lines = ff.readlines()

for i in range(len(print_lines)):
    print print_lines[i]
    print 'Laplace Unigram Likelihood'
    print laplace_uni[i]
    print 'Good-Turing Unigram Likelihood'
    print turing_uni[i]
    print 'Laplace Bigram Likelihood'
    print laplace_bi[i]
    print 'Good-Turing Bigram Likelihood '
    print turing_bi[i]
    print 'Laplace Trigram Likelihood'
    print laplace_tri[i]
    print 'Good-Turing Trigram Likelihood'
    print turing_tri[i]
    print 'Laplace with backoff'
    print backoff_lap[i]
    print 'Turing with backoff'
    print backoff_turing[i]
    print
    print


