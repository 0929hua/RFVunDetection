import csv
import json
#buggy_1  无漏洞合约 nothing false
#buggy_2  TX合约    true
#buggy_3  DAO合约   nothing  true
#buggy_4  DAO合约   nothing  true
#buggy_5  TX合约    true
#buggy_6  TX合约    true
#buggy_7  无漏洞合约 nothing false
#buggy_8  DAO合约   nothing  true
#buggy_9  DAO合约   nothing  true
#buggy_10  DAO合约   nothing  true
#buggy_11  无漏洞合约  nothing false
#buggy_12  DAO合约  nothing  true      true true
#buggy_13  DAO合约  nothing  true
#tx_1 TX合约        true
#tx_2 TX合约        true
#tx_3 TX合约        true
#tx_4 TX合约        true
#tx_5 TX合约        true     true  true
import os

#  dao 6  无漏洞3个   TX 7个  bothTwo 2个

from gensim.models import Word2Vec
from numpy.compat import long
from sklearn.datasets import load_iris
import numpy as np
from os.path import join, getsize
###读取文件
import os
import sys
sys.setrecursionlimit(1000000000) #例如这里设置为十万
class TailRecurseException(BaseException):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


def tail_call_optimized(g):
    """
    This function decorates a function with tail call
    optimization. It does this by throwing an exception
    if it is it's own grandparent, and catching such
    exceptions to fake the tail call optimization.

    This function fails if the decorated5
    function recurses in a non-tail context.
    """
    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
            raise TailRecurseException(args, kwargs)
        else:
            while 1:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs

    func.__doc__ = g.__doc__
    return func


def read_out_file(path):
 try:
  f = open(path, 'r', encoding='utf-8')
  data = f.readlines()
  f.close()
  print("文件读取成功！")
  return data
 except IOError:
  print('文件读取失败！')
def get_filelist(dir, path, format):
    # 存放对应Json文件
    Filelist = [];
    for home, dir, files, in os.walk(path):
        # 遍历对应的文件下的所有文件
        for filename in files:
            # 通过文件后缀判断是否为format文件
            if filename.endswith(format):
                Filelist.append(os.path.join(home, filename))
    return Filelist
###提取block中 操作码
def operateCodeList(data):
    #path = '../skip/decompile_dao_hack.dasm.output'
    #data = read_out_file(path)  # 读取文件
    nodeS = []  # 去除以B,[,E,S,P,F,=,\n开头的字符串,包含 : 的字符串
    for i in data:
        if i.startswith('B') or i.startswith('[') or i.startswith('E') or i.startswith('S') \
                or i.startswith('P') or i.startswith('F') or i.startswith('=') or i.startswith('\n') or \
                i.__contains__(':'):
            continue
        m = i.lstrip().strip('\n')  # 去除首尾空白字符
        nodeS.append(m)
    # print(nodeS)
    codelist = []
    codeLists = []
    for opcode in nodeS:
        if opcode.__contains__("---"):
            codeLists.append(codelist)
            codelist = []
            continue
        codelist.append(opcode)
    # print(codeLists)

    operateCodeList = []  # 区块节点操作码集合
    for i in codeLists:
        if i.__eq__([]):  # 去除空集
            continue
        operateCodeList.append(i)
    return operateCodeList

#blockList  区块节点
#preSucList   区块节点的后继节点列表
def blockListAndpreSucListS(data):
    blockListAndpreSucList=[]
    blockList = []  # 区块节点
    preSucList = []  # 区块节点的后继节点列表
    succList=[]# 区块节点的前驱节点列表
    for i in data:
        if i.startswith('Block'):
            m = i.lstrip().strip('\n')
            blockList.append(m)
        if i.startswith('Successors'):  # i.startswith('Predecessors') or
            preSucList.append(i)
        if i.startswith('Predecessors'):  # i.startswith('Predecessors') or
            succList.append(i)
        blockListS = []
    #print(blockList)
    blockListS = []
    for i in blockList:
        blockListS.append(i.split()[1])  # 以空格为分隔符，包含 \n
    preSucListS = []
    for i in preSucList:
        list = i.split(':')[1]  # 以空格为分隔符，包含 \n
        preSucListS.append(list)
    succListS=[]
    for i in succList:
        list = i.split(':')[1]  # 以空格为分隔符，包含 \n
        succListS.append(list)
    blockListAndpreSucList.append(blockListS)
    blockListAndpreSucList.append(preSucListS)
    blockListAndpreSucList.append(succListS)
    return blockListAndpreSucList

