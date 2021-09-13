import json
import tweepy
from secrets_manager import SecretsManager

sm = SecretsManager()

api_key = sm('api_key')
api_secret_key = sm('api_secret_key')
access_token = sm('access_token')
access_token_secret = sm('access_token_secret')

def lambda_handler(event, context):

    
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    since_id = None
    my_name = 'BotDarry'
    
    status_list = api.home_timeline(since_id=since_id)
    
    status_counter = 0
    like_counter = 0
    
    for status in status_list:
        status_counter += 1
        for mention in status.entities['user_mentions']:
            if mention['screen_name'] == my_name:
                # print(status.id, status.user.name)
                like_counter += 1
                api.create_favorite(status.id)
            
    # print('Done')
    
    return {
        'statusCode': 200,
        'total_num_status' : status_counter,
        'total_likes_created' : like_counter,
        'body' : f'Run successful! Created {like_counter} new likes from {status_counter} tweets in timeline.'
    }
