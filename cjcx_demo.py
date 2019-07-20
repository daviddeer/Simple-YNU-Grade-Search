from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys #向浏览器发送请求
import requests
import json
from selenium.webdriver.chrome.options import Options

class Cjspider():
    # 驱动浏览器的函数
    def open_browser(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.implicitly_wait(10)
        self.wait = WebDriverWait(self.browser, 20)  # 最长等待时间10so

    def open_login_index(self):
        self.open_browser()
        self.browser.get("http://ehall.ynu.edu.cn/new/index.html")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="ampHasNoLogin"]'))).click()

    def input_user(self):
        self.username=input("Please input the account name: ")
        self.password = input("Please input the account password: ")

    def enter_user_index(self):
        input_username = self.browser.find_element_by_id("username")  # 通过id定位搜索栏位置
        input_username.send_keys(self.username)
        input_username.send_keys(Keys.ENTER)  # 点击搜索确认按钮
        input_password = self.browser.find_element_by_id("password")  # 通过id定位搜索栏位置
        input_password.send_keys(self.password)
        input_password.send_keys(Keys.ENTER)  # 点击搜索确认按钮
        wait = WebDriverWait(self.browser, 10)  # 延时等待

    def enter_cjcx_page(self):
        handles1 = self.browser.window_handles
        self.wait.until(EC.element_to_be_clickable((By.XPATH,'//span[@id="ampHeaderSearchResult"]'))).click()
        kw = self.browser.find_element_by_id("ampServiceSearchInput")  # 通过id定位搜索栏位置
        kw.send_keys("成绩查询")
        kw.send_keys(Keys.ENTER)
        wait = WebDriverWait(self.browser, 10)  # 延时等待
        self.wait.until(EC.element_to_be_clickable((By.XPATH,'//div[@class="amp-hover-app-card-group amp-pull-left amp-service-center-app-group"]'))).click()
        handles2 = self.browser.window_handles
        if handles1==handles2:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="ampDetailEnter"]'))).click()
        time.sleep(1)
        #切换窗口
        handles=self.browser.window_handles
        self.browser.switch_to.window(handles[-1])

    def get_cj(self):
        # 获取cookie列表
        cookie_list = self.browser.get_cookies()
        cookievalue=""
        for ck in cookie_list:
            cookievalue=cookievalue+ck["name"]+"="+ck["value"]+";"
        cookievalue=cookievalue[:-1]
        self.headers={"Cookie":cookievalue,
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
                      }
        res=requests.get(url="http://ehall.ynu.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do",headers=self.headers)
        res.encoding="utf-8"
        html=res.text
        #转换成json数据
        data=json.loads(html)
        cjs=data["datas"]["xscjcx"]["rows"]
        for cj in cjs:
            print(cj["KCM"]+": "+str(cj["ZCJ"]))

    def work_on(self):
        self.open_browser()
        self.open_login_index()
        self.input_user()
        self.enter_user_index()
        self.enter_cjcx_page()
        self.get_cj()
        #关闭窗口
        handles=self.browser.window_handles
        for handle in handles:
            self.browser.switch_to.window(handle)
            self.browser.close()

cjspider=Cjspider()
cjspider.work_on()