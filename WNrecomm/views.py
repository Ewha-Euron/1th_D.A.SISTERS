from django.shortcuts import render, redirect

import pandas as pd
import numpy as np
import warnings; warnings.filterwarnings('ignore')

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
#import requests
import urllib.request
import json
from collections import OrderedDict

novel = pd.read_csv('WNrecomm/static/novel.csv',encoding='cp949').drop('Unnamed: 0',axis=1)
review = pd.read_csv('WNrecomm/static/review.csv')
text =  pd.read_csv('WNrecomm/static/text.csv').drop('Unnamed: 0',axis=1)
cos =  pd.read_csv('WNrecomm/static/cosine_sim.csv').drop('Unnamed: 0',axis=1)



def main(request):
    return render(request, 'main.html')

def q_base(request):
    return render(request, 'q_base.html')

def q1(request):
    return render(request, 'q1.html')

adult = 0 
finish = 0 

def q2(request):
    global adult, finish
    if request.method == 'GET':
        if request.GET.get('adultchild') =='adult_yes' :
              adult = 1 # adult_yes / adult_no
        if request.GET.get('finished') == 'finish_yes' : 
              finish = 1 # finish_yes / finish_no
    return render(request, 'q2.html')




dict_user=[0, 0, 0, 0, 0, 0]

def q3(request):
    if request.method == 'GET':
        if request.GET.get('chb'):
            selected = request.GET.get('chb')
            for i in range(0, len(selected)+1, 2) :
                dict_user[int(selected[i])-1] = 1 
            #print(dict_user)
            return render(request, 'q3.html')

        elif request.GET.get('search'):
            search = request.GET.get('search') # 검색어. json 형태로 보내기 
            idx_list = []
            for i in range(len(novel)) : 
                if str(search) in novel['제목'][i] : 
                    idx_list.append(i)

            search_result = []
            for i in idx_list:
                idx_dict = {
                    'index' : i,
                    'image' : novel.loc[i,'썸네일'], 
                    'title' : novel.loc[i,'제목'],
                    'author': novel.loc[i,'작가'],
                    'genre' : novel.loc[i,'장르']
                }
                search_result.append(idx_dict)

            #print(search_result)
            #targetJson = json.dumps(idx_dict)
            return render(request, 'q3.html',{'search_result' : search_result})

    return render(request, 'q3.html')

cart_result = [] # 계속해서 장바구니에 쌓일 예정
def add_novel_list(request):
    if request.method == 'GET':
        rating = int(request.GET.get('rating'))
        n_i = int(request.GET.get('novel_index'))

        idx_dict = {
            'index' : n_i,
            'image' : novel.loc[n_i,'썸네일'], 
            'title' : novel.loc[n_i,'제목'],
            'author': novel.loc[n_i,'작가'],
            'genre' : novel.loc[n_i,'장르'],
            'rating' : rating
        }
        cart_result.append(idx_dict)

    return redirect('q3')


def novel_list(request):
    return render(request, 'novel_list.html', {'cart_result' : cart_result})


def novel_delete(request):
    if request.method == 'GET':
        n_i_d = int(request.GET.get('novel_index_delete')) # 인덱스 하나 날아옴
        for i in range(len(cart_result)):
            if cart_result[i]['index'] == n_i_d :
                del cart_result[i]
                break
                
    return render(request, 'novel_list.html', {'cart_result' : cart_result})


def loading(request):
    return render(request, 'loading.html')


# 추천시스템
like = dict_user[0]
avgrating = dict_user[1]
totalreview = dict_user[2]
purchase = dict_user[3]
waiting = dict_user[4]
keywords = dict_user[5]

# 유저 데이터프레임 생성
def makeUserDF():
    user = pd.DataFrame({'ID' : ['user']*len(cart_result) , 'novelindex' : [0]*len(cart_result) , '평점' : [0]*len(cart_result) })
    for i in range(len(cart_result)): 
        user['novelindex'][i] = cart_result[i]['index']
        user['평점'][i] = cart_result[i]['rating']
    return user

