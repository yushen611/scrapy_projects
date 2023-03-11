'''
Author: ywy
'''
'''
Author: ywy
'''
from base64 import encode
import pandas as pd
import operator

#让print可以打印unicode
import io  
import sys 
from urllib import request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')


f  = open("jieba_words_forMR.txt","r",encoding='utf-8')
words=[]
for line in f:
    line = line.strip('\n')
    words.append(line)
f.close()

word_dict = {}
for key in words:
  word_dict[key] = word_dict.get(key, 0) + 1


word_dict = dict(sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True))  #按照value值升序



df=pd.DataFrame.from_dict(word_dict, orient='index')

#删除前200个太常见的词以及重复出现的符号
df.drop(df.index[[x for x in range(200)]],axis=0,inplace=True)

wordCloudWords=[]
for tup in df.itertuples():
    if 1>=len(tup[0]):
        continue
    linewords=tup[0]
    wordCloudWords.append(linewords)

out_f = open("wordCloudWords.txt","w",encoding='utf-8')
for word in wordCloudWords:
  out_f.write(word+'\n')
out_f.close()