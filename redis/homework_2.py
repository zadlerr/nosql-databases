import redis
import datetime


ONE_WEEK_IN_SECONDS = 7 * 86400
VOTE_SCORE = 432

def article_vote(redis, user, article, inc):
    if inc > 0:
	inc = 1
    elif inc < 0:
	inc = -1
    else:
	print('inc value can\'t be zero')
	return -1
    cutoff = datetime.datetime.now() - datetime.timedelta(seconds=ONE_WEEK_IN_SECONDS)

    if not datetime.datetime.fromtimestamp(redis.zscore('time:', article)) < cutoff:
        article_id = article.split(':')[-1]
        if redis.sadd('voted:' + article_id, user):
            redis.zincrby(name='score:', value=article, amount=VOTE_SCORE*inc)
            redis.hincrby(name=article, key='votes', amount=inc)

def article_switch_vote(redis, user, from_article, to_article):
    # HOMEWORK 2 Part I
    idx = from_article.split(':')[1]
    idx2 = to_article.split(':')[1]
    name = 'voted:'
    if redis.sismember(name + idx, user):
	#remove and decrement from_article
	redis.srem(name + idx, user)
	article_vote(redis, user,from_article ,-1)
	#add and increment to_article
	redis.sadd(name + idx2, user)
	article_vote(redis, user,to_article ,1)

redis = redis.StrictRedis(host='localhost', port=6379, db=0)
# user:3 up votes article:1
article_vote(redis, "user:3", "article:1", 1)
# user:3 up votes article:3
article_vote(redis, "user:3", "article:3", 1)
# user:2 switches their vote from article:8 to article:1
article_switch_vote(redis, "user:2", "article:8", "article:1")

# Which article's score is between 10 and 20?
# PRINT THE ARTICLE'S LINK TO STDOUT:
# HOMEWORK 2 Part II

lst = redis.zrange('score:', 0, -1, withscores=True)
sol = 0
for pair in lst:
    if pair[1] > 10.0 and pair[1] < 20.0:
	sol = pair[1]
	article = pair[0]

ret = redis.hgetall(article)
print(ret['link'])


