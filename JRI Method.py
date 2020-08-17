import time
import csv
from apyori import apriori
start = time.time()
#Step one reference Transactions Selection (In case study unique set of items)
def ref_transaction_selection(inputfile):
    import csv
    given_data=[]
    with open(inputfile)as f:
        data = csv.reader(f)
        for row in data:
            if row != []:
                given_data.append(row)
    unique_elements = set(x for l in given_data for x in l)
    unique_elements=list(unique_elements)
    uni=[]
    for item in unique_elements:
        if item !='':
            uni.append(item)
    return uni
# Step-2 Jaccard Threshold Discovery, Calculating Jaccard Threshold (The most repeated Jaccard Value)
def jaccardvalue(inputfile):
    import csv
    given_data=[]
    with open(inputfile)as f:
        data = csv.reader(f)
        for row in data:
            if row != []:
                given_data.append(row)
    uni=ref_transaction_selection(inputfile)
    jaccard_simi_values=[]
    y=0
    while y < len(given_data):
        b=0
        a = (set(uni))
        b = (set(given_data[y]))
        intersection_cardinality = len(set.intersection(*[set(a), set(b)]))
        union_cardinality = len(set.union(*[set(a), set(b)]))
        if float(union_cardinality)!=0:
            jac=intersection_cardinality / float(union_cardinality)
            jaccard_simi_values.append(jac)
        y+=1
    i=0
    while i< len(jaccard_simi_values):
        if jaccard_simi_values[0]:
            x=0
        i+=1

    from    collections     import Counter
    a = jaccard_simi_values
    b = Counter(a)
    print("Jaccard similarity threshold values",jaccard_simi_values)
    print("Most repeated Jaccard Value",(Counter(a).most_common(1)[0][0]))
    return (Counter(a).most_common(1)[0][0])
# Step-3 Applying Jaccard Rule (most repeated jaccard value) on Input Dataset
def jaccard_base_extracted_transactions(inputfile):
    given_data=[]
    with open(inputfile)as f:
        data = csv.reader(f)
        for row in data:
            if row != []:
                given_data.append(row)
    unique_elements = set(x for l in given_data for x in l)
    unique_elements=list(unique_elements)
    uni=[]
    for item in unique_elements:
        if item !='':
            uni.append(item)

    jaccard_simi_values=[]
    y=0
    jaccard_set=[]
    while y < len(given_data):
        b=0
        a = (set(uni))
        b = (set(given_data[y]))
        intersection_cardinality = len(set.intersection(*[set(a), set(b)]))
        union_cardinality = len(set.union(*[set(a), set(b)]))
        if float(union_cardinality)!=0:
            jac=intersection_cardinality / float(union_cardinality)
            jaccard_simi_values.append(jac)
            if  jac <=jaccardvalue(inputfile):
                jaccard_set.append(given_data[y])
        y+=1
    print("======================================================")
    print("Jaccard Similarity base Extracted Transactions are ", jaccard_set)
    print("======================================================")
    return jaccard_set

def aprioriresult(inputfile,sup,conf):
    association_rules = apriori(jaccard_base_extracted_transactions(inputfile), min_support=sup, min_confidence=conf, min_length=3)
    association_results = list(association_rules)
    print("*************************************")
    print("Extracted Hidden Information")
    print("=====================================")
    for item in association_results:
        pair = item[0]
        items = [x for x in pair]
        print(str(list(item.ordered_statistics[0].items_base)) + "->" + str(
            list(item.ordered_statistics[0].items_add)))
        print("Support: " + str(item[1]))
        print("Confidence: " + str(item[2][0][2]))
        print("Lift: " + str(item[2][0][3]))
        print("=====================================")
    end = time.time()
    print('Execution time?', str(end - start))
aprioriresult('general dataset.csv',0.2,0.7)


# Step-4 Applying Association Rule Mining Rules on Jaccard Sample
def apriori_ARM_Implentation(inputfile, confidence):
    if len(jaccard_base_extracted_transactions(inputfile))!=0:
        given_data=jaccard_base_extracted_transactions(inputfile)
        #finind combinations
        comb_set=[]
        import itertools
        import json

        stuff = ref_transaction_selection(inputfile)
        for L in range(0, len(stuff)+1):
            for subset in itertools.combinations(stuff, L):
                comb_set.append(subset)
        comb_set_list=json.loads(json.dumps(comb_set))
        comb_set_list = sorted([x for x in comb_set_list if x != []])
        # finding supports of each item by Counting combination data into given data set
        i=0
        count_set=[]
        support_set=[]
        while i < len(comb_set_list):
            j=0
            m=0
            c=0
            n=len(comb_set_list[i])
            while j < len(given_data):
                for x in comb_set_list[i]:
                    if (x in given_data[j]):
                        m+=1
                if (m==n):
                    c+=1
                m=0
                j+=1
            s=round(c/len(given_data),2)
            if s >= 0.2:
                print(comb_set_list[i],"count   ", c, "support is ", s )
            count_set.append(c)
            support_set.append(s)
            i+=1
        #print((count_set))

        # Finding confidence
        j=0
        k=0
        l=0
        conf=[]
        conf_between=[]
        operator=['=>']
        conf_set_pair=[]
        merge=[]
        con=0
        while j < len(comb_set_list):
            k=0
            m=0
            while k <len(comb_set_list):
                m=0
                t=0
                while m <=len(comb_set_list[j])-1:
                    if comb_set_list[j][m] not in comb_set_list[k] :
                        t+=1
                    if comb_set_list[j][m] in comb_set_list[k]:
                        break
                    m+=1
                    if t==len(comb_set_list[j]):
                        if support_set[j]>=0.2 and support_set[k]>=0.2:
                            mylist = list(set(comb_set_list[j] + comb_set_list[k]))
                            merge = list(dict.fromkeys(mylist))
                            #print(comb_set_list[j]," with ", comb_set_list[k])

                            #print("merge is ",comb_set_list[j], "and ", comb_set_list[k], "are ",merge)
                            conf_between = comb_set_list[j] + operator + comb_set_list[k]
                            conf_set_pair.append(conf_between)

                           # print(conf_set_pair)
                            l=0
                            while l < len(comb_set_list):
                                if sorted(merge) == sorted(comb_set_list[l]):
                                    if support_set[j]==0:
                                        #print("sup j", support_set[j], con)
                                        con=0
                                        conf.append(con)
                                        break
                                    else:
                                        con=support_set[l]/support_set[j]
                                        #print("sup l/j", support_set[l], support_set[j], con)
                                        conf.append(con)
                                        break

                                l+=1
                k+=1
            j+=1
        end=time.time()

        x=0
        n=1

        #Obtaing results according to confidence
        while x < len(conf_set_pair):
            if conf[x] >=confidence:
                print(conf_set_pair[x], "confidence",conf[x])

                n+=1
            x+=1


# Calling Poroposed JRI Algorithm
#apriori_ARM_Implentation('general dataset.csv',0.7)
# calling Poroposed JRI Algorithm through conventional Apriori
aprioriresult('general dataset.csv',0.2,0.7)