def Successors(blockNumAndSuccessors):
    nodeAll = []
    for i in blockNumAndSuccessors:
        str = i[1]
        if (str == ' '):
            node = []
            nodeAll.append(node)
        else:
            r = (str.replace('[', '').replace(']', '')).split(',')
            node = []
            for j in r:
                m = j.lstrip().strip('\n')  # 去除首尾空白字符
                node.append(m)
            nodeAll.append(node)
    return nodeAll

###深度优先算法
def dfsTravel(graph, source):
    # 传入的参数为邻接表存储的图和一个开始遍历的源节点
    travel = []  # 存放访问过的节点的列表
    stack = [source]  # 构造一个堆栈
    while stack:  # 堆栈空时结束
        current = stack.pop()  # 堆顶出队
        if current not in travel:  # 判断当前结点是否被访问过
            travel.append(current)  # 如果没有访问过，则将其加入访问列表
        for next_adj in graph[current]:  # 遍历当前结点的下一级
            if (next_adj==''):
                continue
            if next_adj not in travel:  # 没有访问过的全部入栈
                stack.append(next_adj)
    return travel

# 区块号以及区块节点的后继节点列表
#blockList  区块节点
#preSucList   区块节点的后继节点列表
def  blockNumAndSuccessors(blockListS,preSucListS):
    blockNumAndSuccessors = []  # 区块号以及区块节点的后继节点列表
    m = 0
    for i in blockListS:
        nodeList = []
        nodeList.append(i)
        n = 0
        for j in preSucListS:
            if m == n:
                nodeList.append(j)
            n = n + 1
        m = m + 1
        blockNumAndSuccessors.append(nodeList)
    return blockNumAndSuccessors

###将节点以及其后继节点的操作码指令
def blockOperS(numCodeDictS,codeOperDict,blockListS):
    newDict={}
    Mnodes=[]
    for key ,value in numCodeDictS.items():
        #print(key, ":", value)
        Mnode = []
        for i in value:
            for key1, value1 in codeOperDict.items():
                if i.__eq__(key1):
                    Mnode.append(value1)
                    Mnodes.append(Mnode)
    #print(Mnodes)
    res = []
    for i in Mnodes:
        if i not in res:
            res.append(i)
    newDict = {}  # 将节点以及其后继节点的操作码指令  转换为 字典格式
    for i, j in zip(blockListS, res):  # 同时循环两个列表
        newDict[i] = j  # 此时i为键，j为值，即{i：j}

    return newDict
def getFileName(dir,path,format):
    Filelist = [];
    for home, dir, files, in os.walk(path):
        # 遍历对应的文件下的所有文件
        for filename in files:
            if filename.endswith(format):
                Filelist.append(filename.strip(format))
    return Filelist
###提取控制流图所有执行路径
#fileExtractPath=''
#@tail_call_optimized
def add(key,dict,newKey):
    global fileExtractPath
    newKey=newKey+'->'+key;
    if not key=='':
        list = dict[key]
        if len(list)==1 & list[0].__eq__(''):
                 fileExtractPath.write(newKey+'\n')
                 print(newKey)
                 return 'true'
        for i in list:
            add(i, dict, newKey)
###提取所有可执行路径
def extractPath(numCodeDictS,extractPath):
    pathS = []  # 提取控制流图中所有执行路径
    f = open(extractPath, 'r')
    for line in f.readlines():
        curLine = line.strip('\n')
        if curLine.startswith('->'):
            m = curLine.strip('->')
        pathS.append(m)
    #print(pathS)
    pathALL = []
    for path in pathS:
        list = path.split('->')
        pathALL.append(list)
    return pathALL
