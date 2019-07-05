# coding=utf-8
from requests import Session
from time import time
from hashlib import md5
import json

session = Session()

def toutiao(referer='http://m.toutiao.com/profile/50502347096/', max_behot_time=''):
    pc = 'https://www.toutiao.com/c/user/50502347096/#mid=50502347096'
    # pc版要解密_signature参数, 这个有一定复杂度; h5版只需解密as和cp参数
    pc_api = 'https://www.toutiao.com/c/user/article/?page_type=1&user_id=50502347096&max_behot_time=0&count=20&as=&cp=&_signature='
    as_, cp_ = tt_encrypt()
    data = {
        'page_type': '1',
        'max_behot_time': max_behot_time,
        'uid': '50502347096',
        'media_id': '50502347096',
        'output': 'json',
        'is_json': '1',
        'count': 10,
        'from': 'user_profile_app',
        'version': '2',
        'as': as_,
        'cp': cp_,
        'callback': 'jsonp4'
    }
    headers = {
        'Referer': referer,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    h5_api = 'https://www.toutiao.com/pgc/ma/'
    r = session.get(h5_api, headers=headers, params=h5_data)
    j = json.loads(r.text)
    print(j['data'])
    if j['has_more'] == 1:
        toutiao(referer, j['next']['max_behot_time'])

def tt_encrypt():
    now = int(time())
    now_16 = hex(now).upper()[2:]
    now_16_md5 = md5(str(now).encode('utf-8')).hexdigest().upper()
    if len(now_16) == 8:
        s = now_16_md5[0:5]
        o = now_16_md5[-5:]
        n = ""
        l = ""
        for i in range(5):
            n += s[i] + now_16[i]
            l += now_16[i+3] + o[i]
        as_ = "A1" + n + now_16[-3:]
        cp_ = now_16[0:3] + l + "E1"
    else:
        as_ = "479BB4B7254C150"
        cp_ = "7E0AC8874BB0985"
    return as_, cp_
