from pyquery import PyQuery as pq
from selenium import webdriver
from lxml import etree

browser = webdriver.Chrome()
start_url = 'http://www.bfb56.com/companies/1.html'
browser.get(start_url)


# web = browser.page_source
# html = etree.HTML(web)
# doc = pq(html)
#
# company = doc('#mainbody > div > article > dl:nth-child(2) > dt > a').text()
#
# companies = doc('dl.transport-list.clearfix').items()
# for c in companies:
#     print(c('dt>a').text())
#     print(c('dt>a:last-child').attr('href'))
#     print('html:', c('dt>a').html())
#
# url = doc('dl:nth-child(8) > dt > a').attr('href')
# company = doc('dl:nth-child(8) > dt > a').text()
# company_html = doc('dl:nth-child(8) > dt > a').html()

def savedata(infotext):
    with open('bfb56_another.csv', 'a', encoding='utf-8') as f:
        f.write(infotext)
    f.close()


def crawl_pyquery(browser):
    web = browser.page_source
    html = etree.HTML(web)
    doc = pq(html)
    companies = doc('dl.transport-list.clearfix').items()
    for c in companies:
        company = c('dt > a').text()
        url = c('dt>a:last-child').attr('href')
        address = c('dd.transport-item2>p').text()
        qualification = c('dd.transport-item>p.trans-link.trans-linkg').text()
        savedata(f'{company},{url},{address},{qualification}\n')


crawl_pyquery(browser)
