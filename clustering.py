
import sys, math, random
import re
import operator
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


f=open('Telugu.txt')
lines=f.readlines()


quote="'"
print quote



for line in lines:
    temp=line.replace("\n","")

    for i in punctuations:
            temp=temp.replace(i," "+i+" ")

    temp=" " + temp + " "
    token=""
    for i in range(len(temp)):
        if(temp[i] == ' '):
            insert(token)
            token=""
        elif(temp[i] in punctuations):
            insert(token)
            insert(temp[i])
            token=""
        elif(temp[i] == "."):
            if((temp[i-1].isalpha() and temp[i+1].isalpha()) or (temp[i-1].isdigit() and temp[i+1].isdigit())):
                token += temp[i]
            elif(i>=2 and temp[i-2]=='.'):
                token += temp[i]
            else:
                insert(token)
                insert(".")
                token=""
        elif(temp[i]==':'):
            if(token.find('http')!=-1 or token.find('www')!=-1):
                token+=temp[i]
            elif((temp[i-1].isdigit()) and ( temp[i+1].isdigit())):
                token+=temp[i]
            else:
                insert(token)
                insert(":")
                token=""
        elif(temp[i] == '-'):
            if((temp[i-1].isalpha() or temp[i-1].isdigit()) and (temp[i+1].isalpha() or temp[i+1].isdigit())):
                token+=temp[i]
            else:
                insert(token)
                insert('-')
                token=""
        elif(temp[i]==quote):
            if((temp[i-1].isalpha() or temp[i-1].isdigit()) and (temp[i+1].isalpha() or temp[i+1].isdigit())):
                token+=temp[i]
            else:
                insert(token)
                insert(quote)
                token=""
        elif(temp[i] == '*'):
            if(temp[i-1].isalpha() or temp[i-1].isdigit() or temp[i+1].isalpha() or temp[i+1].isdigit()):
                token += temp[i]
            else:
                insert(token)
                insert("*")
                token =""
        else:
            token += temp[i]

for i in bow:
    insert_dic(i)
Unigram = sorted(result.iteritems(), key=operator.itemgetter(1),reverse=True)


for i in range(len(bow)-1):
    insert_dic1(bow[i] + " " + bow[i+1])
Bigram = sorted(result1.iteritems(), key=operator.itemgetter(1),reverse=True)


print len(Unigram)

matrix={}
for i in range(10000):
    try:
        matrix[Unigram[i][0]]={"left":{},"right":{}}
        for j in range(250):
            matrix[Unigram[i][0]]["left"][Unigram[j][0]] = 0
            matrix[Unigram[i][0]]["right"][Unigram[j][0]] = 0
    except:
        break

for i in Bigram:
    try:
        word=i[0].split()
        word1=word[0]
        word2=word[1]
        count=i[1]
    except:
        continue
    try:
        matrix[word1]["right"][word2] += count
    except:
        continue
    try:
        matrix[word2]["left"][word1] += count
    except:
        continue


cluster=[]
centroids=random.sample(set(matrix.keys()), 50)
centroid_vector=[]

def vect(word):
    a=[]
    for i in matrix[word]["left"]:
        a.append(matrix[word]["left"][i])
    for i in matrix[word]["right"]:
        a.append(matrix[word]["right"][i])
    return a

for i in centroids:
    cluster.append([])
    centroid_vector.append(vect(i))

def euclid_dist(word_vector,centroid_vector):
    distance=0
    for i in range(len(word_vector)):
        distance  += (word_vector[i] - centroid_vector[i])**2
    return distance**0.5

def median(cluster):
    a=[]
    n=len(cluster)
    for i in range(500):
        a.append(0)
    for i in cluster:
        b=vect(i[0])
        for j in range(500):
            a[j] += b[j]
    for i in range(500):
        if(n!=0):
            a[i] = a[i] / n
        else:
            a[i] = 0
    return a

big_answer=[]

for iterations in range(1):
    cluster1=[]
    for i in range(50):
        cluster1.append([])
    cluster=cluster1

    for i in matrix:
        flag=0
        min=99999999
        cluster_number=""
        word_vector=vect(i)
        if(iterations == 0):
            for j in range(len(centroids)):
                if(i==centroids[j]):
                    cluster[j].append([i,0.0])
                    flag=1
        if(flag==0):
            for j in range(len(centroid_vector)):
                dist=euclid_dist(word_vector,centroid_vector[j])
                if(dist<min):
                    min=dist
                    cluster_number=j
            cluster[cluster_number].append([i,min])

    centroid_vector1=[]
    for i in range(len(cluster)):
        centroid_vector1.append(median(cluster[i]))
    centroid_vector = centroid_vector1

    big_answer.append(cluster)



for i in cluster:
    sorted = i.sort(key=lambda x: x[1])
    for k in range(25):
        try:
            print i[k][0] ,
        except:
            break
    print

