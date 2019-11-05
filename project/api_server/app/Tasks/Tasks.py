import random
import time
import celery
from celery import Celery

config = {
    'CELERY_BROKER_URL': 'redis://localhost:6379/0',
    'CELERY_RESULT_BACKEND': 'redis://localhost:6379/0'
}

#Set up Celery
celery = Celery('CeleryTest', broker=config['CELERY_BROKER_URL'])
celery.conf.update(config)


@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)

    print('entered long task function')
    for i in range(total):
        print(i)
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}

@celery.task(bind=True)
def predict_user(self, screen_name, app_user):
    pass
    # if screen_name already in db,
        # update app_user's profile

    # else
        #scrape tweets for the user
        #run it through the NLP
        #write results to the DB

@celery.task(bind=True)
def predict_tweet(self, screen_name, tweet_id, app_user):
    #if tweet already in db,
        # update app_user's profile

    #else
        # get screen name of likers
        # scrape tweets of all users
        # run it through NLP
        # update app_user's profile



