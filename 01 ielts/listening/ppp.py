with open('keywords.txt',encoding='gbk') as file:
     content=file.read()
     print(content.rstrip())     ##rstrip()删除字符串末尾的空行
###逐行读取数据
for line in content:
    print(line)