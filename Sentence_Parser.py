import sys
training_file = open("English_Parsed_Train.txt")
training_lines = training_file.readlines()
test_file = open("English_Test_Parse.txt")
test_lines = test_file.readlines()
rules={}
output = ""
newrule_list=[]

#------------------------------------------------- Search whether a given rule exists in CFG while converting CFG to CNF form ---------------------------

def search(rule):
    for i in rules:
        for j in rules[i]:
            if(rule == j):
                return i
    return False


def exists_rule(l):
    try:
        if(len(l) == 2):
            rules[l[0]][l[1]]
            return True
    except:
        return False

#---------------------------------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------- Compute the probabilities -------------------------------------------------------------

def compute_probabilities():
    for rule in rules:
        s = 0
        for i in rules[rule]:
            s += rules[rule][i]
        for i in rules[rule]:
            rules[rule][i] = float(rules[rule][i]) / float(s)


#-------------------------------------------------------------------------------------------------------------------------------------------------------



#---------------------------------------------------------- get line from training file -------------------------------------------------------------
def split_trainingline(l):
    l1=[]
    for i in l:
        if(i.find("(")!=-1):
            temp = i
            temp1 = ""
            for j in temp:
                if(j == "("):
                    temp1 = temp1 + " ( "
                else:
                    temp1 += j
            temp1=temp1.split(" ")
            for j in temp1:
                if(j!=""):
                    l1.append(j)
        elif(i.find(")") != -1):
            temp = i
            temp1 = ""
            for j in temp:
                if(j == ")"):
                    temp1 = temp1 + " ) "
                else:
                    temp1 = temp1 + j
            temp1=temp1.split(" ")
            for j in temp1:
                if(j!=""):
                    l1.append(j)
        else:
            l1.append(i)
    return l1


#-------------------------------------------------------------------------------------------------------------------------------------------------------


#---------------------------- Extract rules from training line ----------------------------------------------------------------------------------------------


def get_rules(l1):
    try:
        a=list()
        for i in l1:
            if(i != ")"):
                a.append(i)
            else:
                rule=[]
                while(a[-1] != "("):
                    rule.append(a.pop())
                a.pop()
                a.append(rule[-1])
                rule.reverse()
                try:
                    rules[rule[0]][" ".join(rule[1:])] += 1
                except:
                    try:
                        rules[rule[0]]
                        rules[rule[0]][" ".join(rule[1:])] = 1
                    except:
                        rules[rule[0]] ={}
                        rules[rule[0]][" ".join(rule[1:])] = 1
    except:
            print l1

#----------------------------------------------------    Parse training data  -------------------------------------------------------


for i in training_lines:
    get_rules(split_trainingline(i.split(" ")))

#---------------------------------------------------------------------------------------------------------------------------------------------




#------------------------------------------------------ Converting CFG to CNF form -----------------------------------------------------------

count = 0
new_rules={}
for i in rules:
    new_rules[i] = {}
    for j in rules[i]:
        if(len(j.split(" ")) < 3):
            new_rules[i][j] = rules[i][j]

for i in rules:
    for j in rules[i]:
        if(len(j.split(" ")) == 3 ):
            flag = 0
            temp = j.split(" ")
            first = temp[0:3]
            second = temp[1:]
            for k in newrule_list:
                try:
                    new_rules[k][first[0] +  " " + first[1]] += rules[i][j]
                    try:
                        new_rules[i][k + " " + temp[2]] += rules[i][j]
                    except:
                        new_rules[i][k + " " + temp[2]] = rules[i][j]
                    flag=1


                except:
                    continue

            if(flag==0):
                bow = "NEWRL" + str(len(newrule_list)+1)
                newrule_list.append(bow)
                new_rules[bow] = {}
                new_rules[bow][first[0] + " " + first[1]] = rules[i][j]
                new_rules[i][bow + " " + temp[2]] = rules[i][j]



#--------------------------------------------------------------------------------------------------------------------------------------------





#-----------------------------------------------------------------Adding test words----------------------------------------------------------------------


def add_rule(word_tag,count):
    #print word_tag
    word_tag = word_tag[:-1]
    word_tag = word_tag.split(" ")

    for i in word_tag:

        try:
            temp = i.split("_")
            word = temp[0]
            tag = temp[1]
            try:
                new_rules[tag][word] += 1
            except:
                new_rules[tag][word] = 1
        except:
            #print count , word_tag , i.split("_")
            temp = i.split("_")
            if(len(temp) == 2):
                try:
                    new_rules[temp[1]][temp[0]] += 1
                except:
                    try:
                        new_rules[temp[1]][temp[0]] = 1
                    except:
                        new_rules[temp[1]] = {}
                        new_rules[temp[1]][temp[0]] = 1





for i in range(len(test_lines)):
    add_rule(test_lines[i],i+1)


#-----------------------------------------------------------------------------------------------------------------------------------------------------





#------------------------------------------- Calling compute probability function -----------------------------------------------------------------------

