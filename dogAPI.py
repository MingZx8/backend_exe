#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: MingZZZZZZZZ
# @Date created:
# @Date last modified:
# Python Version: Python3.6
# Description:

import tornado.web
import tornado.ioloop
import tornado.options
import requests
import json
from collections import defaultdict

# 初始化设置google fusion api
api_key = "AIzaSyDOVEKSUYZOIq-_evlnxPOtqFe2Z_N2gy4"
table_id = "1pKcxc8kzJbBVzLu_kgzoAMzqYhZyUhtScXjB0BQ"
url_ft = "https://www.googleapis.com/fusiontables/v2/tables/%s?key=%s" % (table_id, api_key)
columns = list(map(lambda x:x['name'].lower(), requests.get(url_ft).json()['columns'][:])) # 获取表的所有列名


#定义服务port
tornado.options.define('port', type=int, default=5000, help="server port")

class CountHandler(tornado.web.RequestHandler):
    """
    """
    def set_default_headers(self):
        self.set_header("Content-Type","application/json")

    def get(self):
        global table_id, api_key
        # 提取参数
        args = self.request.arguments
        # 判断参数是否有效, 如果全都无效，返回unknown field并打出400信号
        # 如果只有部分无效则无视
        unknown_fields = []
        kw_dict = defaultdict(str) #初始化装载参数的字典
        for arg_temp in args:
            arg = arg_temp.lower()
            if arg in columns:
                kw_dict[arg] = self.get_arguments(arg_temp)[0].lower()
            else:
                unknown_fields.append(arg_temp)
        if unknown_fields:
            self.set_status(400)
            self.write(json.dumps({'unknown fields': sorted(unknown_fields)}))
        else:
            # 拼接参数为query函数并从fusion table获取数据
            # fusion table大小写敏感，并且不支持lower或者upper函数
            # 分全小写，全大写和单词首字母大写的情况
            query = ''  
            for arg in kw_dict:
                if query:
                    query += ' AND '
                query += str(arg) + " in ('" \
                        + (str(kw_dict[arg])).upper() + "','"\
                        + (str(kw_dict[arg])).lower() + "','"\
                        + (str(kw_dict[arg])).title() + "'"\
                        + ")"
            url_request = "https://www.googleapis.com/fusiontables/v2/query?sql=select count(dog_name) FROM %s where %s&key=%s" % (table_id, query, api_key)
            count_data = {'count': -999}
            try:
                count_data['count'] = int(requests.get(url_request).json()['rows'][0][0])
            except:
                count_data['count'] = 0
            count_json = json.dumps(count_data)
            self.write(count_json)


def make_app():
    return tornado.web.Application([
        (r"/count", CountHandler),
        ],
    debug = True
    )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