fileExtractPath=''
def addC(key, dict, newKey):
    newKey = newKey + '->' + key;
    if not key == '':
        list = dict[key]
        if len(list) == 1 & list[0].__eq__(''):
            fileExtractPath.write(newKey + '\n')
            #print(newKey)
            return
        for i in list:
            if newKey.__contains__(i):
                fileExtractPath.write(newKey + '\n')
                #print(newKey)
                i = ''
            addC(i, dict, newKey)
#去除重复路径
def removeRepeat(data):
    m = len(data) - 1
    while m >= 0:
        strS = data[m]
        strS = strS.strip('\n')
        str = data[m - 1]
        str = str.strip('\n')
        if str in strS:
            data.remove(str + '\n')
        m = m - 1
    return data

flag=''
def daoCheck(pathALL,codeOperDict):
    flag = 'none'  # 默认表示无漏洞
    listCall = []
    for path in pathALL:
        for i in path:
            for key, value in codeOperDict.items():
                if i.__eq__(key):
                    list = []
                    # print(value)
                    for code in value:
                        code = code.split(' ')[1]
                        list.append(code)
                    if list.__contains__('CALL') & list.__contains__('CALLER'):
                        if   list.__contains__('RETURNDATASIZE') :
                            continue
                        else:
                            listCall.append(value)

    if len(listCall)>0:
        key = 'SSTORE'
        for codeList in listCall:
            opList = []
            locationNum = []
            dict = {}
            i = 0
            keyNum = 0
            for code in codeList:
                if code.__contains__(key):
                    keyNum = keyNum + 1
            if keyNum == 0:
                flag = 'true'
                break
            if flag.__eq__('none'):
                for code in codeList:
                    if code.__contains__('SHA3'):
                        opList.append('SHA3')
                        i = i + 1
                        locationNum.append(i)
                    if code.__contains__('SLOAD'):
                        opList.append('SLOAD')
                        i = i + 1
                        locationNum.append(i)
                    if code.__contains__('SSTORE'):
                        opList.append('SSTORE')
                        i = i + 1
                        locationNum.append(i)
                    if code.__contains__('GAS'):
                        opList.append('GAS')
                        i = i + 1
                        locationNum.append(i)
                    if code.__contains__('CALL'):
                        opList.append('CALL')
                        i = i + 1
                        locationNum.append(i)
                for i, j in zip(opList, locationNum):  # 同时循环两个列表
                    dict[i] = j  # 此时i为键，j为值，即{i：j}
                # print("dict:")
                # print(dict)
                sstore = dict['SSTORE']
                call = dict['CALL']
                if sstore < call:
                    flag = 'false'
                else:
                    flag = 'true'
    else:
        flag = 'none'
    return flag
def txOriginCheck(pathALL,codeOperDict):
    flag = 'none'  # 默认表示无漏洞
    listTX = []
    for path in pathALL:
        for i in path:
            for key, value in codeOperDict.items():
                if i.__eq__(key):
                    list = []
                    # print(value)
                    for code in value:
                        code = code.split(' ')[1]
                        list.append(code)
                    if list.__contains__('ORIGIN') & list.__contains__('EQ') :
                        #if not list.__contains__('CALL'):
                            listTX.append(value)
    print('len(listTX)')
    print(len(listTX))
    if len(listTX) > 0:
        for codeList in listTX:
            i = 0
            locationNum = []
            newList = []
            dict = {}
            for code in codeList:
                if code.__contains__('ORIGIN'):
                    i = i + 1
                    locationNum.append(i)
                    newList.append('ORIGIN')
                if code.__contains__('EQ'):
                    i = i + 1
                    locationNum.append(i)
                    newList.append('EQ')
            for i, j in zip(newList, locationNum):  # 同时循环两个列表
                dict[i] = j  # 此时i为键，j为值，即{i：j}
            ORIGIN = dict['ORIGIN']
            EQ = dict['EQ']
            if ORIGIN < EQ:
                flag = 'true'
                break
            else:
                flag = 'false'
        print('listTX')
        #print(listTX)
    else:
        flag = 'none'
    return flag