## 1. 성인, 완결 필터링
def filtering():
    a = [] # 리뷰에서도 작품을 제외하기 위한 list -> 이 안의 작품들은 리뷰에서 지워짐
    f = []

    if adult == 0:
        a = novel[novel['성인'] == True].index.tolist()
        
    if finish == 1:
        f = novel[novel['완결'] == False].index.tolist()

    # 이중리스트를 제거하고 중복 값 삭제
    f_book = list(set(sum([a, f], [])))

    # 리뷰에서 필터링된(f_book) 작품 제거
    idx_del_review = review[review['novelindex'].isin(f_book)].index
    idx_del_novel = novel[novel['novelindex'].isin(f_book)].index

    review_new = review.drop(idx_del_review)
    novel_new = novel.drop(idx_del_novel)

    return review_new, novel_new

## 2. CB
def recommended_wn_each(title, novel_new):
    recommended_wn = []
    indices = pd.Series(novel['제목'])

    idx = indices[indices == title].index[0]
    score_google = pd.Series(cos[idx]).iloc[novel_new.index].sort_values(ascending = False)
    score_google=score_google.iloc[novel_new.index]
    top_10_indices = score_google.iloc[2:11].index  
    
    for i in top_10_indices:
        recommended_wn.append(novel_new['제목'][i])
        
    return recommended_wn

def cb_recommend_all(index, novel_new):
    topn=[]
    title_list = list(novel_new['제목'].iloc[index])
    for i in title_list :
        for j in recommended_wn_each(i, novel_new):
            topn.append(j)
    return list(set(topn))

def top_10(index, novel_new):
    waiting = dict_user[4]
    keywords = dict_user[5]

    cb = 0 
    scaler = MinMaxScaler()
    list_topn = cb_recommend_all(index, novel_new)
    list_gidamoo = [] 
    for i in range(len(novel_new)) : 
        if novel_new['제목'][i] in list_topn : 
            list_gidamoo.append((i,novel_new['제목'][i],novel_new['기다무'][i], novel_new['무료공개'][i],novel_new['가중평균'][i]))
  
    df=pd.DataFrame({x[0]:x[1:] for x in list_gidamoo}).T.reset_index()
    df.columns = ['index','제목','기다무','무료공개','가중평균']

    if waiting == 1:
        df['기다무'] = scaler.fit_transform(df[['기다무']]) + 1
        df['가중평균'] = df['가중평균'] * df['기다무']

        df['무료공개'] = scaler.fit_transform(df[['무료공개']]) + 1
        df['가중평균'] = df['가중평균'] * df['무료공개']     
        
        cb += 1
    
    if keywords == 1:
        cb += 2

    return df[['index','제목','가중평균']].sort_values(by = '가중평균', ascending= False)[:2+cb]['index'].tolist()

def CB(user, novel_new):
    global cos
    cos = np.array(cos)
    cb_recmm=top_10(user['novelindex'], novel_new)
    return cb_recmm

## 3. CF
# 예측 평점을 구하는 함수, R(u, i)에 관한 식
def predict_rating(ratings_arr, item_sim_arr):
    ratings_pred = ratings_arr.dot(item_sim_arr) / np.array([np.abs(item_sim_arr).sum(axis=1)])
    return ratings_pred

def cf_predict(user, review_new, ID):
    review_user = pd.concat([user, review_new], axis = 0)

    # user rating matrix
    ratings = review_user.pivot_table('평점', index = 'ID', columns = 'novelindex')
    ratings = ratings.fillna(0) # 없는 평점은 0으로

    # item dim_df -> 영화간 유사도 계산
    ratings_T = ratings.transpose()
    item_sim = cosine_similarity(ratings_T, ratings_T)
    item_sim_df = pd.DataFrame(data = item_sim, index = ratings.columns, columns = ratings.columns)

    predict = predict_rating(ratings, item_sim_df)
    unseen_lst = unseen_item(ratings, ID)

    return predict, unseen_lst

