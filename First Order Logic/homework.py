## TODO clean up, a bit complicated beacuse of variable subsitution

from copy import deepcopy
inputf = open('input.txt', 'r')
outputf = open('output.txt', 'w')
num_queries = int(inputf.readline())
queries = []
sept = 1
for i in range(num_queries):
    predicateandargument = inputf.readline().replace('\n', '').replace(" ", "").split('|')
    repl = ''
    replacingvalue = {}
    for iopi in range(len(predicateandargument)):
        predicate = predicateandargument[iopi].split('(')[0]
        arguments = predicateandargument[iopi].split('(')[1].replace(')', '').split(',')
        predii = predicate + '('
        for rgui in range(len(arguments)):
            if (ord(arguments[rgui][0]) >= 97 and ord(arguments[rgui][0]) <= 122):
                if (not replacingvalue.__contains__(arguments[rgui])):
                    replacingvalue[arguments[rgui]] = 'x' + str(sept)
                    sept += 1
                arguments[rgui] = replacingvalue[arguments[rgui]]
            if (rgui == len(arguments) - 1):
                predii += arguments[rgui] + ' '
            else:
                predii += arguments[rgui] + ' ,'
        predii += ')'
        if (iopi == len(predicateandargument) - 1):
            repl += predii
        else:
            repl += predii + '|'
    queries.append(repl)
num_dict = int(inputf.readline())
dict_queries = []
for i in range(num_dict):
    predicateandargument = inputf.readline().replace('\n', '').replace(" ","").split('|')
    repl = ''
    replacingvalue = {}
    for iopi in range(len(predicateandargument)):
        predicate = predicateandargument[iopi].split('(')[0]
        arguments = predicateandargument[iopi].split('(')[1].replace(')','').split(',')
        predii = predicate + '('
        for rgui in range(len(arguments)):
            if(ord(arguments[rgui][0])>=97 and ord(arguments[rgui][0])<=122):
                if(not replacingvalue.__contains__(arguments[rgui])):
                    replacingvalue[arguments[rgui]] = 'x' + str(sept)
                    sept += 1
                arguments[rgui] = replacingvalue[arguments[rgui]]
            if(rgui == len(arguments) - 1):
                predii += arguments[rgui] + ' '
            else:
                predii += arguments[rgui] + ' ,'
        predii += ')'
        if(iopi == len(predicateandargument) - 1):
            repl += predii
        else:
            repl += predii + '|'
    dict_queries.append(repl)
