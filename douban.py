import requests
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import cv2
import numpy as np

headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Origin': 'https://accounts.douban.com',
    'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
}
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}

def shuru():
    s1 = input('账号:')
    s2 = input('密码:')
    return s1, s2
def denglu(s1,s2):
    session = requests.session()
    url_login = 'https://accounts.douban.com/j/mobile/login/basic'
    data_login = {
        'ck': '',
        'remember': 'true',
        'name': s1,
        'password': s2,
    }
    response1 = session.post(url_login, headers=headers1, data=data_login)
    print(response1.json()['description'])
    if response1.json()['description'] == '需要图形验证码':
        huadong()
        denglu(s1, s2)
        exit(0)
    if response1.json()['description'] == '用户名或密码错误':
        s1, s2 = shuru()
        denglu(s1, s2)
        exit(0)
    response2 = session.get('https://www.douban.com/', headers=headers2)
    ck = response2.cookies['ck']
    print('登录成功')
    data_comment = {
        'ck': ck,
        'comment': input('请输入评论:'),
        'privacy_and_reply_limit': 'P,',
    }
    url_comment = 'https://www.douban.com/'
    response3 = session.post(url_comment, headers=headers2, data=data_comment)
    if response3.status_code == 200:
        print('发表成功')
    else:
        print('发表失败')
def shibie(driver):
    image1 = driver.find_element_by_xpath('//*[@id="slideBg"]').get_attribute('src')
    image2 = driver.find_element_by_xpath('//*[@id="slideBlock"]').get_attribute('src')
    r1 = urllib.request.Request(image1)
    r1g = open('r1.png', 'wb+')
    r1g.write(urllib.request.urlopen(r1).read())
    r1g.close()
    r2 = urllib.request.Request(image2)
    r2g = open('r2.png', 'wb+')
    r2g.write(urllib.request.urlopen(r2).read())
    r2g.close()
    cv2.imwrite('r3.jpg', cv2.imread('r1.png', 0))
    cv2.imwrite('r4.jpg', cv2.imread('r2.png', 0))
    cv2.imwrite('r4.jpg', abs(255 - cv2.cvtColor(cv2.imread('r4.jpg'), cv2.COLOR_BGR2GRAY)))
    result = cv2.matchTemplate(cv2.imread('r4.jpg'), cv2.imread('r3.jpg'), cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)
    cv2.rectangle(cv2.imread('r3.jpg'), (y+20, x+20), (y + 136-25, x + 136-25), (7, 249, 151), 2)
    print('识别坐标为:', y+20)
    if y + 20 < 450: #如果缺口位置坐标小于450，刷新验证码重新计算缺口位置
        shuaxin = driver.find_element_by_xpath('//*[@id="reload"]/div')
        shuaxin.click()
        time.sleep(1)
        y = shibie()
    return y
def huadong():
    print('登录失败，正在模拟滑块验证')
    driver = webdriver.Chrome()
    driver.get('https://www.douban.com/')
    driver.implicitly_wait(10)
    iframe1 = driver.find_element_by_xpath('//*[@id="anony-reg-new"]/div/div[1]/iframe')
    driver.switch_to.frame(iframe1)  # 先进子页面iframe
    t1 = driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
    t1.click()
    time.sleep(1)
    t2 = driver.find_element_by_xpath('//*[@id="username"]')
    t2.send_keys(s1)
    t3 = driver.find_element_by_xpath('//*[@id="password"]')
    t3.send_keys(s2)
    time.sleep(1)
    t4 = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]/a')
    t4.click()
    time.sleep(2)
    iframe2 = driver.find_element_by_id('tcaptcha_iframe')  # 定位到滑块验证码的iframe
    driver.switch_to.frame(iframe2)  # 切换到iframe
    xx = shibie(driver)
    x = int((xx - 70 + 20) / 2.41)  # 滑块的固定坐标为70，2.41是原图在网页上缩小为2.41倍
    tracks = [x + 30, -43, 8]
    huakuai = driver.find_element_by_id('tcaptcha_drag_thumb')
    ActionChains(driver).click_and_hold(on_element=huakuai).perform()
    for track in tracks:
        ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(driver).release(on_element=huakuai).perform()
    time.sleep(2)
    driver.close()

s1,s2 = shuru()
denglu(s1, s2)