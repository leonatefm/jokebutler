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

import urllib, os, random, json
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
    
def getRecommendations(ratings, number):
    logging.info(ratings)
    user_rating = dict()
    for key in ratings:
        user_rating[int(key)] = ratings[key]
    user_ratings = {'current':user_rating}
    rec_list = recommendations.getRecommendedItems(user_ratings, jokesim.sim_critics, 'current')
    if len(rec_list) > 10:
        rec_list = rec_list[0:10]
    
    logging.info(rec_list)
    rec_jokes = list()
    for item in rec_list:
        # rec_jokes[item[1]] = jokes.jokes[item[1]]
        rec_jokes.append((item[1], jokes.jokes[item[1]], item[0]))
    return rec_jokes

class MainPage(webapp2.RequestHandler):
    def get(self):
        
        random_jokes = getRandomJokes(5)
        
        logging.info(random_jokes)
        logging.info(random_jokes.keys())
        
        template_values = {
            'randomjokes': random_jokes,
            'jokescount': len(random_jokes),
        }
        template = JINJA_ENVIRONMENT.get_template('/views/index.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        user_ratings = json.loads(self.request.get('ratings'))
        rec_jokes = getRecommendations(user_ratings, 10)

        rec_data = {"rec_jokes":rec_jokes}
        
        self.response.out.write(json.dumps(rec_data))



app = webapp2.WSGIApplication([('/', MainPage)])
