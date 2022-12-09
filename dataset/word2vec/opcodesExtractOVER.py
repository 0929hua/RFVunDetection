import csv
import json
import os
from gensim.models import Word2Vec
from numpy.compat import long
from sklearn.datasets import load_iris
import numpy as np
from os.path import join, getsize
###读取文件
import os
import sys

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
        if str.startswith('VALUE'):
            str = str.lstrip('VALUE')
        if str.startswith('DATASIZE'):
            str = str.lstrip('DATASIZE')
        if str.startswith('ODE'):
            str = str.lstrip('ODE')
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
    num=0
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
