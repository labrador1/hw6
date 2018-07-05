#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from google.appengine.api import urlfetch
import json
import jinja2

networkJson = urlfetch.fetch("http://nausicaa.fantasy-transit.appspot.com/net?format=json").content  # ウェブサイトから電車の線路情報をJSON形式でダウンロードする
network = json.loads(networkJson.decode('utf-8'))  # JSONとしてパースする（stringからdictのlistに変換する）

tmpl = jinja2.Template(  # Jinjaのテンプレートエンジンを使ってHTMLを作ります
    u'''
<form action = "/search">
    <label> 出発地: </label>
        <select name = start>
            {% for line in network %}
                <option disabled>{{line["Name"]}}</option>
                {% for station in line["Stations"] %}
                    <option name="text1">{{station}}</option>
                {% endfor %}
            {% endfor %}
        </select>
    <label> 目的地: </label>
        <select name = goal>
            {% for line in network %}
            <option disabled>{{line["Name"]}}</option>
                {% for station in line["Stations"] %}
                    <option  name="text1">{{station}}</option>
                {% endfor %}
            {% endfor %}
        </select>
    <input type=submit value="乗り換え案内">
</form>
''')

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        self.response.write(tmpl.render(network=network))
        
class SearchPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        start = self.request.get("start")
        goal = self.request.get("goal")
        
        self.response.write("出発地：")
        self.response.write(start)
        self.response.write("　")
        self.response.write("目的地：")
        self.response.write(goal)
        
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/search', SearchPage),
], debug=True)
