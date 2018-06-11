def rulesGenerator(frequentPatterns, rules, minConf=0.1):
    for frequentset in frequentPatterns:
        if(len(frequentset) > 1):
            getRules(frequentset,frequentset, rules, frequentPatterns, minConf)

def removeStr(set, str):
    tempSet = []
    for elem in set:
        if(elem != str):
            tempSet.append(elem)
    tempFrozenSet = frozenset(tempSet)
    return tempFrozenSet


def getRules(frequentset,currentset, rules, frequentPatterns, minConf=0.1):
    for frequentElem in currentset:
        subSet = removeStr(currentset, frequentElem)
        confidence = frequentPatterns[frequentset] / frequentPatterns[subSet]
        if (confidence >= minConf):
            flag = False
            for rule in rules:
                if(rule[0] == subSet and rule[1] == frequentset - subSet):
                    flag = True
            if(flag == False):
                rules.append((subSet, frequentset - subSet, confidence))

            if(len(subSet) >= 2):
                getRules(frequentset, subSet, rules, frequentPatterns, minConf)
