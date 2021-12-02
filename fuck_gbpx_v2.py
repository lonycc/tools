from selenium import webdriver
import time
from tqdm import tqdm
from hashlib import md5
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


class GbpxAuto(object):
    def __init__(self):
        self.driver_path = '/Users/work/Downloads/chromedriver'
        self.login_url = 'https://gbpx.gd.gov.cn/gdceportal/index.aspx'
        self.study_center_url = 'https://gbpx.gd.gov.cn/gdceportal/Study/LearningCourse.aspx?mid=' + md5(str(time.time()).encode('utf-8')).hexdigest()
        self.username = ''
        self.password = ''
        self.current_page = 1

    def login(self):
        """登陆网站"""
        print('开始登陆')
        self.browser.get(self.login_url)
        self.browser.maximize_window()
        self.browser.find_element(By.ID, 'txtLoginName').send_keys(self.username)
        self.browser.find_element(By.ID, 'txtPassword').send_keys(self.password)
        while True:
            try:
                self.browser.find_element(By.ID, 'txtLoginName')
                print('请自行填入用户名密码和验证码并提交登录')
                time.sleep(2)
            except:
                print('登录成功')
                break

    def watch_videos(self):
        """观看视频"""
        videos = self.browser.find_elements(By.XPATH, '//a[@class="courseware-list-reed"]')
        for i, video in enumerate(videos):
            if '100.0％' in video.get_attribute('title'):
                continue
            video.click()
            all_windows = self.browser.window_handles
            self.browser.switch_to.window(all_windows[-1])
            # 缓冲5秒，打开视频页
            time.sleep(5)
            self.browser.switch_to.frame('course_frame')
            title = self.browser.find_element(By.TAG_NAME, 'h3').get_attribute('innerText')
            # 缓冲5秒，加载视频框架
            time.sleep(5)
            # 点击播放
            self.browser.find_element(By.TAG_NAME, 'button').click()
            # 缓冲5秒，等视频加载出来
            time.sleep(5)
            # 获取视频时长
            video_duration_str = self.browser.find_element(By.XPATH, '//span[@class="vjs-remaining-time-display"]').get_attribute('innerText')
            arr = video_duration_str.split(':')
            video_remaining_seconds = int(arr[0]) * 60 + int(arr[1]) if len(arr) == 2 else int(arr[0]) * 3600 + int(arr[1]) * 60 + int(arr[2])

            print(f'{i}. {title}')
            # 静音播放
            self.browser.find_element().click()
            # 执行3倍速播放
            #self.browser.execute_script("document.querySelector('video').playbackRate = 3.0;")
            for i in tqdm(range(0, video_remaining_seconds+3, 3)):
                time.sleep(1)
            self.browser.switch_to.parent_frame()
            self.browser.close()
            self.browser.switch_to.window(all_windows[0])
        print(f'恭喜你，第 {self.current_page} 页完成了')
        self.current_page += 1

    def start(self):
        """启动入口"""
        self.browser = webdriver.Chrome(service=Service(self.driver_path), options=webdriver.ChromeOptions())
        # 登录，自动填充账号密码和验证码
        self.login()
        # 登录成功，访问学习中心
        self.browser.get(self.study_center_url)
        # 观看视频
        self.watch_videos()
        # 是否有下一页
        next_page_btn = self.browser.find_element(By.ID, 'btnNextPage')
        while next_page_btn.get_attribute('disabled') is None:
            # 点进下一页
            next_page_btn.click()
            self.watch_videos()
            next_page_btn = self.browser.find_element(By.ID, 'btnNextPage')

        print('终于搞完了，可喜可贺')
        # 全部完成后可推出浏览器
        self.browser.quit()


if __name__ == '__main__':
    print('启动')
    gbpx = GbpxAuto()
    gbpx.start()