def timeStamp(pathALL,codeOperDict):
    flag = 'none'  # 默认表示无漏洞
    listTX = []
    listCaller = []
    for path in pathALL:
        for i in path:
            for key, value in codeOperDict.items():
                if i.__eq__(key):
                    list = []
                    # print(value)
                    for code in value:
                        code = code.split(' ')[1]
                        list.append(code)
                    if list.__contains__('TIMESTAMP') & list.__contains__('EQ'):
                        # if not list.__contains__('CALL'):
                        listTX.append(value)
    if len(listTX) > 0:
        for codeList in listTX:
            i = 0
            locationNum = []
            newList = []
            dict = {}
            for code in codeList:
                if code.__contains__('TIMESTAMP'):
                    i = i + 1
                    locationNum.append(i)
                    newList.append('TIMESTAMP')
                if code.__contains__('EQ'):
                    i = i + 1
                    locationNum.append(i)
                    newList.append('EQ')
            for i, j in zip(newList, locationNum):  # 同时循环两个列表
                dict[i] = j  # 此时i为键，j为值，即{i：j}
            TIMESTAMP = dict['TIMESTAMP']
            EQ = dict['EQ']
            if TIMESTAMP < EQ:
                flag = 'true'
                break
            else:
                flag = 'false'
        print('listTX')
    else:
        flag = 'none'
    return flag
def unCheckSend(pathALL,codeOperDict):
    flag = 'none'  # 默认表示无漏洞
    listCall = []
    for path in pathALL:
        for i in path:
            for key, value in codeOperDict.items():
                if i.__eq__(key):
                    list = []
                    # print(value)
                    for code in value:
                        code = code.split(' ')[1]
                        list.append(code)
                    if list.__contains__('CALL') & list.__contains__('CALLER'):
                        if list.__contains__('RETURNDATASIZE'):
                            continue
                        else:
                            listCall.append(value)

    if len(listCall) > 0:
        key = 'SSTORE'
        for codeList in listCall:
            opList = []
            locationNum = []
            dict = {}
            i = 0
            keyNum = 0
            for code in codeList:
                if code.__contains__(key):
                    keyNum = keyNum + 1
            if keyNum == 0:
                flag = 'true'
                break
            if flag.__eq__('none'):
                for code in codeList:
                    if code.__contains__('SHA3'):
                        opList.append('SHA3')
                        i = i + 1
                        locationNum.append(i)
                    if code.__contains__('SLOAD'):
                        opList.append('SLOAD')
                        i = i + 1
                        locationNum.append(i)
                    if code.__contains__('SSTORE'):
                        opList.append('SSTORE')
                        i = i + 1
                        locationNum.append(i)
                    if code.__contains__('GAS'):
                        opList.append('GAS')
                        i = i + 1
                        locationNum.append(i)
                    if code.__contains__('CALL'):
                        opList.append('CALL')
                        i = i + 1
                        locationNum.append(i)
                    if code.__contains__('ISZERO'):
                        opList.append('ISZERO')
                        i = i + 1
                        locationNum.append(i)
                    if code.__contains__('REVERT'):
                        opList.append('REVERT')
                        i = i + 1
                        locationNum.append(i)
                for i, j in zip(opList, locationNum):  # 同时循环两个列表
                    dict[i] = j  # 此时i为键，j为值，即{i：j}
                # print("dict:")
                # print(dict)
                sstore = dict['SSTORE']
                call = dict['CALL']
                isZero = dict['ISZERO']
                revert = dict['REVERT']
                if sstore < call & call < isZero & isZero < revert:
                    flag = 'false'
                else:
                    flag = 'true'
    else:
        flag = 'none'
    return flag