for i in range(num_queries):
    found = False
    test_queries = set(dict_queries)
    test_dict = num_dict
    num_updates = 1
    queries_to_test = set()
    sub = {}
    for ko in test_queries:
        if(len(ko.split('|')) == 1):
            for arg in ko.split('(')[1].split(','):
                if(ord(arg[0])>=65 and ord(arg[0])<=90):
                    queries_to_test.add(ko)
    if(queries[i][0] != '~'):
        queries_to_test.add('~' + queries[i])
    else:
        queries_to_test.add(queries[i].replace('~', ''))
    formed_q = deepcopy(test_queries)
    new_q = deepcopy(queries_to_test)
    qusept = sept
    while(len(new_q)>0 and not found and qusept < 500):
        for ui in new_q:
            test_queries.add(ui)
        for wi in new_q:
            if(len(wi.split('|')) == 1):
                queries_to_test.add(wi)
        new_q = set()
        for query_to_test in queries_to_test:
            for j in test_queries:
                dict_yu = j.split('|')
                test_yu = query_to_test.split('|')
                deleted_yu = -1
                #print('Query:'+str(j))
                #print('To_test'+ str(query_to_test))
                for yu in range(len(test_yu)):
                    deleted = -1
                    for k in range(len(dict_yu)):
                        pred = dict_yu[k].split('(')[0]
                        arg = dict_yu[k].split('(')[1]
                        if(pred.replace('~','') == test_yu[yu].split('(')[0].replace('~','') and ((pred[0] == '~' and test_yu[yu][0]!='~') or (pred[0] != '~' and test_yu[yu][0]=='~'))):
                            if(len(arg.split(',')) == len(test_yu[yu].split('(')[1].split(','))):
                                arguments = arg.replace(')', '').split(',')
                                subsitutions = test_yu[yu].split('(')[1].replace(')','').split(',')
                                for arg in range(len(arguments)):
                                    if ord(arguments[arg][0])>=65 and ord(arguments[arg][0])<=90 and ord(subsitutions[arg][0])>=65 and ord(subsitutions[arg][0])<=90:
                                        if(arguments[arg] != subsitutions[arg]):
                                            deleted = -1
                                            sub = {}
                                            deleted_yu = -1
                                            break
                                        else:
                                            deleted = k
                                            deleted_yu = yu
                                    elif (ord(arguments[arg][0])>=97 and ord(arguments[arg][0])<=122):
                                        if(not sub.__contains__(arguments[arg])):
                                            sub[arguments[arg]] = subsitutions[arg]
                                            deleted = k
                                            deleted_yu = yu
                                        else:
                                            if(sub[arguments[arg]]!=subsitutions[arg]):
                                                deleted = -1
                                                deleted_yu = -1
                                                break
                                    elif(ord(subsitutions[arg][0])>=97 and ord(subsitutions[arg][0])<=122 and ord(arguments[arg][0])>=65 and ord(arguments[arg][0])<=90):
                                        if (not sub.__contains__(arguments[arg])):
                                            sub[subsitutions[arg]] = arguments[arg]
                                            deleted = k
                                            deleted_yu = yu
                                        else:
                                            if(sub[arguments[arg]]!=subsitutions[arg]):
                                                deleted = -1
                                                deleted_yu = -1
                                                break
                    if(deleted!=-1):
                        #print(sub)
                        dict_yu.remove(dict_yu[deleted])
                        for k in range(len(dict_yu)):
                            predi = dict_yu[k].split('(')[0]
                            argi = dict_yu[k].split('(')[1].replace(')','').split(',')
                            dict_yu[k] = predi + '('
                            for hu in range(len(argi)):
                                if(sub.__contains__(argi[hu])):
                                    argi[hu] = sub[argi[hu]]
                                dict_yu[k] += argi[hu].strip()
                                if(hu!=len(argi)-1):
                                    dict_yu[k] += ' ,'
                            dict_yu[k] += ' )'
                        strio = ''
                        for k in range(len(dict_yu)):
                            strio += dict_yu[k]
                            if(k!=len(dict_yu)-1):
                                strio += '|'
                        for k in range(len(test_yu)):
                            predi = test_yu[k].split('(')[0]
                            argi = test_yu[k].split('(')[1].replace(')', '').split(',')
                            test_yu[k] = predi + '('
                            for hu in range(len(argi)):
                                if (sub.__contains__(argi[hu])):
                                    argi[hu] = sub[argi[hu]]
                                test_yu[k] += argi[hu].strip()
                                if (hu != len(argi) - 1):
                                    test_yu[k] += ' ,'
                            test_yu[k] += ' )'
                        for op in range(len(test_yu)):
                            if(op != deleted_yu):
                                if(strio == ''):
                                    strio = strio + test_yu[op]
                                else:
                                    strio = strio + '|' + test_yu[op]
                        if (strio != ''):
                            if (not formed_q.__contains__(strio)):
                                formed_q.add(strio)
                                repl = ''
                                predicateandargument = strio.split('|')
                                replacingvalue = {}
                                for iopistr in range(len(predicateandargument)):
                                    predicate = predicateandargument[iopistr].split('(')[0]
                                    arguments = predicateandargument[iopistr].split('(')[1].replace(')', '').split(',')
                                    predii = predicate + '('
                                    for rgui in range(len(arguments)):
                                        replaced = False
                                        if (ord(arguments[rgui][0]) >= 97 and ord(arguments[rgui][0]) <= 122):
                                            if (not replacingvalue.__contains__(arguments[rgui])):
                                                replacingvalue[arguments[rgui]] = 'x' + str(qusept)
                                                qusept += 1
                                            arguments[rgui] = replacingvalue[arguments[rgui]]
                                        if (rgui == len(arguments) - 1):
                                            predii += arguments[rgui].strip() + ' '
                                        else:
                                            predii += arguments[rgui].strip() + ' ,'
                                    predii += ')'
                                    if (iopistr == len(predicateandargument) - 1):
                                        repl += predii
                                    else:
                                        repl += predii + '|'
                                strio = repl
                        #print(strio)
                        #print('\n')
                        if(strio!=''):
                            if(not test_queries.__contains__(strio)):
                                new_q.add(strio)
                            if(strio == queries[i]):
                                found = True
                            #something here
                            if((len(strio.split('|')) == 1) and ((strio[0] == '~' and test_queries.__contains__(strio.replace('~',''))) or (strio[0] != '~' and test_queries.__contains__('~' + strio)))):
                                found = True
                        if(strio == ''):
                            found = True
                    break
                sub = {}
    print('Found' + str(found))
    print('new_q' + str(len(new_q)))
    print('qusept' + str(qusept))
    if(found):
        outputf.write('TRUE\n')
    else:
        true = False
        if(not true):
            outputf.write('FALSE\n')
        else:
            outputf.write('TRUE\n')
