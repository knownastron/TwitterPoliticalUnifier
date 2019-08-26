**a description of the project(s) and the final deliverables**
So this idea will need some insight from you to flesh out. But the general idea
is I want to use a combination of Natural Language Processing and Graph analysis
(perhaps ML as well) on Twitter data to group users into 'Conservatives' and
'Liberals' (or more categories, but those to start) and be able to find tweets
that are liked by both groups. Basically it finds reverse "scissor statements".

So the end product I'm envisioning is a UI where you enter a link to a tweet and
it gives you a 'polarity score' between 0 and 100. 50 being a balanced tweet where
both liberals and conservatives like it. The closer the score is to 0 or 100 the
more it is liked by liberals or conservatives exclusively.

I also imagine that I can allow users to perhaps enter a hashtag and use the
streaming API to collect 50-100 tweets and doing the analysis on a number of
tweets to see how polarized a topic is.

Another possibility is to find the top 10 most or least polarized tweets
by hashtag?

The motivation for this is that America's political climate is really polarized
right now and being able to find topics or ideas that cut across party lines would
be interesting and perhaps useful? I also have interest in NLP and data science
in general.


**project milestones**
Milestones (not in order):

- Build Twitter data collector using a combination of Twitter API and web scraping
- Gather adequate amount of data for graph and NLP testing
- Create database model
- Build NLP model
- Build graph distance model (conservatives should be farther away from liberals
  than to other conservatives)
- Build server
- build front end


**the proposed mentor**
Since this is a data science focused project, I think Ben would be best. But
that's just based on the fact that Ben teaches the data science course. But I'm
happy to have either Ben or Varun as a mentor.


**skills/tools the you expect you'll need to learn/develop to complete the project**
- Data science (NLP, Graph analysis, ML)
- Some web dev stuff for the frontend/server


**"risks" that you think might make the project difficult/impossible, other concerns**
- Not being able to gather enough data from Twitter
- Will I be able to organize the vast amount of data needed to accomplish this?
  Ideally I have a graph of a couple million users, right?
- I'm limited by Twitter's API, I can make 180 calls per 15 mins for free tier.
  I'd be willing to pay for access to a higher tier of their API for 3 months,
  hopefully not because it starts at $149/mo but if I have to I will.
- Can I do this efficiently? An intelligent way to cache user information will
  be really important


**Questions I have regarding this project**
- how do I keep a persistent graph? I can't imagine building this graph each in
  memory and then discarding it every time I need to use it and then discarding it
- Is there a way to implement ML in this project?
