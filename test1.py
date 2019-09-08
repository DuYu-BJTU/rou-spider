import requests
from lxml import etree
from functools import reduce

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
           'Cookie':'pgv_pvid=7377727156; pgv_info=ssid=s9030076508; JSESSIONID=881A33E2ADC0834C1CD9AE31BF4EBA6F',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'}
url = 'http://news.bjtu.edu.cn/info/1044/30257.htm'

html = requests.get(url, headers=headers)
web = html.content.decode('UTF-8')

with open('bjtunews.html','w',encoding='UTF-8') as f:
    f.write(web)
f.close()

html = etree.HTML(web)

parse = '/html/body/div[1]/div[3]/div/div[1]/div[2]/ul/li[3]/a/{}'
result_text = html.xpath(parse.format('text()'))
result_href = html.xpath(parse.format('@href'))

print(result_text )
print(result_href )

for txt in result_text:
    print(reduce(lambda str1, str2: str1.replace(str2, '北大'), [txt, '、','\r\n','【','】','北京']))
    print(txt.strip())

with open('bjtunews.csv', 'w', encoding='utf-8') as f:
    f.write('news,url\n')
    for txt, href in zip(result_text, result_href):
        newtxt = txt.strip()
        newhref = href.strip()+'\n'
        f.write(','.join([newtxt, newhref]))
    f.close()