rules = new_rules
compute_probabilities()

#----------------------------------------------------------------------------------------------------------------------------------------------------------







#---------------------------------------------------------- Print parse tree --------------------------------------------------------------------------------

def build_tree(back,begin,end,tag):
    global output
    try:
        """if(tag=="S"):
            bp=back[str(begin)][str(end)]["S"]
            sys.stdout.write("("+tag)
            build_tree(back,begin,end,bp[0])
            sys.stdout.write(")")
        else:"""
        bp=back[str(begin)][str(end)][tag]
        #sys.stdout.write(" ("+tag)
        output += " ("+tag
        if(len(bp)==3):
            build_tree(back,begin,bp[0],bp[1])
            build_tree(back,bp[0],end,bp[2])
        else:
            if(tag == "."):
                output += " " + tag
            else:
                build_tree(back,begin,end,bp[0])
        output += ")"
        #sys.stdout.write(")")
    except:
        output += " " + tag
        #sys.stdout.write(" "+tag)


#--------------------------------------------------------------------------------------------------------------------------------------------------------

def compute_parsetrees(back,score,words,x):
    output_list=[]
    dic={}
    for i in x:
        if((type(x[i]) == list) and (len(x[i])==1) ):
            #print x[i]
            dic[x[i][0]] = 1
            global output
            output = ""
            build_tree(back,0,len(words),i)
            output_list.append([output[1:],score['0'][str(len(words))][i]])
        elif( (type(x[i]) == list) and (len(x[i])==3) ):
            try:
                dic[i]
            except:
                #print x[i]
                global output
                output = ""
                build_tree(back,0,len(words),i)
                output_list.append([output[1:],score['0'][str(len(words))][i]])
    return output_list

#------------------------------------------------------------------------------------- CYK algorithm ------------------------------------------------------

def CYK(args):

    test_line= args

    test_line = test_line.split(" ")


    score={}
    back={}
    for i in range(len(test_line)+1):
        score[str(i)]={}
        back[str(i)] = {}
        for j in range(len(test_line)+1):
            score[str(i)][str(j)]={}
            back[str(i)][str(j)] = {}
            for k in rules:
                score[str(i)][str(j)][k] = 0.0
                back[str(i)][str(j)][k]  = 0.0
    words = test_line
    for i in range(len(words)):
        word = words[i].split("_")[0]
        for A in rules:
            try:
                score[str(i)][str(i+1)][A] = rules[A][word]
                back[str(i)][str(i+1)][A] = [word]
                #print A,word
            except:
                continue
        added = True
        while added:
            added = False
            for A in rules:
                for B in rules:
                    if(score[str(i)][str(i+1)][B] > 0 and exists_rule([A,B])):
                        prob = rules[A][B] * score[str(i)][str(i+1)][B]
                        if(prob > score[str(i)][str(i+1)][A]):
                            score[str(i)][str(i+1)][A] = prob
                            back[str(i)][str(i+1)][A] = [B]
                            added = True
    for span in range(2,len(words)+1):
        for begin in range(len(words)-span + 1):
            end = begin + span

            for split in range(begin+1 , end):
                print begin,end,split
                for A in rules:
                    for B in rules:
                        for C in rules:
                            try:
                                prob = score[str(begin)][str(split)][B] * score[str(split)][str(end)][C] * rules[A][B+" "+C]
                                if(prob > score[str(begin)][str(end)][A]):
                                    score[str(begin)][str(end)][A] = prob
                                    back[str(begin)][str(end)][A] = [split,B,C]
                            except:
                                s1=""
            added = True
            while added:
                added = False
                for A in rules:
                    for B in rules:
                        try:
                            prob = rules[A][B] * score[str(begin)][str(end)][B]
                            if(prob > score[str(begin)][str(end)][A]):
                                score[str(begin)][str(end)][A] = prob
                                back[str(begin)][str(end)][A] = [B]
                                added = True
                        except:
                            s1=""

    """for i in range(len(words)):
                x = back[str(i)][str(i+1)]
                print "******" , i , i+1 , "****************"
                print
                for j in x:
                    if(x[j] > 0.0):
                        print j , x[j]

                print
                print "***********************"

    for span in range(2,len(words)+1):
        for begin in range(len(words)-span + 1):
            end = begin + span
            for split in range(begin+1 , end):
                x = back[str(begin)][str(end)]
                print "******" , begin , end , "****************"
                print
                for i in x:
                    if(x[i] > 0.0):
                        print i , x[i]
                print
                print "***********************" """


    x = back[str(0)][str(len(words))]

    output_list=compute_parsetrees(back,score,words,x)


    output_list.sort(key=lambda x: x[1], reverse=True)
    if(len(output_list) == 0):
            print "No parse tree possible"
    else:
        for i in range(len(output_list)):
            print output_list[i][0]

#----------------------------------------------------------------------------------------------------------------------------------------------------------------




for i in test_lines:
    print "#------------- PARSE TREES ---------------# \n"
    CYK(i)
    print
    print



