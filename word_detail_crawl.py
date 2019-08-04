import requests
from bs4 import BeautifulSoup
import re


def crawl(word):
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    try:
        url = 'https://dict.baidu.com/s?wd={0}&device=pc&from=home'.format(word)
        response = requests.get(url=url,headers=headers).text
        content = BeautifulSoup(response,'lxml')
        soup = content.find(id="word_bishun")
        if soup == None:
            url = 'https://dict.baidu.com/s?wd={0}&ptype=zici'.format(word)
            response = requests.get(url=url,headers=headers).text
            content = BeautifulSoup(response,'lxml')
            # print(response)
            # 笔顺动图
            soup = content.find(id="word_bishun")
            bishun = re.findall(r'data-src="(.*?)"',str(soup))[0]
            # 拼音
            soup = content.find(id="pinyin")
            pinyins = soup.find_all('b')
            pinyin = ''
            for i in pinyins:
                i = re.findall(r'>(.*?)<',str(i))[0]
                pinyin = pinyin + ' ' + i
            pinyin = pinyin.strip(' ')
            # 部首
            soup = content.find(id="radical")
            bushou = soup.find('span').get_text()
            # 笔画
            soup = content.find(id="stroke_count")
            bihua = soup.find('span').get_text()
            # 组词
            soup = content.find(class_="related_idiom").get_text()
            zuci = soup.replace('\n',' ').strip(' ').rstrip(' 更多') # 当组词过多时防止末尾出现更多这一链接词
            # 近反义词
            try:
                syns = content.find(id="synonym-content").get_text().strip('\n') # 单独执行时不报错且不执行后面的语句
                syn = ''
                for i in syns:
                    if ishan(i):
                    	syn += i
            except:
                syn = 'Nan'
            try:
                ants = content.find(id="antonym-content").get_text().strip('\n')
                ant = ''
                for i in ants:
                    if ishan(i):
                    	ant += i
            except:
                ant = 'Nan'
            jinfan = syn + ' ' + ant
            # print(word, bishun, pinyin, bushou, bihua, zuci, jinfan)
        else:
            bishun = re.findall(r'data-src="(.*?)"',str(soup))[0]
            # 拼音
            soup = content.find(id="pinyin")
            pinyins = soup.find_all('b')
            pinyin = ''
            for i in pinyins:
                i = re.findall(r'>(.*?)<',str(i))[0]
                pinyin = pinyin + ' ' + i
            pinyin = pinyin.strip(' ')
            # 部首
            soup = content.find(id="radical")
            bushou = soup.find('span').get_text()
            # 笔画
            soup = content.find(id="stroke_count")
            bihua = soup.find('span').get_text()
            # 组词
            soup = content.find(class_="related_idiom").get_text()
            zuci = soup.replace('\n',' ').strip(' ').rstrip(' 更多') # 当组词过多时防止末尾出现更多这一链接词
            # 近反义词
            try:
                syns = content.find(id="synonym-content").get_text().strip('\n') # 单独执行时不报错且不执行后面的语句
                syn = ''
                for i in syns:
                    if ishan(i):
                    	syn += i
            except:
                syn = '暂无近义词'
            try:
                ants = content.find(id="antonym-content").get_text().strip('\n')
                ant = ''
                for i in ants:
                    if ishan(i):
                    	ant += i
            except:
                ant = '暂无反义词'
            jinfan = syn + ' ' + ant

        result = {
            'word': word,
            'bishun': bishun,
            'pinyin': pinyin,
            'bushou': bushou,
            'bihua': bihua,
            'zuci': zuci,
            'jinfan': jinfan
        }
        return result
    except:
        return None

# find_all() 方法没有找到目标是返回空列表, find() 方法找不到目标时,返回 None

# 判断是否为一个中文汉字
def ishan(text):
	if len(text) == 1:
		return all('\u4e00' <= char <= '\u9fff' for char in text)
	else:
		return False


if __name__ == '__main__':
	#  你我1
	#  了2
	result = crawl('了')
	print(result)
