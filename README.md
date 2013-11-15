jokebutler
==========

## System name: 
JokeButler
**Link**: http://jokesbutler.appspot.com/

Instructions to use:

Log-in with your FaceBook in the top-right corner in order to keep a history of what you’ve rated.
If this is your first time to the app, you’ll start with “Round 0”. Here, you will be given 5 jokes to rate so that we can assess your preferences. In order to rate a joke, simply use the five faces below to indicate your reaction to the joke. 
After you’ve given us 5 ratings, our system calculates which jokes it recommends to you.The system will then progress through rounds where you’re given 5 new jokes each time. After this initial round 0, all the jokes in the subsequent rounds are selected and recommended based on your prior ratings. You should also not see any jokes you’ve seen before

Writeup:

Jokes have been a part of human history for as long as we’ve known it. The power of laughter and humor has been well documented, and people around the world, from different nations and of different ages, enjoy a good joke. Due to this, we were excited to find a rich data-set of joke ratings when we were exploring ideas for our recommendations project, and as a result, we present to you the Joke Butler.

All it takes to use the Joke Butler is a sense of humor and the patience to read a few jokes. Any user can use our system as it does not require someone to have heard a certain song, read a certain book, or watched a certain movie in the past. Instead, users can come to the system with no prior knowledge, rate 5 jokes to give us a taste of their preferences, and start getting personally recommended jokes. In this way, we appeal to a universal audience (with the only constraint that our jokes are in English). If you have a Facebook account, you can also log-in so that we can keep track of the jokes you’ve rated in the past. This way, you can avoid having to go through the on-boarding process each time you come to the site.

The Joke Butler is based off of the publicly available dataset of anonymous user ratings from the Jester jokes recommender system (http://eigentaste.berkeley.edu/dataset/). Using their 2nd dataset, we were able to grab data to over 1.7 million user ratings of 150 jokes. In examining the data-set, we realized that our best approach would be to use item-based filtering to generate our recommendations. We came to this decision because of two reasons. First, many users in the dataset gave ratings to only a limited set of the 150 jokes, making it difficult to rely on user-based filtering to map to our user’s ratings (i.e., sparse data-set). Second, with a dataset this large, we felt that we could achieve better speed for our end-user, as most of our calculations can be done in advance and we could update the database periodically.

So, what we’ve done is invert the database to a list of jokes along with how they were rated by users. Using the Pearson correlation score, we calculate similarity metrics for these jokes to identify the top 10 most similar joke for each joke. Based on this, we created a dictionary of each joke and its most similar jokes. The original system created by the researchers that made this dataset available(Jester) had ratings for jokes on a scale of -10-10, as they allowed users to give their ratings on an open-ended ‘slider’ scale. We did not find that this was intuitive and felt that this was a poor way to rate jokes - how do you differentiate between a -7.5 jokes and a -7.1 joke? So, we decided to use a 1-5 rating scale on our system, and normalized the ratings in the old database to this scale. We then provide users of our system 5 faces that range from a grimace to indicate you didn’t like the joke to a teeth-baring grin. We label the end-point faces and the middle face to anchor the user in what ‘rating’ those faces relate to. We felt that this was much more intuitive for the user than a numerical scale.

After the user gives us 5 ratings in the round 0 onboarding phase, we then take these ratings to calculate the top 5 jokes recommended for them. How do we find this recommendation? Using our items dictionary, we look at each joke the user has not rated yet, multiply its similarity with the five “onboard” jokes’ users ratings of that joke, calculate the sum total of the five weighted rating, and normalize it by dividing the total of five similarity. The outcome for each of these un-read jokes is then the predicted rating of that joke, and, in round 1, we display the top 5 predicted jokes to our user. Initially, we gave them 10 jokes to rate before ratings were re-calculated, but we figured that (1) people don’t like to read all that much anymore, and so their attention may wane if they have to read 10 jokes and (2) if we split it into 5 jokes per round, we would be able to re-calculate recommendations quicker for the user. As mentioned above, we only present jokes that the user has not seen yet, and we keep a history of their prior ratings to avoid repetition.

We identified a few key points as to where we differ from the Jester joke recommender system:
We do not use their ‘Eigentaste algorithm’, and instead stick with the Pearson correlation score and item-based filtering
Instead of using their -10 to 10 rating slider, we stick with a simpler to understand (for the users) 1-5 scale, which we further make easier with faces with a natural scale of emotions instead of a raw number scale.

We were able to get the core functionalities that we wanted to establish implemented. However, with more time, there were other features that we would have liked to include. Here is a brief list of what we discussed for future iterations:
Allow users to add new jokes into the database, to create a type of ‘joke community’
Rather than a randomly selected set of 5 on-boarding jokes, we could divide our jokes into ‘categories’ (politics, science, word-games, etc.), and test the user’s preferences in these categories. This would allow us to further cater our recommendations and make them more personalized and precise
Present the users with our predicted rating of a joke
While we considered this feature, we were not 100% sure whether this was something we should actually include. Apart from not wanting to influence someone’s rating and allowing them to come to their own conclusion, the showing of predicted rating like MovieLens did not seem to fit jokes. Unlike movies, where there is a significant effort cost to watch a movie (which makes it useful to know predicted ratings beforehand), we are trying to get you to laugh and give you jokes to read right then and there.
Allow the user to skip jokes they don’t want to read or rate

Overall, we are satisfied with what we have been able to implement so far. Jokes are universally beloved, and with our system, users can come in from a busy day and get a few jokes that they might particularly enjoy. With future iterations, we hope to grow the amount of jokes we can serve and allow the user to pick more specific buckets of jokes to view.