def abnormalFlow(pathALL,codeOperDict):
    flag = 'none'  # 默认表示无漏洞
    listCallAdd = []
    listCallSub = []
    listCallMul = []
    for path in pathALL:
        for i in path:
            for key, value in codeOperDict.items():
                if i.__eq__(key):
                    list = []
                    # print(value)
                    for code in value:
                        code = code.split(' ')[1]
                        list.append(code)
                    if list.__contains__('ADD') :
                            listCallAdd.append(value)
                    elif list.__contains__('GT'):
                            listCallSub.append(value)
                    elif list.__contains__('MUL'):
                            listCallMul.append(value)

    if len(listCallAdd) > 0:
        for codeList in listCallAdd:
            opList = []
            locationNum = []
            dict = {}
            i = 0
            if flag.__eq__('none'):
                for code in codeList:
                    if code.__contains__('ADD'):
                        opList.append('ADD')
                        i = i + 1
                        locationNum.append(i)
                    if code.__contains__('ISZERO'):
                        opList.append('ISZERO')
                        i = i + 1
                        locationNum.append(i)
                for i, j in zip(opList, locationNum):  # 同时循环两个列表
                    dict[i] = j  # 此时i为键，j为值，即{i：j}
                # print("dict:")
                # print(dict)
                ADD = dict['ADD']
                if 'ISZERO' in dict:
                    isZero = dict['ISZERO']
                    if ADD < isZero :
                        flag = 'none'
                    else:
                        flag = 'true'
                        break
                else :
                    flag = 'true'
                    break

    if flag.__eq__('none'):
       if len(listCallAdd) > 0:
        for codeList in listCallAdd:
            opList = []
            locationNum = []
            dict = {}
            i = 0
            if flag.__eq__('none'):
                for code in codeList:
                    if code.__contains__('GT'):
                        opList.append('GT')
                        i = i + 1
                        locationNum.append(i)
                    if code.__contains__('ISZERO'):
                        opList.append('ISZERO')
                        i = i + 1
                        locationNum.append(i)
                for i, j in zip(opList, locationNum):  # 同时循环两个列表
                    dict[i] = j  # 此时i为键，j为值，即{i：j}
                # print("dict:")
                # print(dict)
                GT = dict['GT']
                if 'ISZERO' in dict:
                    isZero = dict['ISZERO']
                    if GT < isZero:
                        flag = 'none'
                    else:
                        flag = 'true'
                        break
                else:
                    flag = 'true'
                    break
    if flag.__eq__('none'):
      if len(listCallAdd) > 0:
        for codeList in listCallAdd:
            opList = []
            locationNum = []
            dict = {}
            i = 0
            if flag.__eq__('none'):
                for code in codeList:
                    if code.__contains__('MUL'):
                        opList.append('MUL')
                        i = i + 1
                        locationNum.append(i)
                    if code.__contains__('ISZERO'):
                        opList.append('ISZERO')
                        i = i + 1
                        locationNum.append(i)
                for i, j in zip(opList, locationNum):  # 同时循环两个列表
                    dict[i] = j  # 此时i为键，j为值，即{i：j}
                # print("dict:")
                # print(dict)
                MUL = dict['MUL']
                if 'ISZERO' in dict:
                    isZero = dict['ISZERO']
                    if MUL < isZero:
                        flag = 'none'
                    else:
                        flag = 'true'
                        break
                else:
                    flag = 'true'
                    break
    return flag
def delegatecall(pathALL, codeOperDict):
    flag = 'none'  # 默认表示无漏洞
    listTX = []
    listCaller = []
    for path in pathALL:
        for i in path:
            for key, value in codeOperDict.items():
                if i.__eq__(key):
                    list = []
                    # print(value)
                    for code in value:
                        code = code.split(' ')[1]
                        list.append(code)
                    if list.__contains__('DELEGATECALL'):
                        # if not list.__contains__('CALL'):
                        listTX.append(value)
    if len(listTX) > 0:
       flag = 'true'
    else:
        flag = 'none'
    return flag
