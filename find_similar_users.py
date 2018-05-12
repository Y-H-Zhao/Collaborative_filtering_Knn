# -*- coding: utf-8 -*-
"""
Created on Sat May 12 19:19:45 2018

@author: ZYH
"""
'''
寻找数据集中的相似用户
'''
import json 
import numpy as np

from pearson_score import pearson_score

#定义一个返回相似用户的函数，需要三个参数，数据库，用户名，相似用户个数
def find_similar_users(dataset,user,num_users):
    #首先看该用户是否在数据库中
    if user not in dataset:
        raise TypeError('User' + user + 'not in dataset')
    #计算该用户和所有用户的相关系数
    scores = np.array([[x, pearson_score(dataset,user,x)] for x in dataset if user != x])
    #将得分按第二列排 返回索引的序号
    scores_sorted = np.argsort(scores[:,1])
    #倒序
    scores_sorted_dec = scores_sorted[::-1]
    #取num_users个最高的索引位置 返回电影和评分
    top_k = scores_sorted_dec[0:num_users]
    return scores[top_k]
#定义main
if __name__=='__main__':
    data_file = 'movie_ratings.json'

    with open(data_file, 'r') as f:
        data = json.loads(f.read())

    user = 'John Carson'
    print ("\nUsers similar to " + user + ":\n")
    similar_users = find_similar_users(data, user, 3) 
    print ("User\t\t\tSimilarity score\n")
    for item in similar_users:
        print (item[0], '\t\t', round(float(item[1]), 2))
