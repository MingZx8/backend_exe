#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: MingZZZZZZZZ
# @Date created: 11 Jan 2019
# @Date last modified: 14 Jan 2019
# Python Version: Python3.6
# Description:

import tornado.web
import tornado.ioloop
import tornado.options
import requests
import json
from collections import defaultdict

# the setting of google fusion tables api
api_key = "your_google_fusion_tables_api_key"
table_id = "1pKcxc8kzJbBVzLu_kgzoAMzqYhZyUhtScXjB0BQ"
url_ft = "https://www.googleapis.com/fusiontables/v2/tables/%s?key=%s" % (table_id, api_key)
columns = list(map(lambda x:x['name'].lower(), requests.get(url_ft).json()['columns'][:])) # retrieve the name of columns in the table


# define the sever port using 5000
tornado.options.define('port', type=int, default=5000, help="server port")

class CountHandler(tornado.web.RequestHandler):
    """
    """
    def set_default_headers(self):
        self.set_header("Content-Type","application/json")

    def write_error(self, scode, **kwargs):
        if scode == 400:
            self.write(str(kwargs['content']))

    def get(self):
        global table_id, api_key
        # retrieve the arguments
        args = self.request.arguments
        # initialize the list of unknown keywords and the dictionary of params
        unknown_fields = []
        kw_dict = defaultdict(str)
        # classify the arguments
        # since it is case insensitive, the args are transferred in lower case
        for arg_temp in args:
            arg = arg_temp.lower()
            if arg in columns:
                kw_dict[arg] = self.get_arguments(arg_temp)[0].lower()
            else:
                unknown_fields.append(arg_temp)
        # if any invalid query string parameters are provided, return an error message containing the unknown fields
        if unknown_fields:
            self.send_error(400, content=json.dumps({'unknown fields': sorted(unknown_fields)}))
        else:
            # the query for the data in fusion tables(FT) is case sensitive, but FT does not support lower or upper function
            # 3 cases are considered here:
            # Upper case
            # Lower case
            # Title case
            query = ''  
            for arg in kw_dict:
                if query:
                    query += ' AND '
                query += str(arg) + " in ('" \
                        + (str(kw_dict[arg])).upper() + "','"\
                        + (str(kw_dict[arg])).lower() + "','"\
                        + (str(kw_dict[arg])).title() + "'"\
                        + ")"
            # query in the Google fusion tables API
            url_request = "https://www.googleapis.com/fusiontables/v2/query?sql=select count(dog_name) FROM %s where %s&key=%s" % (table_id, query, api_key)
            count_data = {'count': -999}
            try:
                count_data['count'] = int(requests.get(url_request).json()['rows'][0][0])
            except KeyError: # if there is not any row in the dataset
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