def dealdata(dataADD):
    textF = open("word2vecNew.txt", "w")
    textF.truncate()
    for str in dataADD:
        if str.startswith('DEST'):
            str = str.lstrip('DEST')
        if str.startswith('POP'):
            str = str.lstrip('POP')
        if str.startswith('JUMPI'):
            str = str.lstrip('JUMPI')
        if str.startswith('JUMP'):
            str = str.lstrip('JUMP')
        if str.startswith('ISZERO'):
            str = str.lstrip('ISZERO')
        if str.startswith('I'):
            str = str.lstrip('I')
        if str.startswith('PUSH3'):
            str = str.lstrip('PUSH3')
        if str.startswith('DUP3'):
            str = str.lstrip('DUP3')
        if str.startswith('PUSH20'):
            str = str.lstrip('PUSH20')
        if str.startswith('PUSH4'):
            str = str.lstrip('PUSH4')
        if str.startswith('SWAP2'):
            str = str.lstrip('SWAP2')
        if str.startswith('DIV'):
            str = str.lstrip('DIV')
        if str.startswith('DUP4'):
            str = str.lstrip('DUP4')
        if str.startswith('OR'):
            str = str.lstrip('OR')
        if str.startswith('LOG3'):
            str = str.lstrip('LOG3')
        if str.startswith('LOG1'):
            str = str.lstrip('LOG1')
        if str.startswith('SWAP3'):
            str = str.lstrip('SWAP3')
        if str.startswith('PUSH9'):
            str = str.lstrip('PUSH9')
        if str.startswith('MUL'):
            str = str.lstrip('MUL')
        if str.startswith('CALL'):
            str = str.lstrip('CALL')
        if str.startswith('SWAP7'):
            str = str.lstrip('SWAP7')
        if str.startswith('DATACOPY'):
            str = str.lstrip('DATACOPY')
        if str.startswith('DUP11'):
            str = str.lstrip('DUP11')
        if str.startswith('EQ'):
            str = str.lstrip('EQ')
        if str.startswith('RETURN'):
            str = str.lstrip('RETURN')
        if str.startswith('3'):
            str = str.lstrip('3')
        if str.startswith('BLOCKHASH'):
            str = str.lstrip('BLOCKHASH')
        if str.startswith('0'):
            str = str.lstrip('0')
        if str.startswith('1'):
            str = str.lstrip('1')
        if str.startswith('2'):
            str = str.lstrip('2')
        if str.startswith('4'):
            str = str.lstrip('4')
        if str.startswith('5'):
            str = str.lstrip('5')
        if str.startswith('6'):
            str = str.lstrip('6')
        if str.startswith('7'):
            str = str.lstrip('7')
        if str.startswith('8'):
            str = str.lstrip('8')
        if str.startswith('9'):
            str = str.lstrip('9')
        if str.startswith('GIN'):
            str = str.lstrip('GIN')
        if str.startswith('RESS'):
            str = str.lstrip('RESS')
        if str.startswith('ER'):
            str = str.lstrip('ER')
        if str.startswith('DATALOAD'):
            str = str.lstrip('DATALOAD')
        if str.startswith('DATASIZE'):
            str = str.lstrip('DATASIZE')
        if str.startswith('MOD'):
            str = str.lstrip('MOD')
        if str.startswith('VALUE'):
            str = str.lstrip('VALUE')
        textF.write(str)
    textF.close()
    return "true"
def addData(x):
    listADD = []
    #listADD.append(x)
    dataA = read_out_file("word2vecNew.txt")
    for j in dataA:
        list = j.split(" ")
        newlist = []
        for i in list:
            if i.__eq__(""):
                continue;
            else:
                i = i.strip("\n")
                newlist.append(i)
        # print(newlist)
        m = 0
        for j in newlist:
            m = m + float(j)
        listADD.append(m)
    return listADD
