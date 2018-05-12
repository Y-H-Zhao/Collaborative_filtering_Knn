# -*- coding: utf-8 -*-
"""
Created on Sat May 12 19:46:51 2018

@author: ZYH
"""
import json
import numpy as np

from pearson_score import pearson_score
#from find_similar_users import find_similar_users

#定义一个为给定用户生成推荐电影的函数
def generate_recommendations(dataset, user):
    #首先检查是否存在该用户
    if user not in dataset:
        raise TypeError('User' + user + 'not in dataset')
    #计算该用户与其他用户的相关系数
    total_scores = {}
    #similarity_sums = {}
    
    for u in [x for x in dataset if x != user]:
        similar_score = pearson_score(dataset, user, u)
        
        if similar_score <= 0:
            continue #跳过
        #找到该用户没看过的电影 ，也就是没有评分的
        for item in [x for x in dataset[u] if x not in dataset[user] or 
                     dataset[user][x] ==0]:
            #update 是字典的更新添加方式
            total_scores.update({item:dataset[u][item] * similar_score})
            
    #如果该用户看过所有电影，不推荐
    if len(total_scores) == 0:
        return ['No recommendations possible']
    
    #生成电影评分标准化表 其实就是把评分弄出来
    movie_ranks = np.array([[score,item] for item,score in total_scores.items()])
    # 对相关系数倒叙排列
    movie_ranks = movie_ranks[np.argsort(movie_ranks[:, 0])[::-1]]
    # 得到推荐电影
    recommendations = [movie for _, movie in movie_ranks]

    return recommendations
 
if __name__=='__main__':
    data_file = 'movie_ratings.json'

    with open(data_file, 'r') as f:
        data = json.loads(f.read())

    user = 'Michael Henry'
    print("\nRecommendations for " + user + ":")
    movies = generate_recommendations(data, user) 
    for i, movie in enumerate(movies):
        print(str(i+1) + '. ' + movie)

    user =('John Carson') 
    print("\nRecommendations for " + user + ":")
    movies = generate_recommendations(data, user) 
    for i, movie in enumerate(movies):
        print(str(i+1) + '. ' + movie)
