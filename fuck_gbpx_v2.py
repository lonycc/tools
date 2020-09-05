# coding=utf-8

from selenium import webdriver
import time
from tqdm import tqdm
from hashlib import md5


class GbpxAuto(object):
    def __init__(self):
        self.driver_path = '/Users/work/Downloads/chromedriver'
        self.login_url = 'https://gbpx.gd.gov.cn/gdceportal/index.aspx'
        self.study_center_url = 'https://gbpx.gd.gov.cn/gdceportal/Study/LearningCourse.aspx?mid=' + md5(str(time.time()).encode('utf-8')).hexdigest()
        self.username = 'your username'
        self.password = 'your password'
        self.current_page = 1

    def login(self):
        """登陆网站"""
        print('开始登陆')
        self.browser.get(self.login_url)
        self.browser.maximize_window()
        self.browser.find_element_by_id('txtLoginName').send_keys(self.username)
        self.browser.find_element_by_id('txtPassword').send_keys(self.password)
        while True:
            try:
                self.browser.find_element_by_id('txtLoginName')
                print('请自行填入验证码并登录')
                time.sleep(2)
            except:
                print('登录成功')
                break

    def watch_videos(self):
        """观看视频"""
        videos = self.browser.find_elements_by_xpath('//a[@class="courseware-list-reed"]')
        for i, video in enumerate(videos):
            if '100.0％' in video.get_attribute('title'):
                continue
            video.click()
            all_windows = self.browser.window_handles
            self.browser.switch_to.window(all_windows[-1])
            # 缓冲5秒，打开视频页
            time.sleep(5)
            self.browser.switch_to.frame('course_frame')
            title = self.browser.find_element_by_tag_name('h3').get_attribute('innerText')
            # 缓冲5秒，加载视频框架
            time.sleep(5)
            # 点击播放
            self.browser.find_element_by_tag_name('button').click()
            # 缓冲5秒，等视频加载出来
            time.sleep(5)
            # 获取视频时长
            video_duration_str = self.browser.find_element_by_xpath('//span[@class="vjs-remaining-time-display"]').get_attribute('innerText')
            arr = video_duration_str.split(':')
            video_remaining_seconds = int(arr[0]) * 60 + int(arr[1]) if len(arr) == 2 else int(arr[0]) * 3600 + int(arr[1]) * 60 + int(arr[2])

            print(f'{i}. {title}')
            for i in tqdm(range(video_remaining_seconds+3)):
                time.sleep(1)
            self.browser.switch_to.parent_frame()
            self.browser.close()
            self.browser.switch_to.window(all_windows[0])
        print(f'恭喜你，第 {self.current_page} 页完成了')
        self.current_page += 1

    def start(self):
        """启动入口"""
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(self.driver_path, options=options)
        # 登录，自动填充账号密码和验证码
        self.login()
        # 登录成功，访问学习中心
        self.browser.get(self.study_center_url)
        # 观看视频
        self.watch_videos()
        # 是否有下一页
        next_page_btn = self.browser.find_element_by_id('btnNextPage')
        while next_page_btn.get_attribute('disabled') is None:
            # 点进下一页
            next_page_btn.click()
            self.watch_videos()
            next_page_btn = self.browser.find_element_by_id('btnNextPage')

        print('终于搞完了，可喜可贺')
        # 全部完成后可推出浏览器
        self.browser.quit()


if __name__ == '__main__':
    print('启动')
    gbpx = GbpxAuto()
    gbpx.start()