import time
if __name__ == "__main__":
    begin_time = time.time()
    print(begin_time)
    print('可重入漏洞：')
    conOpCodesPath = 'D:/pyProjects/pythonProject/mlVunDet/overfl/'
    conOpCodesPathList = get_filelist(dir, conOpCodesPath, "txt")
    print(conOpCodesPathList)
    daoNum=0
    num=0
    txNum=0
    normal=0
    bothTwo=0
    daoList=[]
    txList=[]
   # listLast = []
    listword=[]
    label=[]
    for file in conOpCodesPathList:
      #if file.__eq__('D:/pyProjects/pythonProject/mlVunDet/oOPCODES/60.txt')  :
                listLast = []
                num = num + 1
        #if num < 100:
                #print(getsize(file))
                flag = 'false'  # 默认表示无漏洞
                data = read_out_file(file)  # 读取文件
                print(file)
                name=file.strip('D:/pyProjects/pythonProject/mlVunDet/overfl/')
                x=name.strip('.tx')
                print(x)
                blockListAndpreSucList = blockListAndpreSucListS(data)
                blockListS = blockListAndpreSucList[0]  # 区块节点
                preSucListS = blockListAndpreSucList[1]  # 区块节点的后继节点列表
                succListS = blockListAndpreSucList[2]  # 区块节点的前继节点列表
                blockNumAndSuccessor = blockNumAndSuccessors(blockListS, preSucListS)  # 区块号以及区块节点的后继节点列表
                blockNumAndprecessor = blockNumAndSuccessors(blockListS, succListS)  # 区块号以及区块节点的前继节点列表
                Successor = Successors(blockNumAndSuccessor)  # 后继节点

                numCodeDictS = {}  # 将节点以及其后继节点  转换为 字典格式
                for i, j in zip(blockListS, Successor):  # 同时循环两个列表
                    numCodeDictS[i] = j  # 此时i为键，j为值，即{i：j}
                # print("numCodeDictS:")
                # print(numCodeDictS)
                opFe = []
                operateCodeListS = operateCodeList(data)  # 提取操作码指令
                # print(operateCodeListS)
                for list in operateCodeListS:
                    lists = []
                    for i in list:
                        # print(i)
                        if len(i)>1:
                            m = i.split(' ')[1]
                            lists.append(m)
                    #print(lists)
                    if 'ADD' in lists and 'LT' not in lists  and'GT' not in lists  and 'EQ' not in lists and 'ISZERO' not in lists and 'MISSING' not in lists:
                            opFe.append(lists)
                # print(opFe)
                print(len(opFe))
                #print(max(opFe))
                # test_senTIME = []
                if len(opFe)>0:
                   # test_senTIME = []
                    print(max(opFe))
                    if len(max(opFe)) > 1:
                            listLast=max(opFe)
                    print(listLast)
                    if len(listLast):
                        test_senTIME = []
                        test_senTIME.append(listLast)
                    # print(list)
                    # test_senTIME = []
                    # test_senTIME.append(listLast)
                        print(test_senTIME)
                        if len(test_senTIME):
                            model = Word2Vec(sentences=test_senTIME, vector_size=10, window=1, min_count=1, workers=1)
                            model.wv.save_word2vec_format('word2vec.txt', binary=False)
                            data = read_out_file("./word2vec.txt")
                            text_file = open("word2vecNew.txt", "w")
                            for i in listLast:
                                code = ''
                                # print(i)
                                for string in data:
                                    if string.endswith("10\n"):
                                        continue;
                                    else:
                                        if string.startswith(i):
                                            code = string.lstrip(i)
                                            # print(code)
                                text_file.write(code)
                            text_file.close()
                            # print(model)
                            dataADD = read_out_file("word2vecNew.txt")
                            dealdata(dataADD)
                            listADD = addData(x)
                            label.append(listADD)
                #if 0 < int(x) < 10000:
                #if 10000 < int(x) < 20000:
                #if 20000 < int(x) < 30000:
                #if 30000 < int(x) < 40000:
                #if 40000 < int(x) < 50000:
                #if 50000< int(x) < 60000:
                #if 60000 < int(x) < 70000:
                #if 70000 < int(x) < 80000:
                #if 90000 < int(x) < 100000:
                #if 100000 < int(x) < 110000:
                #if 110000 < int(x) < 120000:
                #if 120000 < int(x) < 130000:
                #if 130000 < int(x) < 140000:
                #if 140000 < int(x) < 150000:
                #if 150000 < int(x) < 160000:
                #if 160000 < int(x) < 170000:
                #if 170000 < int(x) < 180000:
    print(label)
    print(len(label))
    textl = open("./overflow/labelListOVERFL.txt", "a")
    textl.write(str(label))
    textl.close()




































































































