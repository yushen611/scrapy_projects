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
file.close()



out_f = open("jieba_words_forMR.txt","w",encoding='utf-8')
for word in words:
  out_f.write(word+'\n')
out_f.close()


