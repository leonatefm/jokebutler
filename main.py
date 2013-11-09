#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import urllib, os, random
import webapp2, jinja2, logging
import jokes, jokesim, recommendations

from google.appengine.ext import ndb
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
def getRandomJokes(number):
    joke_keys = jokesim.sim_critics.keys()
    random_joke_keys = random.sample(joke_keys, number)
    random_jokes = dict()
    for key in random_joke_keys:
        random_jokes[key] = jokes.jokes[key]
    return random_jokes

class MainPage(webapp2.RequestHandler):
    def get(self):
        
        random_jokes = getRandomJokes(5)
        
        logging.info(random_jokes)
        logging.info(random_jokes.keys())
        
        template_values = {
            'randomjokes': random_jokes,
        }
        template = JINJA_ENVIRONMENT.get_template('/views/index.html')
        self.response.write(template.render(template_values))



app = webapp2.WSGIApplication([('/', MainPage)])
