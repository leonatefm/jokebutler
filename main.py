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
import webapp2, jinja2, logging, facebook
import jokes, jokesim, recommendations

from google.appengine.ext import ndb
from google.appengine.api import users

FACEBOOK_APP_ID = "701530443205317"
FACEBOOK_APP_SECRET = "0eb5f65825ee5b53b1904c6b99f18838"

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
class record(ndb.Model):
    userid = ndb.StringProperty()
    ratings = ndb.JsonProperty()
    
def getRandomJokes(number):
    joke_keys = jokesim.sim_critics.keys()
    random_joke_keys = random.sample(joke_keys, number)
    random_jokes = list()
    for key in random_joke_keys:
        random_jokes.append((key, jokes.jokes[key]))
    return random_jokes
    
def getRecommendations(ratings, number):
    # logging.info(ratings)
    user_rating = dict()
    for key in ratings:
        user_rating[int(key)] = ratings[key]
    user_ratings = {'current':user_rating}
    rec_list = recommendations.getRecommendedItems(user_ratings, jokesim.sim_critics, 'current')
    if len(rec_list) > number:
        rec_list = rec_list[0:number]
    
    # logging.info(rec_list)
    rec_jokes = list()
    for item in rec_list:
        # rec_jokes[item[1]] = jokes.jokes[item[1]]
        rec_jokes.append((item[1], jokes.jokes[item[1]], item[0]))
    return rec_jokes

class MainPage(webapp2.RequestHandler):
    def get(self):

        try:
            user = facebook.get_user_from_cookie(self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
        except:
            user = None
        
        if user:
            graph = facebook.GraphAPI(user["access_token"])
            profile = graph.get_object("me")
            user_name = profile['name']
            user_id = profile['id']
            current_user = {
                'id': user_id,
                'name': user_name
            }
            
            user_record = record.get_by_id(user_id)
            
            if user_record:
                ratings = user_record.ratings
                rec_jokes = getRecommendations(ratings, 5)
                
                user_rating = dict()
                for key in ratings:
                    user_rating[int(key)] = ratings[key]
                
                template_values = {
                    'jokes': rec_jokes,
                    'jokescount': len(rec_jokes),
                    'user': current_user,
                    'ratings': user_rating,
                    'round': len(user_rating)/5
                }
                
            else:    
                random_jokes = getRandomJokes(5)
                template_values = {
                    'jokes': random_jokes,
                    'jokescount': len(random_jokes),
                    'user': current_user
                }
        else:

            random_jokes = getRandomJokes(5)
            template_values = {
                'jokes': random_jokes,
                'jokescount': len(random_jokes),
            }
                    

        template = JINJA_ENVIRONMENT.get_template('/views/index.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        user_ratings = json.loads(self.request.get('ratings'))
        user_id = self.request.get('userid')
        
        if user_id:
            logging.info(user_id)
            newrecord = record(id = str(user_id), userid = user_id, ratings = user_ratings)
            newrecord.put()
            
            logging.info(record.get_by_id(user_id))
            
        else:
            logging.info('no id, no database, dude')
        
        rec_jokes = getRecommendations(user_ratings, 5)

        rec_data = {"rec_jokes":rec_jokes}
        
        self.response.out.write(json.dumps(rec_data))


class CheckUser(webapp2.RequestHandler):
    def post(self):
        user_id = self.request.get('userid')
        
        if record.get_by_id(user_id):
            self.response.out.write('Yes')
        else:
            self.response.out.write('No')
            
            
app = webapp2.WSGIApplication([('/', MainPage),('/checkuser', CheckUser)])
