import pprint as pp
import math
import sys

#calculating unique values for a column in a dataset
def unique_vals(rows,col):
    return sorted(list(set(row[col] for row in rows)))

#counts no. of each type of labels in a dataset and returns a dictionary.
def dict_counts(rows):

    counts = {}
    for row in rows:
        label = row[-1]     #in our dataset, label is always the last column
        if label not in counts:
            counts[label] = 0
        counts[label] +=1
    return counts

#calculate entropy for given row.
def entropy(rows):
    d = dict_counts(rows)
    # print(d)
    E = 0
    den = 0
    for key in d:
        den += d[key]
    
    # print(den)
    for key in d:
        p = float(d[key])/float(den)
        # print("p",p)

        if p>0:
            E -= float(p*math.log(p,2))
    # print(E)
    return E

#calculating gain for the attribute
def findGain(dataset,col):
    E_dataset = entropy(dataset)
    # print(E_dataset)

    val = list(unique_vals(dataset,col))
    # print(val)
    E_val = []
    len_val = []
    # print(val)

    for v in val:
        # print(v)
        len_v = 0
        new_data = []
        for r in dataset:
            if str(v) == str(r[col]):
                new_data.append(r)
                len_v+=1
        # print(new_data)
        E_val.append(entropy(new_data))
        len_val.append(len_v)
    

    # print(E_val,len_val)

    gain = E_dataset
    S = float(len(dataset))
    for (e,s) in zip(E_val,len_val):
        gain -= (s/S)*e

    return gain

#finding column with maximum gain attribute of given dataset
def maxGainAttribute(dataset):
    max_gain_col = 0
    max_gain = -1
    for i in range(len(dataset[0])-1):
        new_gain = findGain(dataset,i)
        # print(new_gain)
        if new_gain >= max_gain:
            max_gain = new_gain
            max_gain_col = i
    
    return max_gain_col

#splitting the given dataset on the basis of given type
def splitdata(dataset,type,col):
    rows = []
    for r in dataset:
        if str(r[col]) == str(type):
            rows.append(r)
    return rows

#function to check spliting is possible or not
def isSplitable(dataset):
    for i in range(len(dataset[0])-1):
        if len(unique_vals(dataset,i))>1:
            return True
    return False


#creating and printing a decision tree
def ID3DecisionTree(header,dataset):
    best_col = maxGainAttribute(dataset)
    uni_types = unique_vals(dataset,best_col) 
    labels_count = dict_counts(dataset)

    node = header[best_col]
    #leaf node condition
    if len(labels_count.keys())==1 or not isSplitable(dataset):
        return max(labels_count.keys(),key=lambda x: labels_count[x])
    else:
        ans = {}
        for i in uni_types:
            new_data = splitdata(dataset,i,best_col)
            ans[i]= ID3DecisionTree(header,new_data)
    
        return {node:ans}

#_________________________file reading_________________________________

if __name__ == "__main__":

    if len(sys.argv) <2:
        print("Please give a file as argument")
        sys.exit()
    filename = sys.argv[1]
    f = open(filename,"r")

    header = f.readline()[:-1].split("\t")
    # print(header)
    data = []
    for line in f.readlines():
        data.append(line[:-1].split("\t"))

    # print(maxGainAttribute(data))
    pp.pprint(ID3DecisionTree(header,data))