#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 迭代次数
ITERATION = 70
# 初始化向量
W = [1, 1, 1]


def createDate():
    lines_set = open('../data/Dataset_PLA.txt').readlines()
    train_set = lines_set[1:7]
    test_set = lines_set[9:13]
    return processData(train_set), processData(test_set)


# 将字符串分割成一个个的单词列表,组成一个二维数组
def processData(lines):
    dataList = []
    for line in lines:
        dataLine = line.strip().split()
        dataLine = [int(data) for data in dataLine]
        dataList.append(dataLine)
    return dataList


# 将一个向量与权重向量相乘,如果值大于0则返回1,反之返回-1
def sign(W, dataList):
    sum = 0
    for i in range(len(W)):
        sum += W[i] * dataList[i]

    if sum > 0:
        return 1
    return -1


# 重置矩阵,当算法预测的结果与实际结果不一致的时候W[k]=W[k]+y(t)*X[k]
def reSetW(W, trainData):
    signData = sign(W, trainData)
    if signData == trainData[-1]:
        return W
    for k in range(len(W)):
        W[k] = W[k] + trainData[-1] * trainData[k]
    return W


def train(W, trainDatas):
    for i in range(ITERATION):
        index = i % len(trainDatas)
        W = reSetW(W, trainDatas[i])

def predictData(W,train_set,test_set):
    newW=train(W,train_set)
    print newW
    for i in range(len(test_set)):
        result=sign(newW,test_set[i])
        print result

trainData,testData=createDate()
predictData(W,trainData,testData)
