import scrapy
from sqlalchemy import false

from listening.items import ListeningItem
import Levenshtein


class YasiSpider(scrapy.Spider):
    name = 'yasi'
    # allowed_domains = ['www.laokaoya.com']
    start_urls = ['http://www.laokaoya.com/43420.html']
    
    uncontaineds = ['词汇','答案解析','剑','雅思听力','原文',':'] + [('Q'+str(x+1)+',' ) for x in range(40)]+ [('Q'+str(x+1)+' ' ) for x in range(40)]
    Qwords = [('Q'+str(x+1)) for x in range(40)] #Q1-Q40

    #统计字符串大写字母比例 同于判断是否是人名
    def __up_str_proportion(self,str_in):
        up_count = 0
        str_len = len(str_in)
        for i in str_in:#for循环遍历   
            if i.isupper():#语句判断
                up_count += 1
        return up_count/str_len

    def parse(self, response):
        #获取首页各个时期听力真题题目的链接
        a_list = response.xpath('//*[@id="content"]/div[1]/div[2]/div[3]/div[2]/p/a/@href')
        for i,a in enumerate(a_list):
            if i <= 15:
                # 剑桥4的数据很多不符合格式 就不爬取了
                continue
            #二级界面的url
            url = a.extract()
            print(url)
            #对二级界面发起访问
            yield scrapy.Request(url=url,callback=self.parse_second,meta={'index':i})

        pass
    
    def parse_second(self,response):
        print("二级界面{}".format(response.meta['index']),end="————")
        #爬取所有红色字体的字
        # red_a_list = response.xpath('//*[@id="content"]/div[1]/div[2]/div[3]/div[2]/p/span/strong//text()')
        
        red_a_list = response.xpath('//strong//text()')
        #爬取标题
        title = response.xpath('//*[@id="content"]/div[1]/div[2]/div[1]/div/h2//text()').extract_first()
        print(title)

        words=[] #存放考点词
        for i,red_a in enumerate(red_a_list):
            red_word = red_a.extract()
            is_right = True #是否是正确的word
            #判断是否正确
            for uncontain in self.uncontaineds:
                if red_word.find(uncontain)>=0:
                    is_right = False
                    break
            #判断与Q的编辑距离
            for Q in self.Qwords:
                if red_word.find(Q)>=0:
                    if Levenshtein.distance(Q,red_word) <=6:
                        is_right = False
                        break
            #判断是否是人名
            if self.__up_str_proportion(red_word) >=0.79:
                is_right = False
            #如果正确就加入words
            if is_right:
                words.append(red_word)
        #输出words观察正确性
        for word in words:
            print(word)

        #给items赋值
        item = ListeningItem()
        item['title'] = title
        item['words'] = words

        #把itmes返回管道
        yield item

