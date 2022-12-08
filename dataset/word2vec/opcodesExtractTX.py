from gensim.models import Word2Vec
import os
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
        if str.startswith('PRICE'):
            str = str.lstrip('PRICE')
        if str.startswith('OD'):
            str = str.lstrip('OD')
        if str.startswith('VALUE'):
            str = str.lstrip('VALUE')
        if str.startswith('E'):
            str = str.lstrip('E')
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
    conOpCodesPath = 'D:/pyProjects/pythonProject/MachineLearningVulnerabilityDetection/dataset/opcodes/tx.origin/'
    conOpCodesPathList = get_filelist(dir, conOpCodesPath, "txt")
    label=[]
    for file in conOpCodesPathList:
                listLast=[]
                num = num + 1
                data = read_out_file(file)  # 读取文件
                name=file.strip(conOpCodesPath)
                x=name.strip('.tx')
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
                opFe = []
                operateCodeListS = operateCodeList(data)  # 提取操作码指令
                for list in operateCodeListS:
                    for i in list:
                        if i.__contains__('ORIGIN'):
                            opFe.append(list)
                if len(opFe) < 20:
                    for i in opFe[0]:
                        code = i.split(' ')[1]
                        print(code)
                        if 'MISSING' not in code:
                            listLast.append(code)
                    print(listLast)
                    test_senTIME = []
                    test_senTIME.append(listLast)
                    model = Word2Vec(sentences=test_senTIME, vector_size=10, window=1, min_count=1, workers=1)
                    model.wv.save_word2vec_format('word2vec.txt', binary=False)
                    data = read_out_file("./word2vec.txt")
                    text_file = open("word2vecNew.txt", "w")
                    for i in listLast:
                        code = ''
                        for string in data:
                            if string.endswith("10\n"):
                                continue;
                            else:
                                if string.startswith(i):
                                    code = string.lstrip(i)
                        text_file.write(code)
                    text_file.close()
                    dataADD = read_out_file("word2vecNew.txt")
                    dealdata(dataADD)
                    listADD = addData(x)
                    label.append(listADD)
    print(label)
    print(len(label))
    textl = open("./tx.origin/labelListTX.txt", "a")
    textl.write(str(label))
    textl.close()
































































































