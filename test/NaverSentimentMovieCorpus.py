# -*- coding: utf-8 -*-
"""감정분석.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rWjmvYk5mQ1Nm37ay1Kcr_ce4_LHjnNp

# 1.Naver Sentiment Movie Corpus dataset을 이용한 감정분석
"""

import tensorflow as tf
import numpy as np
path_to_train_file=tf.keras.utils.get_file('train.txt','https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt')
path_to_test_file=tf.keras.utils.get_file('test.txt','https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt')

train_text=open(path_to_train_file,'rb').read().decode(encoding='utf-8')
test_text=open(path_to_test_file,'rb').read().decode(encoding='utf-8')

print('Length of text:{} characters'.format(len(train_text)))
print('Length of text:{} characters'.format(len(test_text)))
print()

print(train_text[:300])
#각 행은 tab으로 구분

train_Y=np.array([[int(row.split('\t')[2])] for row in train_text.split('\n')[1:] if row.count('\t')>0])
test_Y=np.array([[int(row.split('\t')[2])] for row in test_text.split('\n')[1:] if row.count('\t')>0])
print(train_Y.shape,test_Y.shape)
print(train_Y[:5])

#전처리
import re
def clean_str(string):
  string = re.sub(r"[^가-힣A-Za-z0-9(),!?\'\`]", " ", string)     
  string = re.sub(r"\'s", " \'s", string) 
  string = re.sub(r"\'ve", " \'ve", string) 
  string = re.sub(r"n\'t", " n\'t", string)  
  string = re.sub(r"\'re", " \'re", string) 
  string = re.sub(r"\'d", " \'d", string) 
  string = re.sub(r"\'ll", " \'ll", string) 
  string = re.sub(r",", " , ", string) 
  string = re.sub(r"!", " ! ", string) 
  string = re.sub(r"\(", " \( ", string) 
  string = re.sub(r"\)", " \) ", string) 
  string = re.sub(r"\?", " \? ", string) 
  string = re.sub(r"\s{2,}", " ", string)
  string=re.sub(r"\'{2,}", "\' ",string)
  string=re.sub(r"\' ", "",string)

  return string.lower()

train_text_X=[row.split('\t')[1] for row in train_text.split('\n')[1:] if row.count('\t') >0]
train_text_X=[clean_str(sentence) for sentence in train_text_X]
sentences=[sentence.split(' ') for sentence in train_text_X]
for i in range(5):
  print(sentences[i])

import matplotlib.pyplot as plt
sentence_len=[len(sentence) for sentence in sentences]
sentence_len.sort()
plt.plot(sentence_len)
plt.show()

print(sum([int(l<=25) for l in sentence_len]))

sentences_new=[]
print(sentences)
for sentence in sentences:
  sentences_new.append([word[:5] for word in sentence][:25])
sentences=sentences_new
for i in range(5):
  print(sentences[i])

#전처리
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer=Tokenizer(num_words=20000)
tokenizer.fit_on_texts(sentences)
train_X=tokenizer.texts_to_sequences(sentences)
train_X=pad_sequences(train_X,padding='post')

print(train_X[:5])

print(tokenizer.index_word[19999])
print(tokenizer.index_word[20000])
temp=tokenizer.texts_to_sequences(['#$#$#','경우는','잊혀질','연기가'])
print(temp)
temp=pad_sequences(temp,padding='post')
print(temp)

model=tf.keras.Sequential([
                           tf.keras.layers.Embedding(20000,300,input_length=25),
                           tf.keras.layers.LSTM(units=50),
                           tf.keras.layers.Dense(2,activation='softmax')
])

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
model.summary()

history=model.fit(train_X,train_Y,epochs=5,batch_size=128,validation_split=0.2)
