import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
def collaborative_filtering(userid='A1BB77SEBQT8VX', itemid='B00007GDFV'):
    df =pd.read_pickle('1LRecord.pkl').head(5000)
    pivot_table = pd.pivot_table(df, values='rating', index='userID', columns='productId')
    item_ratings = pivot_table[itemid]
    item_rated_by = item_ratings.dropna().index
    pivot_table.fillna(0, inplace=True)
    user_ratings = pivot_table.loc[userid].values.reshape(1, -1)
    item_ratings = pivot_table.loc[item_rated_by]
    similarity_scores = cosine_similarity(user_ratings, item_ratings)
    weighted_ratings = similarity_scores.dot(item_ratings.fillna(0))
    weighted_sum = similarity_scores.sum()
    predicted_rating = weighted_ratings / weighted_sum
    similar_users = list(pivot_table.index[np.argsort(-similarity_scores)])
    return similar_users



'''
productId                                                 B00007GDFV
title                           Buxton Heiress Pik-Me-Up Framed Case
imageURLHighRes    ['https://images-na.ssl-images-amazon.com/imag...
brand                                                         Buxton
rating                                                           3.0
date                                                     09 22, 2013
userID                                                A1BB77SEBQT8VX
productId                                                 B00007GDFV
reviewerName                                      Darrow H Ankrum II
reviewText         mother - in - law wanted it as a present for h...
summary                                          bought as a present
title                           Buxton Heiress Pik-Me-Up Framed Case
brand                                                         Buxton
feature            ['Leather', 'Imported', 'synthetic lining', 'F...
rank                              43,930inClothing,Shoesamp;Jewelry(
imageURLHighRes    ['https://images-na.ssl-images-amazon.com/imag...
'''