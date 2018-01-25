# coding=utf-8

import re
import json
from bs4 import BeautifulSoup as bs

def response(flow):
    path = flow.request.path
    if path.startswith('/mp/profile_ext?action=getmsg'):
        '''文章列表数据'''
        content = flow.response.text
        data = json.loads(content)
        for msg in data['general_msg_list']['list']:
            if 'common_msg_info' in msg:
                id = msg['common_msg_info']['id']
                datetime = msg['common_msg_info']['datetime']
                fakeid = msg['common_msg_info']['fakeid']
                type = msg['common_msg_info']['type']
                status = msg['common_msg_info']['status']
                content = msg['common_msg_info']['content']
            if 'app_msg_ext_info' in msg:
                title = msg['app_msg_ext_info']['title']
                digest = msg['app_msg_ext_info']['digest']
                content = msg['app_msg_ext_info']['content']
                fileid = msg['app_msg_ext_info']['fileid']
                content_url = msg['app_msg_ext_info']['content_url']
                source_url = msg['app_msg_ext_info']['source_url']
                cover = msg['app_msg_ext_info']['cover']
                subtype = msg['app_msg_ext_info']['subtype']
                is_multi = msg['app_msg_ext_info']['is_multi']
                author = msg['app_msg_ext_info']['author']
                copyright_stat = msg['app_msg_ext_info']['copyright_stat']
                del_flag = msg['app_msg_ext_info']['del_flag']
                if is_multi == 1:
                    title = msg['app_msg_ext_info']['multi_app_msg_item_list']['title']
                    digest = msg['app_msg_ext_info']['multi_app_msg_item_list']['digest']
                    content = msg['app_msg_ext_info']['multi_app_msg_item_list']['content']
                    fileid = msg['app_msg_ext_info']['multi_app_msg_item_list']['fileid']
                    content_url = msg['app_msg_ext_info']['multi_app_msg_item_list']['content_url']
                    source_url = msg['app_msg_ext_info']['multi_app_msg_item_list']['source_url']
                    cover = msg['app_msg_ext_info']['multi_app_msg_item_list']['cover']
                    author = msg['app_msg_ext_info']['multi_app_msg_item_list']['author']
                    copyright_stat = msg['app_msg_ext_info']['multi_app_msg_item_list']['copyright_stat']
                    del_flag = msg['app_msg_ext_info']['multi_app_msg_item_list']['del_flag']
    elif path.startswith('/mp/appmsg_comment?action=getcomment'):
        '''评论数据'''
        content = flow.response.text
        data = json.loads(content)
        for item in data['elected_comment']:
            content = data['elected_comment']['content']
            content_id = data['elected_comment']['content_id']
            logo_url = data['elected_comment']['logo_url']
            nick_name = data['elected_comment']['nick_name']
    elif path.startswith('/s?__biz='):
        ''''文章正文数据'''
        soup = bs(flow.response.text, 'html.parser')
        content = soup.find('div', class_='rich_media_content')
    elif path.startswith('/getappmsgext?__biz='):
        '''阅读点赞等数据'''
        content = flow.response.text
        data = json.loads(content)
        read_num = data['appmsgstat']['read_num']
        like_num = data['appmsgstat']['like_num']
