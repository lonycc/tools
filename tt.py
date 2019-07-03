# coding=utf-8
from requests import Session
from time import time
from hashlib import md5

s = Session()

def toutiao():
    pc = 'https://www.toutiao.com/c/user/50502347096/#mid=50502347096'
    h5 = 'http://m.toutiao.com/profile/50502347096/#mid=50502347096'
    # pc版要解密_signature参数, 这个有一定复杂度; h5版只需解密as和cp参数
    pc_api = 'https://www.toutiao.com/c/user/article/?page_type=1&user_id=50502347096&max_behot_time=0&count=20&as=&cp=&_signature='
    as_, cp_ = tt_encrypt()
    h5_data = {
        'page_type': '1',
        'max_behot_time': '',
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
        'Referer': 'http://m.toutiao.com/profile/50502347096/',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)'
    }
    h5_api = 'https://www.toutiao.com/pgc/ma/'
    r = s.get(h5_api, headers=headers, params=h5_data)
    print(r.url)
    print(r.text)

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
