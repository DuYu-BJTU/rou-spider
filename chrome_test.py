from selenium import webdriver
from lxml import etree
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

start_url = 'http://www.bfb56.com/companies/1.html'
browser = webdriver.Chrome()
browser.get(start_url)
wait = WebDriverWait(browser, 10)


def crawl(browser):
    web = browser.page_source
    html = etree.HTML(web)
    info = '//*[@id="mainbody"]/div/article/dl[2]/dt/a[last()]/{}'
    companies = html.xpath(info.format('text()'))
    href = html.xpath(info.format('@href'))
    address = html.xpath('//*[@id="mainbody"]/div/article/dl[2]/dd[2]/p/text()')
    address = [add.replace('所在地：', '') for add in address]
    qualify = html.xpath('//*[@id="mainbody"]/div/article/dl[2]/dd[1]/p[2]/text()')
    qualify = [qlfy.replace('行业资质：', '') for qlfy in qualify]

    for name, link, add, qlfy in zip(companies, href, address, qualify):
        infotext = ','.join([name, link, add, qlfy]) + '\n'
        print(infotext)
        savedata(infotext)


def savedata(infotext):
    with open('bfb56.csv', 'a', encoding='utf-8') as f:
        f.write(infotext)
    f.close()


def next_page(page):
    submit = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR,
         '#mainbody > div > article > div.pagination > a.next_page')))
    submit.click()
    return page + 1


if __name__ == '__main__':
    page = 0
    for _ in range(3):
        crawl(browser)
        time.sleep(3)
        page = next_page(page)
        print(f'第{page}页')
    browser.close()
