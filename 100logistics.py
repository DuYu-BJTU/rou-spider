import requests
from lxml import etree

#代理信息
start_url = 'http://www.bfb56.com/companies/1.html'
basic_url = 'http://www.bfb56.com'

headers = {'Refere':'http://www.bfb56.com/jifen.html',
           'User-Agent': ''.join(['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)',
                                  ' AppleWebKit/537.36 (KHTML, like Gecko) ',
                                  'Chrome/76.0.3809.132 Safari/537.36'])}

# //*[@id="mainbody"]/div/article/dl[2]/dt/a
#//*[@id="mainbody"]/div/article/dl[2]/dt

response = requests.get(start_url, headers=headers)
web = response.text
html = etree.HTML(web)
info = '//*[@id="mainbody"]/div/article/dl[2]/dt/a[last()]/{}'
title = html.xpath(info.format('text()'))
href = html.xpath(info.format('@href'))

print(title)
print(href)

address = html.xpath('//*[@id="mainbody"]/div/article/dl[2]/dd[2]/p/text()')
address = [add.replace('所在地：','') for add in address]
qualify = html.xpath('//*[@id="mainbody"]/div/article/dl[2]/dd[1]/p[2]/text()')
qualify = [qlfy.replace('行业资质：','') for qlfy in qualify]

print(address)
print(qualify)

#合并
def savedata(infotext):
    with open('bfb56.csv', 'a', encoding='utf-8') as f:
        f.write(infotext)
    f.close()


for name, link, add, qlfy in zip(title, href, address, qualify):
    infotext = ','.join([name, link, add, qlfy]) + '\n'
    savedata(infotext)


# //*[@id="mainbody"]/div/article/dl[1]
# //*[@id="mainbody"]/div/article/dl[2]
# //*[@id="mainbody"]/div/article/dl[10]

def parse_nextpage(html):
    nextpage_url = html.xpath('//*[@id="mainbody"]/div/article/div[2]/a[8]/@href')
    if not nextpage_url:
        return None
    else:
        newpage = '{}{}'.format(basic_url, nextpage_url[0])
        return newpage