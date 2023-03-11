'''
Author: ywy
'''
import jieba
import logging
import pandas as pd
import operator

#jieba log配置 关闭
jieba.setLogLevel(logging.INFO)

file = open('keywords.txt','r',encoding='utf-8')
lines = file.readlines()

words =[]
for line in lines:
    line = line.strip('\n')
    #分词
    seg_list = list(jieba.cut(line, cut_all=False))
    while ' ' in seg_list:
        seg_list.remove(' ')
    words = words + seg_list
    

word_dict = {}
for key in words:
  word_dict[key] = word_dict.get(key, 0) + 1


word_dict = dict(sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True))  #按照value值升序


df=pd.DataFrame.from_dict(word_dict, orient='index')
print(df)
file.close()

df.to_csv(path_or_buf="words_frequency.csv")



