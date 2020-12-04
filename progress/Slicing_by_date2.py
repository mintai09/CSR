#!/usr/bin/env python
# coding: utf-8

# In[88]:


#.csv파일 받아와 날짜별로 packing


# In[1]:


import pandas as pd
raw_data=pd.read_csv('./dataset_(0806-1106).csv')
raw_data.head(10)


# In[2]:


#일자| [ pos, neg , mod ] | [ e1 e2 e3 e4 e5 e6 e7 e8 ] | [확진자, 사망자, ...]
from pandas import Series
import numpy as np
data=pd.DataFrame()
data['일자']=Series(raw_data['일자'])

#일자 column
data=data.drop_duplicates(['일자'],keep='first')
date_idx_list=list(data.index)
date_idx_list.append(len(raw_data)) # 끝값 넣어주기
print(date_idx_list)    #날짜별 인덱스 리스트 저장
data=data.reset_index(drop=True)

# emo2 [ pos, neg , mod ] column
# 날짜별 전체 뉴스의 기사를 긍부정 판단 후 소수로 확률 표현
emo2_list=['None']*93
for j in range(len(date_idx_list)-1):
    emo={'Pos':0,'Neg':0,'Mod':0}
    for i in range(date_idx_list[j],date_idx_list[j+1]):
        if raw_data.loc[i,'pos_neg']==1:emo['Pos']+=1
        elif raw_data.loc[i,'pos_neg']==-1:emo['Neg']+=1
        elif raw_data.loc[i,'pos_neg']==0: emo['Mod']+=1
    emo2_list[j]=emo
data['emo2']=emo2_list
display(data)


# In[99]:


# emo8 [ Anger, Anticipation, Disgust, Fear, Joy, Sadness, Surprise, Trust ] column
emo8_list=['None']*93
for j in range(len(date_idx_list)-1):
    emo={'Anger':0,'Antic':0,'Disg':0,'Fear':0,
        'Joy':0,'Sad':0,'Sup':0,'Trust':0}
    for i in range(date_idx_list[j],date_idx_list[j+1]):
        emo['Anger']+=raw_data.loc[i,'Anger_val']
        emo['Antic']+=raw_data.loc[i,'Anticipation_val']
        emo['Disg']+=raw_data.loc[i,'Disgust_val']
        emo['Fear']+=raw_data.loc[i,'Fear_val']
        emo['Joy']+=raw_data.loc[i,'Joy_val']
        emo['Sad']+=raw_data.loc[i,'Sadness_val']
        emo['Sup']+=raw_data.loc[i,'Suprise_val']
        emo['Trust']+=raw_data.loc[i,'Trust_val']
    emo8_list[j]=emo
data['emo8']=emo8_list
display(data)


# In[100]:


raw_data=pd.read_csv('./covid19_trend.csv')
'''
날짜:stateDt
당일확진자수:decCnt
당일격리해제수:clCnt
당일사망자수:dthCnt
당일결과음성수:enCnt
당일검사수:examCnt
'''

covid_data=raw_data[['stateDt','decCnt','enCnt','clCnt','dthCnt','examCnt']]
covid_data.columns=['일자','decCnt','enCnt','clCnt','dthCnt','examCnt']
covid_data=covid_data.loc[::-1]
covid_data=covid_data.reset_index(drop=True)
display(covid_data)
del covid_data['일자']


# In[101]:


covid=covid_data.to_dict('records')
data['covid']=pd.Series(covid)
data.columns=['data','emo2','emo8','covid']
data.drop(data.index[0],inplace=True)
display(data)


# In[102]:





# In[ ]:


#subjective 객관주관 분석
#데이터를 날짜당 50개씩 분할
#일자|본문|키워드
raw_data=pd.read_csv('./.csv')
raw_data=raw_data[['일자','본문']]
tmp=raw_data[['일자']]
tmp=tmp.drop_duplicates(['일자'],keep='first')
date_idx_list=list(data.index)
date_idx_list.append(len(raw_data)) # 끝값 넣어주기
sub_list=['None']*93

for j in range(len(date_idx_list)-1):
    contents_by_date=[] 
    for k in range(j,j+50):
        contents_by_date.append(raw_data.iloc(j,0))
    sub_list[j]=contents_by_date
    
data['subjective']=sub_list
display(data)


# In[ ]:


data.to_csv('Data.txt',index=False,sep='\t')

