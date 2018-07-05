#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
import os
import jinja2
import cgi

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)

class BaseHandler(webapp2.RequestHandler):
    def render(self, html, values={}):
        template = JINJA_ENVIRONMENT.get_template(html)
        self.response.write(template.render(values))

class MainHandler(BaseHandler):
    def get(self):
        self.render("main.html")

class ResultHandler(BaseHandler):
    def get(self):
        self.render("main.html")
        text1 = cgi.escape(self.request.get("text1"))
        text2 = cgi.escape(self.request.get("text2"))
        mix_text = ""
        for t1, t2 in zip (text1, text2):
            mix_text += t1 + t2
        self.response.out.write(mix_text)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/result', ResultHandler)
], debug=True)
