import scrapy
import pandas as pd
from pandas import ExcelWriter
class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['dxsbb.com']
    start_urls = ['https://www.dxsbb.com/news/42613.html']

    def parse(self, response):
        new_school_name_list = []
        new_area_list = []
        school_name_list = response.xpath('//*[@id="content"]/div[2]/div/table/tbody/tr/td[2]').extract()
        area_list = response.xpath('//*[@id="content"]/div[2]/div/table/tbody/tr/td[3]').extract()
        s_count = 0
        a_count = 0
        for school_name in school_name_list:
            if s_count == 0:
                s_count = s_count + 1
                continue
            school_name = school_name[4:]
            school_name = school_name[:-5]
            new_school_name_list.append(school_name)
        for area in area_list:
            if a_count == 0:
                a_count = a_count + 1
                continue
            area = area[4:]
            area = area[:-5]
            new_area_list.append(area)
        rankdata = {"学校":new_school_name_list,"地区/国家":new_area_list}
        rankData = pd.DataFrame(rankdata)
        rankData.index=rankData.index+1
        print(rankData.head(5))
        
        count_dict={}
        for key in new_area_list:
            count_dict[key]=count_dict.get(key,0)+1  

        count_data = {"地区/国家":count_dict.keys(),"出现次数":count_dict.values()}
        countData = pd.DataFrame(count_data)
        countData = countData.sort_values(by="出现次数",ascending=False)
        countData = countData.reset_index(drop=True)

        countData.index=countData.index+1
        print(countData.head(5))
        
        all_school_num = len(new_area_list)
        percent_list = []
        for count in count_dict.values():
            percent = round(count/all_school_num,3)
            percent_list.append(percent)
        education_data = {"国家/地区":count_dict.keys(),"高校出现次数":count_dict.values(),"占比":percent_list}
        educationData = pd.DataFrame(education_data)
        educationData.index=educationData.index+1
        print(educationData.head(5))

        try:
            rankData.to_excel("1_排名.xlsx")
            print("保存成功1")
            educationData.to_excel("3_教育质量.xlsx")
            print("保存成功3")
            countData.to_excel("2_上榜国家或地区统计.xlsx")
            print("保存成功2")

        except Exception as e:
            print(e)

        
        pass
