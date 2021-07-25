import random
import copy

import os
from io import StringIO

from requests.exceptions import ReadTimeout
import requests

import pandas as pd
import numpy as np


import warnings
from tqdm import tqdm # 進度條
from tqdm import tnrange, tqdm_notebook

import urllib.request
import zipfile # 解壓縮 # zipfile.Zipfile
import shutil # 目錄操作
import time
import datetime

# 爬蟲專用隨機環境
def generate_random_header():
    random_user_agents = {'chrome': ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
      'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
      'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
      'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36',
      'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
      'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F',
      'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
      'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
      'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
      'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36',
      'Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
      'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
      'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
      'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14'],
     'opera': ['Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
      'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
      'Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14',
      'Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02',
      'Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00',
      'Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00',
      'Opera/12.0(Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00',
      'Opera/12.0(Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00',
      'Mozilla/5.0 (Windows NT 5.1) Gecko/20100101 Firefox/14.0 Opera/12.0',
      'Opera/9.80 (Windows NT 6.1; WOW64; U; pt) Presto/2.10.229 Version/11.62',
      'Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.10.229 Version/11.62',
      'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52',
      'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52',
      'Opera/9.80 (Windows NT 5.1; U; en) Presto/2.9.168 Version/11.51',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; de) Opera 11.51',
      'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50',
      'Opera/9.80 (X11; Linux i686; U; hu) Presto/2.9.168 Version/11.50',
      'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11',
      'Opera/9.80 (X11; Linux i686; U; es-ES) Presto/2.8.131 Version/11.11',
      'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/5.0 Opera 11.11',
      'Opera/9.80 (X11; Linux x86_64; U; bg) Presto/2.8.131 Version/11.10',
      'Opera/9.80 (Windows NT 6.0; U; en) Presto/2.8.99 Version/11.10',
      'Opera/9.80 (Windows NT 5.1; U; zh-tw) Presto/2.8.131 Version/11.10',
      'Opera/9.80 (Windows NT 6.1; Opera Tablet/15165; U; en) Presto/2.8.149 Version/11.1',
      'Opera/9.80 (X11; Linux x86_64; U; Ubuntu/10.10 (maverick); pl) Presto/2.7.62 Version/11.01',
      'Opera/9.80 (X11; Linux i686; U; ja) Presto/2.7.62 Version/11.01',
      'Opera/9.80 (X11; Linux i686; U; fr) Presto/2.7.62 Version/11.01',
      'Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.7.62 Version/11.01',
      'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.7.62 Version/11.01',
      'Opera/9.80 (Windows NT 6.1; U; sv) Presto/2.7.62 Version/11.01',
      'Opera/9.80 (Windows NT 6.1; U; en-US) Presto/2.7.62 Version/11.01',
      'Opera/9.80 (Windows NT 6.1; U; cs) Presto/2.7.62 Version/11.01',
      'Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.7.62 Version/11.01',
      'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.7.62 Version/11.01',
      'Opera/9.80 (Windows NT 5.1; U;) Presto/2.7.62 Version/11.01',
      'Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.7.62 Version/11.01',
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.13) Gecko/20101213 Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.7.62 Version/11.01',
      'Mozilla/5.0 (Windows NT 6.1; U; nl; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01',
      'Mozilla/5.0 (Windows NT 6.1; U; de; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01',
      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; de) Opera 11.01',
      'Opera/9.80 (X11; Linux x86_64; U; pl) Presto/2.7.62 Version/11.00',
      'Opera/9.80 (X11; Linux i686; U; it) Presto/2.7.62 Version/11.00',
      'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.6.37 Version/11.00',
      'Opera/9.80 (Windows NT 6.1; U; pl) Presto/2.7.62 Version/11.00',
      'Opera/9.80 (Windows NT 6.1; U; ko) Presto/2.7.62 Version/11.00',
      'Opera/9.80 (Windows NT 6.1; U; fi) Presto/2.7.62 Version/11.00',
      'Opera/9.80 (Windows NT 6.1; U; en-GB) Presto/2.7.62 Version/11.00',
      'Opera/9.80 (Windows NT 6.1 x64; U; en) Presto/2.7.62 Version/11.00',
      'Opera/9.80 (Windows NT 6.0; U; en) Presto/2.7.39 Version/11.00'],
     'firefox': ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
      'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
      'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0',
      'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0',
      'Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0',
      'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0',
      'Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3',
      'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:27.0) Gecko/20121011 Firefox/27.0',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0',
      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
      'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0',
      'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0',
      'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0',
      'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0',
      'Mozilla/5.0 (Microsoft Windows NT 6.2.9200.0); rv:22.0) Gecko/20130405 Firefox/22.0',
      'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1',
      'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:21.0.0) Gecko/20121011 Firefox/21.0.0',
      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',
      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0',
      'Mozilla/5.0 (X11; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0',
      'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20130514 Firefox/21.0',
      'Mozilla/5.0 (Windows NT 6.2; rv:21.0) Gecko/20130326 Firefox/21.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130330 Firefox/21.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
      'Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130401 Firefox/21.0',
      'Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0',
      'Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0',
      'Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21.0',
      'Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130331 Firefox/21.0',
      'Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20100101 Firefox/21.0',
      'Mozilla/5.0 (Windows NT 5.0; rv:21.0) Gecko/20100101 Firefox/21.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
      'Mozilla/5.0 (Windows NT 6.2; Win64; x64;) Gecko/20100101 Firefox/20.0',
      'Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0',
      'Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/19.0',
      'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/18.0.1',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0)  Gecko/20100101 Firefox/18.0',
      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6'],
     'internetexplorer': ['Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
      'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0;  rv:11.0) like Gecko',
      'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)',
      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',
      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)',
      'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
      'Mozilla/4.0 (Compatible; MSIE 8.0; Windows NT 5.2; Trident/6.0)',
      'Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',
      'Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)',
      'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))',
      'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; InfoPath.3; MS-RTC LM 8; .NET4.0C; .NET4.0E)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; chromeframe/12.0.742.112)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; Tablet PC 2.0; InfoPath.3; .NET4.0C; .NET4.0E)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; yie8)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET CLR 1.1.4322; .NET4.0C; Tablet PC 2.0)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; FunWebProducts)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/13.0.782.215)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/11.0.696.57)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.1; SV1; .NET CLR 2.8.52393; WOW64; en-US)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; chromeframe/11.0.696.57)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/4.0; GTB7.4; InfoPath.3; SV1; .NET CLR 3.1.76908; WOW64; en-US)',
      'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)',
      'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
      'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; InfoPath.1; SV1; .NET CLR 3.8.36217; WOW64; en-US)',
      'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; .NET CLR 2.7.58687; SLCC2; Media Center PC 5.0; Zune 3.4; Tablet PC 3.6; InfoPath.3)',
      'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; Media Center PC 4.0; SLCC1; .NET CLR 3.0.04320)',
      'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322)',
      'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727)',
      'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
      'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; SLCC1; .NET CLR 1.1.4322)',
      'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.0; Trident/4.0; InfoPath.1; SV1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 3.0.04506.30)',
      'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.0; Trident/4.0; FBSMTWB; .NET CLR 2.0.34861; .NET CLR 3.0.3746.3218; .NET CLR 3.5.33652; msn OptimizedIE8;ENUS)',
      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)',
      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8',
      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; Media Center PC 6.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C)',
      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.3; .NET4.0C; .NET4.0E; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MS-RTC LM 8)',
      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 3.0)'],
     'safari': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
      'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
      'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; ko-KR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; fr-FR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; cs-CZ) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; sv-se) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; ko-kr) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; it-it) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; fr-fr) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; es-es) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-gb) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; de-de) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; sv-SE) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Windows; U; Windows NT 6.0; hu-HU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Windows; U; Windows NT 6.0; de-DE) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Windows; U; Windows NT 5.1; it-IT) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-us) AppleWebKit/534.16+ (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; fr-ch) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; de-de) AppleWebKit/534.15+ (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; ar) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Android 2.2; Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-HK) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
      'Mozilla/5.0 (Windows; U; Windows NT 6.0; tr-TR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
      'Mozilla/5.0 (Windows; U; Windows NT 6.0; nb-NO) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
      'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
      'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-TW) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
      'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-cn) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5']}
    random_headers = [
    {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36 OPR/56.0.3051.104'},
    {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36 OPR/54.0.2952.64'},
    {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0.2) Gecko/20100101 Firefox/58.0.2'},
    {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36 OPR/56.0.3051.104'},
    {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36 OPR/57.0.3098.116'},
    {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'},
    {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Safari/537.36'},
    {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'},
    {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'},
    {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1; rv:52.1.0) Gecko/20100101 Firefox/52.1.0'},
    ]
    # 先把抬頭讀取出來 "chrome" , "opera" ,"firefox".... 放入list中 將自典型態轉換 隨機選擇
    browser = random.choice(list(random_user_agents.keys()))
    # 隨機選擇一台電腦 透過browser
    user_agent = random.choice(random_user_agents[browser])
    # 透過copy 複製出來
    header = copy.copy(random.choice(random_headers))
    # 將隨機電腦放入 user-Agent
    header['User-Agent'] = user_agent
    
    return header


def find_best_session():

    for i in range(10):
        try:
            print('獲取新的Session 第', i, '回合')
            headers = generate_random_header()# 取得header 並且開始正式爬蟲
            ses = requests.Session()# session会保存会话，往下发送请求，直接使用session即可
            # 取得Response(200)
            ses.get('https://www.twse.com.tw/zh/', headers=headers, timeout=10)
            
            ses.headers.update(headers)
            print('成功！')
            return ses # 若成功就不會輸出錯誤訊息
        except (ConnectionError, ReadTimeout) as error:
            print(error)
            print('失敗，10秒後重試')
            time.sleep(10)
            
    print('您的網頁IP已經被證交所封鎖，請更新IP來獲取解鎖')
    print("　手機：開啟飛航模式，再關閉，即可獲得新的IP")
    print("數據機：關閉然後重新打開數據機的電源")

ses = None
# *未宣告之參數(12,11,33) ** 已宣告之參數(k1=1,k2=2)
def requests_post(*args1, **args2):
  
    # get current session
    global ses
    
    if ses == None:
        ses = find_best_session()# 取得保存好的header
    
    # download data 總測試次數三次
    i = 3
    while i >= 0:
        try:
            # 每次爬蟲間隔10秒 因為前面已經宣告 所以可以直接拿來使用
            return ses.post(*args1, timeout=10, **args2)
            
        # 若錯誤輸出錯誤字樣
        except (ConnectionError, ReadTimeout) as error:
            print(error)
            print('retry one more time after 60s', i, 'times left')
            time.sleep(60)
            ses = find_best_session()
            
        i -= 1
    # 若無成功傳回空值
    return pd.DataFrame()

ses = None
def requests_get(*args1, **args2):
  
    # get current session
    global ses
    if ses == None:
        ses = find_best_session()# 取得保存好的header
        
    # download data 總測試次數三次
    i = 3
    while i >= 0:
        try:
            # 每次爬蟲間隔10秒 因為前面已經宣告 所以可以直接拿來使用 args2已宣告參數會被放置在後面
            return ses.get(*args1, timeout=10, **args2)
        # 若錯誤輸出錯誤字樣
        except (ConnectionError, ReadTimeout) as error:
            print(error)
            print('retry one more time after 60s', i, 'times left')
            time.sleep(60)
            ses = find_best_session()
            
        i -= 1
    # 若無成功傳回空值
    return pd.DataFrame()
# 股價爬蟲
def crawl_price(date):
    # 將時間轉換成字串
    datestr = date.strftime('%Y%m%d')
    
    try:
        # 證卷交易所網址
        # lwo
        r = requests_post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALLBUT0999')
        # 嘗試有錯誤
    except Exception as e:
        # 今天爬取不到資料
        print('**WARRN: cannot get stock price at', datestr)
        print(e)
        return None
    # 將多餘的等號刪除
    content = r.text.replace('=', '')

    # 將所有資料 串再一起
    lines = content.split('\n')
    # 將資料清洗 剩餘股價資料
    lines = list(filter(lambda l:len(l.split('",')) > 10, lines))
    # 透過換行符號重新合成
    content = "\n".join(lines)
    
    # 若無抓到資料返回空值
    if content == '':
        return None
    
    # 放入檔案 轉成pd
    df = pd.read_csv(StringIO(content))
    # 所有資料轉成字串
    df = df.astype(str)
    # 將字串內的 ,號刪除 apply 使用函數
    df = df.apply(lambda s: s.str.replace(',', ''))
    # 將時間轉換成 pd.時間
    # 將放入的date 轉換並新增入 df
    df['date'] = pd.to_datetime(date)
    # 改變colunms 的名字
    df = df.rename(columns={'證券代號':'stock_id'})
    # 取代index
    df = df.set_index(['stock_id', 'date'])
    # 將所有字串變成 數字(index 和 columns不受影響) pd.to_numeric 只能用在 Series 可以透過apply(放入函數)
    df = df.apply(lambda s:pd.to_numeric(s, errors='coerce'))
    # 將Unnamed:拋棄 
    # 保留非整行 colunms 皆為空值 的 columns
    df = df[df.columns[df.isnull().all() == False]]
    # 保留 row 非0 的值
    df = df[~df['收盤價'].isnull()]

    
    return df


warnings.simplefilter(action='ignore', category=FutureWarning)


# 讀取月營收


def crawl_monthly_report(date):
    # https://mops.twse.com.tw/nas/t21/sii/t21sc03_108_7.html
    # 由於網頁為民國年分 需減去1911
    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(date.year - 1911)+'_'+str(date.month)+'.html'
    
    
    # 偽瀏覽器 
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    # 下載該年月的網站
    try:
        # 使用函數 requests.get
        # 請注意，當verify設置為 時False，請求將接受服務器提供的任何 TLS 證書，並將忽略主機名不匹配和/或過期的證書，
        # 這將使您的應用程序容易受到中間人 (MitM) 攻擊。將 verify 設置為False在本地開發或測試期間可能很有用。
        
        # r = requests_get(url, headers=headers, verify=False)
        r = requests_get(url, verify=False)
        r.encoding = 'big5'
        
        
    except:
        print('**WARRN: requests cannot get html')
        return None
    
    import lxml
    
    try:
        # 使用try 避免爬取不到報錯
        # 用pandas轉換成 dataframe
        html_df = pd.read_html(StringIO(r.text))
#         print(html_df)
    except:
        print('**WARRN: Pandas cannot find any table in the HTML file')
        return None
    
    # 處理一下資料
    if html_df[0].shape[0] > 500:
        df = html_df[0].copy()
    else:
        # 將 df的shape[1,"2"] 取編號1元素 <小於11 和大於5 取值可以參考原網站資料架構
        # 再重新合併dataframe
        df = pd.concat([df for df in html_df if df.shape[1] <= 11 and df.shape[1] > 5])

    # 查詢物件屬性 只是為了 if else的動作
    if 'levels' in dir(df.columns):       
        # 取得colunms(1)置換原本colunms(0)
        df.columns = df.columns.get_level_values(1)
    else:
        # 防止後面錯亂的columns 
        df = df[list(range(10))]
        column_index = df.index[(df[0] == '公司代號')][0]
        df.columns = df.iloc[column_index]
    # 當月營收最重要 將其轉換成數字 若錯誤 coerce (errors='coerce') 將無法轉換字轉成NAN
    df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
    df = df[~df['當月營收'].isnull()]# ~非的意思保留非空直
    df = df[df['公司代號'] != '合計']# 刪除最下面兩行
    # 計算下個月
    next_month = datetime.date(date.year + int(date.month / 12), ((date.month % 12) + 1), 10)
    
    df['date'] = pd.to_datetime(next_month)

    df = df.rename(columns={'公司代號':'stock_id'})
    df = df.set_index(['stock_id', 'date'])
    
    # 公司名稱在這裡被丟掉
    df = df.apply(lambda s:pd.to_numeric(s, errors='coerce'))
    df = df[df.columns[df.isnull().all() == False]]
    
    return df



# 只能下載 還沒解析
# 財報下載
def crawl_finance_statement2019(year, season):
    # 單一文件下載網址
    # <input type="button" value="下載" onclick="window.open('/server-java/FileDownLoad?functionName=t164sb01&amp;step=9&amp;co_id=2330&amp;year=2021&amp;season=1&amp;report_id=C','new1');">
    # 整批文件下載
    # <input type="button" value="下載" onclick="window.open('/server-java/FileDownLoad?step=9&amp;fileName=tifrs-2021Q1.zip&amp;filePath=/home/html/nas/ifrs/2021/','new1');">
    # step 參數無調整
    def ifrs_url(year, season):
        url = "https://mops.twse.com.tw/server-java/FileDownLoad?step=9&fileName=tifrs-"+str(year)+"Q"+str(season)\
                +".zip&filePath=/home/html/nas/ifrs/"+str(year)+"/"
        # print(url)
        return url


    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    print('start download')
    
    # 繼承tqdm物件
    class DownloadProgressBar(tqdm):
        # 非 tqdm 裡面的 update_to
        # 回调函数   接收 relrieve傳出來之參數 # 已经下载的数据块  # 数据块的大小 # 远程文件的大小
        def update_to(self, b=1, bsize=1, tsize=None):
            # 有收到檔案時            
            if tsize is not None:
                # 取得檔案大小 若值為-1 網站為舊版
                self.total = tsize
            # print(b , bsize ,self.total)
            self.update(b * bsize - self.n)

    # https://pypi.org/project/tqdm/#documentation
    def download_url(url, output_path):
        #unit 字串 unit_scale 顯示小數點 #miniters=1官方建議網路不穩使用 desc 打印名稱顯示
        with DownloadProgressBar(unit='B', unit_scale=True,
                                 miniters=1, desc=url.split('/')[-1]) as t:
            # filename 檔案的名稱
            urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)
           


    url = ifrs_url(year,season)
    download_url(url, 'temp.zip')

    print('finish download')

    path = os.path.join('data', 'financial_statement', str(year) + str(season))
    # 如果存在路徑
    if os.path.isdir(path):
        # 如果檔案重複 刪除目錄 (financial下整個目錄(名稱相等))
        shutil.rmtree(path)
    
    print('create new dir')
    
    #  with ZipFile('temp.zip', 'rb')

    # 解壓縮
    zipfiles = zipfile.ZipFile(open('temp.zip', 'rb'))
    # 將存檔放置在指定目錄
    zipfiles.extractall(path=path)
          
    print('extract all files')
    
    # 將目錄中的檔案存成陣列 #'tifrs-fr1-m1-basi-cr-2801-2020Q1.html'
    fnames = [f for f in os.listdir(path) if f[-5:] == '.html']
    
    # 將目錄排序
    fnames = sorted(fnames)
    
    # 保存新的檔案名稱 先取得後整理
    newfnames = [f.split("-")[5] + '.html' for f in fnames]
    
    # 裝成tuple  一起處理資料 (num1 ,num2)
    for fold, fnew in zip(fnames, newfnames):
        
        if len(fnew) != 9:
            # 將不是資料內容移除 # 2801.html>>9
            print('remove strange code id', fnew)
            os.remove(os.path.join(path, fold))
            # 跳過本次
            continue
        # exists 如果存在 回傳true
        if not os.path.exists(os.path.join(path, fnew)):
            
            os.rename(os.path.join(path, fold), os.path.join(path, fnew))
        else:
            os.remove(os.path.join(path, fold))
            
            
            
def crawl_finance_statement_by_date(date):
    # 將資料轉換成季 財報晚三個月
    year = date.year
    if date.month == 3:
        season = 4
        year = year - 1
        month = 11
    elif date.month == 5:
        season = 1
        month = 2
    elif date.month == 8:
        season = 2
        month = 5
    elif date.month == 11:
        season = 3
        month = 8
    else:
        return None
    
    
    if year >= 2019:
        crawl_finance_statement2019(year, season)
    else:
        pass
        # df = crawl_monthly_report(datetime.datetime(year, month, 1))
        # crawl_finance_statement(year, season, df.index.levels[0])
#     html2db(date)
    return {}



# 讀取時間range
from datetime import date
from dateutil.rrule import rrule, DAILY, MONTHLY #rrule規則

def date_range(start_date, end_date):
    # 返回生成日期的 不需要時間 (每天)
    return [dt.date() for dt in rrule(DAILY, dtstart=start_date, until=end_date)]


def month_range(start_date, end_date):
    # date 若是12.31 會有bug 出現 # 待修正 其餘正常
    return [dt.date() for dt in rrule(MONTHLY, dtstart=start_date, until=end_date)]

    # 3 5 8 11 每季時間 (3 要year-1)
def season_range(start_date, end_date):
    # 回傳時間 判斷類別是否想同
    if isinstance(start_date, datetime.datetime):
        start_date = start_date.date()
        
    if isinstance(end_date, datetime.datetime):
        end_date = end_date.date()
    
    ret = []
    for year in range(start_date.year-1, end_date.year+1):
        # 將所有相關年份月日列出
        ret += [  datetime.date(year, 5, 15),
                datetime.date(year, 8, 14),
                datetime.date(year, 11, 14),
                datetime.date(year+1, 3, 31)]
    # 重新整理資料 保留時間內的資料
    ret = [r for r in ret if start_date < r < end_date]
    
    return ret

# 考慮以後應用 故選用dateitme.datetime()
# season_range(start_date=datetime.datetime(2018,8,10),end_date=datetime.datetime(2020,8,10))


# ========================================================================================================
def table_exist(conn, table):
    return list(conn.execute(
        # sqlite3 內建有一個系統資訊 sqlite_master 只允許讀取(使用者) 若有 [(1,)] 回傳格式
        "select count(*) from sqlite_master where type='table' and name='" + table + "'"))[0][0] == 1
    
# def table_latest_date(conn, table):
#     cursor = conn.execute('SELECT date FROM ' + table + ' ORDER BY date DESC LIMIT 1;')
#     return datetime.datetime.strptime(list(cursor)[0][0], '%Y-%m-%d %H:%M:%S') 

# def table_earliest_date(conn, table):
#     cursor = conn.execute('SELECT date FROM ' + table + ' ORDER BY date ASC LIMIT 1;')
#     return datetime.datetime.strptime(list(cursor)[0][0], '%Y-%m-%d %H:%M:%S') 
# conn 資料庫 name=table name df 爬取到的資料
def add_to_sql(conn, name, df):
    
    # 檢查是否存在
    exist = table_exist(conn, name)
    # 讀取sql ("seclet 句子" , 資料庫 ,設定index) 若不存在 回傳空值
    ret = pd.read_sql('select * from ' + name, conn, index_col=['stock_id', 'date']) if exist else pd.DataFrame()
    
    # 新增資料
    ret = ret.append(df)
    # 將放入資料庫的index 重設 # 注意index 也會重置
    ret.reset_index(inplace=True)
    # 確保為 字串
    ret['stock_id'] = ret['stock_id'].astype(str)
    # 確保為 時間
    ret['date'] = pd.to_datetime(ret['date'])
    # 要刪除重複項並保留最後一次出現，請使用keep. 兩個都要相同才會被刪掉
    ret = ret.drop_duplicates(['stock_id', 'date'], keep='last')
    # 將序列排序 由小到大 並設定新的index
    ret = ret.sort_values(['stock_id', 'date']).set_index(['stock_id', 'date'])
    
    # 如須備份請開啟
    #============================
    # add the combined table
    ret.to_csv('backup.csv')
    #============================
    
    try:
        # 會刪除原本所有的
        ret.to_sql(name, conn, if_exists='replace')
    except:
        ret = pd.read_csv('backup.csv', parse_dates=['date'], dtype={'stock_id':str})
        ret['stock_id'] = ret['stock_id'].astype(str)
        ret.set_index(['stock_id', 'date'], inplace=True)
        ret.to_sql(name, conn, if_exists='replace')
    
# ========================================================================================================

# update_table(conn, 'price', crawl_price, [datetime.date(2018,3,26)])
def update_table(conn, table_name, crawl_function, dates):
    
    # 顯示爬取資料
    print('start crawl ' + table_name + ' from ', dates[0] , 'to', dates[-1])
    
    df = pd.DataFrame()
    dfs = {}
    
    # 創建tqdm 顯示會以tqdm方式顯示
    progress = tqdm(dates, )
    
    for d in progress:
        # 陣列顯示時間
        print('crawling', d)
        progress.set_description('crawl' + table_name + str(d))
        
        data = crawl_function(d)
        
        # 如果沒有date 回傳 可能為星期天
        if data is None:
            print('fail, check if it is a holiday')
            
        # 爬取多筆資料
        elif isinstance(data, dict):
            if len(dfs) == 0:
                dfs = {i:pd.DataFrame() for i in data.keys()}
                    
            for i, d in data.items():
                dfs[i] = dfs[i].append(d)
                
        # 爬取單一資料
        else:
            df = df.append(data)
            print('success')

            
        if len(df) > 50000:
            add_to_sql(conn, table_name, df)
            df = pd.DataFrame()
            print('save', len(df))
        # 為避免造成太大影響 所以限制時間
        time.sleep(10)
        
        
        
    if df is not None and len(df) != 0:
        # 將資料放進資料庫
        add_to_sql(conn, table_name, df)
        
    if len(dfs) != 0:
        for i, d in dfs.items():
            print('saveing df', d.head(), len(d))
            if len(d) != 0:
                print('save df', d.head())
                add_to_sql(conn, i, d)


# ========================================================================================================