# 유저가 보지 않은 소설 반환
def unseen_item(ratings, ID):
    user_rating = ratings.loc[ID, :]
    already_seen = user_rating[user_rating>0].index.tolist()
    
    novel_list = ratings.columns.tolist()
    unseen_list = [novel for novel in novel_list if novel not in already_seen]
    
    return unseen_list

# 추천
def cf_item_recomm(pred_df, ID, unseen_list, top_n=10):
    recomm_novel = pred_df.loc[ID, unseen_list].sort_values(ascending=False)[:top_n]
    return recomm_novel

def CF(user, review_new, novel_new):
    like = dict_user[0]
    avgrating = dict_user[1]
    totalreview = dict_user[2]
    purchase = dict_user[3]

    cf = 0
    scaler = MinMaxScaler()

    # review에 없는 작품 index list에 append
    d = review_new.novelindex.sort_values().unique().tolist()
    x = range(0, len(novel_new))
    nonereview = []

    sd = sum(d)
    xd = sum(x)

    for i in x: 
        if i not in d:
            nonereview.append(i)

    if like == 1:
        like_scale = scaler.fit_transform(novel_new[['좋아요수']]) + 1
        like_scale = sum(like_scale.tolist(), [])
        
        # 계산된 가중치에서 rating table에 없는 것들 제외(행렬곱을 위함)
        for index in sorted(nonereview, reverse = True):
            del like_scale[index]
        
        cf += 1

    if avgrating == 1:
        avgrating_scale = scaler.fit_transform(novel_new[['평균별점']]) + 1
        avgrating_scale = sum(avgrating_scale.tolist(), [])
        
        for index in sorted(nonereview, reverse = True):
            del avgrating_scale[index]
            
        cf += 1

    if totalreview == 1:
        totalreview_scale = scaler.fit_transform(novel_new[['전체리뷰수']]) + 1
        totalreview_scale = sum(totalreview_scale.tolist(), [])
        
        for index in sorted(nonereview, reverse = True):
            del totalreview_scale[index]
        
        cf += 1
        
    if purchase == 1:
        purchase_scale = scaler.fit_transform(novel_new[['구매자수']]) + 1
        purchase_scale = sum(purchase_scale.tolist(), [])
        
        for index in sorted(nonereview, reverse = True):
            del purchase_scale[index]
        
        cf += 1

    ID = 'user'
    predict, unseen_lst = cf_predict(user, review_new, ID)

        # 가중치 부여 
    if like == 1:
        predict * np.array(like_scale)

    if avgrating == 1:
        predict * np.array(avgrating_scale)

    if purchase == 1:
        predict * np.array(purchase_scale)

    if totalreview == 1:
        predict * np.array(totalreview_scale)

    recomm_novel = cf_item_recomm(predict, ID, unseen_lst, top_n = 2 + cf)
    cf_recmm = recomm_novel.index.tolist()

    return cf_recmm


def result(request):
    user = makeUserDF()
    review_new, novel_new = filtering()

    cb_recmm = CB(user, novel_new)
    cf_recmm = CF(user, review_new, novel_new)
    recmm_idx = cb_recmm + cf_recmm

    recmm_result = [] # 프론트에서 접근 가능한 형태로 변환
    for i in recmm_idx:
        idx_dict = {
                    'index' : i,
                    'image' : novel.loc[i,'썸네일'], 
                    'title' : novel.loc[i,'제목'],
                    'author': novel.loc[i,'작가'],
                    'genre' : novel.loc[i,'장르'],
                    'url' : novel.loc[i, '링크']
                }
        recmm_result.append(idx_dict)
    return render(request, 'result.html', {'recmm_result' : recmm_result})





