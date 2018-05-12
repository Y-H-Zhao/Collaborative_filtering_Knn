# -*- coding: utf-8 -*-
"""
Created on Sat May 12 18:50:04 2018

@author: ZYH
"""
'''
构造函数计算两人对电影的评分的皮尔逊相关系数
'''
import json
import numpy as np

def pearson_score(dataset,user1,user2):
    #看两人是否在数据库中出现
    if user1 not in dataset:
        raise TypeError('user1' + user1 + 'not in dataset')
    if user2 not in dataset:
        raise TypeError('user2' + user2 + 'not in dataset')
        
    #提取两人都评论过的电影
    rated_by_both = {}
    for item in dataset[user1]:
        if item in dataset[user2]:
            rated_by_both[item] = 1 
    num_ratings = len(rated_by_both)
    
    #如果没有相同评论电影，相关性为0
    if num_ratings==0:
        return 0
    #如果存在相同评论电影，计算皮尔逊相关系数
    #需要相同电影各自评分的 和 、平方和 、 对应乘积
    #各自和
    user1_sum = np.sum([dataset[user1][item] for item in rated_by_both])
    user2_sum = np.sum([dataset[user2][item] for item in rated_by_both])

    #各自平方和
    user1_squared_sum = np.sum([np.square(dataset[user1][item]) for item in rated_by_both])
    user2_squared_sum = np.sum([np.square(dataset[user2][item]) for item in rated_by_both])

    #对应乘积
    product_sum = np.sum([dataset[user1][item] * dataset[user2][item] for item in rated_by_both])

    #计算 Pearson correlation
    Sxy = product_sum - (user1_sum * user2_sum / num_ratings)
    Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
    Syy = user2_squared_sum - np.square(user2_sum) / num_ratings
    
    #分母为0
    if Sxx * Syy == 0:
        return 0
    #正常情况
    return Sxy / np.sqrt(Sxx * Syy)

#主函数测试
if __name__=='__main__':
    data_file = 'movie_ratings.json'

    with open(data_file, 'r') as f:
        data = json.loads(f.read())

    user1 = 'John Carson'
    user2 = 'Michelle Peterson'

    print("\nPearson score:")
    print(pearson_score(data, user1, user2)) 
    
