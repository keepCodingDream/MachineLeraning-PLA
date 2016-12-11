#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv

# 迭代次数
ITERATION = 110
# 初始化向量
W = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
need_transfer_list = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'poutcome']
# 存放需要map字符串与分数的map
score_map = {}


# 将原始数据经过变换以后持久化存储到txt文件中
def processOriginalData2txt():
    test_set = csv.reader(open('data/bank.csv', 'rb'))
    train_set = csv.reader(open('data/bank-full.csv', 'rb'))
    return saveOriginalData2txt(train_set, 'train.txt'), saveOriginalData2txt(test_set, 'test.txt')


def saveOriginalData2txt(lines, file_name):
    dataList = []
    for line in lines:
        dataLine = line[0].strip().replace('"', '').replace("'", '').split(';')
        dataList.append(dataLine)
    names = dataList.pop(0)
    if not score_map:
        build_data2map(names, dataList)
    result_list = []
    for i in range(len(dataList)):
        sub_numbers = []
        for j in range(len(dataList[i]) - 1):
            number = dataList[i][j]
            if score_map.__contains__(names[j]):
                number = score_map.get(names[j]).get(dataList[i][j])
            sub_numbers.append(int(number))
        if 'no' == dataList[i][-1]:
            sub_numbers.append(-1)
        else:
            sub_numbers.append(1)
        result_list.append(sub_numbers)
    fileObject = open(file_name, 'w')
    for ip in result_list:
        for item in ip:
            fileObject.write(str(item))
            fileObject.write(' ')
        fileObject.write('\n')
    fileObject.close()


def createDate():
    train_set = open('train.txt').readlines()
    test_set = open('test.txt').readlines()
    return processData(train_set), processData(test_set)


# 将字符串分割成一个个的单词列表,组成一个二维数组
def processData(lines):
    dataList = []
    for line in lines:
        dataLine = line.strip().split()
        dataLine = [int(data) for data in dataLine]
        dataList.append(dataLine)
    return dataList


# 将需要将name解释成分数的list构造成score_map
def build_data2map(names, data_list):
    all_item_dic = {}
    fileObject = open('name_score.txt', 'w')
    for i in range(len(data_list)):
        for j in range(len(data_list[i])):
            if all_item_dic.__contains__(names[j]):
                item_list = all_item_dic[names[j]]
            else:
                item_list = set([])
            item_list.add(data_list[i][j])
            all_item_dic[names[j]] = item_list
    for name in all_item_dic.keys():
        if need_transfer_list.__contains__(name):
            item_score = {}
            item_list = list(all_item_dic.get(name))
            fileObject.write(name + ':')
            for i in range(len(item_list)):
                if 'unknown' == item_list[i]:
                    item_score[item_list[i]] = 0
                else:
                    item_score[item_list[i]] = i + 1
            fileObject.write(str(item_score))
            fileObject.write('\n')
            score_map[name] = item_score
    fileObject.close()


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
        W = reSetW(W, trainDatas[index])
    return W


# 使用测试集去测试训练后的W的正确度
def predictData(W, train_set, test_set):
    newW = train(W, train_set)
    print newW
    error_count = 0
    for i in range(len(test_set)):
        result = sign(newW, test_set[i])
        if result != int(test_set[i][-1]):
            error_count += 1
    print 1.0 * (len(test_set) - error_count) / len(test_set)


##避免多次format,只有第一次执行,以后只关注训练
# processOriginalData2txt()

trainData, testData = createDate()
predictData(W, trainData, testData)