'''
##2. CF##
# review에 없는 작품 index list에 append
d = review.novelindex.sort_values().unique().tolist()
x = range(0, 457)
nonereview = []

sd = sum(d)
xd = sum(x)

for i in x: 
    if i not in d:
        nonereview.append(i)

if like == 1:
    like_scale = scaler.fit_transform(novel_new[['좋아요수']]) + 1
    like_scale = sum(like_scale.tolist(), [])
    
    # 계산된 가중치에서 rating table에 없는 것들 제외(행렬곱을 위함)
    for index in sorted(nonereview, reverse = True):
        del like_scale[index]
    
    cf += 1

if avgrating == 1:
    avgrating_scale = scaler.fit_transform(novel_new[['평균별점']]) + 1
    avgrating_scale = sum(avgrating_scale.tolist(), [])
    
    for index in sorted(nonereview, reverse = True):
        del avgrating_scale[index]
        
    cf += 1

if totalreview == 1:
    totalreview_scale = scaler.fit_transform(novel_new[['전체리뷰수']]) + 1
    totalreview_scale = sum(totalreview_scale.tolist(), [])
    
    for index in sorted(nonereview, reverse = True):
        del totalreview_scale[index]
    
    cf += 1
    
if purchase == 1:
    purchase_scale = scaler.fit_transform(novel_new[['구매자수']]) + 1
    purchase_scale = sum(purchase_scale.tolist(), [])
    
    for index in sorted(nonereview, reverse = True):
        del purchase_scale[index]
    
    cf += 1

review_user = pd.concat([user, review_new], axis = 0)

# user rating matrix
ratings = review_user.pivot_table('평점', index = 'ID', columns = 'novelindex')
ratings = ratings.fillna(0) # 없는 평점은 0으로

# item dim_df -> 유사도 계산
ratings_T = ratings.transpose()
item_sim = cosine_similarity(ratings_T, ratings_T)
item_sim_df = pd.DataFrame(data = item_sim, index = ratings.columns, columns = ratings.columns)

# 예측 평점을 구하는 함수, R(u, i)에 관한 식
def predict_rating(ratings_arr, item_sim_arr):
    ratings_pred = ratings_arr.dot(item_sim_arr) / np.array([np.abs(item_sim_arr).sum(axis=1)])
    return ratings_pred

predict = predict_rating(ratings, item_sim_df)


# 가중치 부여 
if like == 1:
    predict * np.array(like_scale)

if avgrating == 1:
    predict * np.array(avgrating_scale)

if purchase == 1:
    predict * np.array(purchase_scale)

if totalreview == 1:
    predict * np.array(totalreview_scale)
    

# 유저가 보지 않은 소설 반환
def unseen_item(ratings, ID):
    user_rating = ratings.loc[ID, :]
    already_seen = user_rating[user_rating>0].index.tolist()
    
    novel_list = ratings.columns.tolist()
    unseen_list = [novel for novel in novel_list if novel not in already_seen]
    
    return unseen_list

# 추천
def cf_item_recomm(pred_df, ID, unseen_list, top_n=10):
    recomm_novel = pred_df.loc[ID, unseen_list].sort_values(ascending=False)[:top_n]
    return recomm_novel

ID = 'user'

unseen_lst = unseen_item(ratings, ID)
recomm_novel = cf_item_recomm(predict, ID, unseen_lst, top_n = 2 + cf)

# 상위 추천 작품 list (인덱스형태)
cf_recmm = recomm_novel.index.tolist()

##4. 추천 결과 합치기##
recmm_idx = cb_recmm + cf_recmm

recmm_result = [] # 프론트에서 접근 가능한 형태로 변환
    for i in recmm_idx:
        idx_dict = {
                    'index' : i,
                    'image' : novel.loc[i,'썸네일'], 
                    'title' : novel.loc[i,'제목'],
                    'author': novel.loc[i,'작가'],
                    'genre' : novel.loc[i,'장르'],
                    'url' : novel.loc[i, '링크']
                }
        recmm_result.append(idx_dict)


#####################################################
'''