#Necessary Imports
import unicodedata
import praw
import os

#Check that the required files are there
if not  os.path.isfile("config_bot.py"):
    print "You must create a config file with your username and password."
    exit(1)
if not  os.path.isfile("topComments.py"):
    print "You are missing the Youtube Comment Scraper."
    exit(1)

import topComments
from config_bot import *

#Function that calls on topComments to get the comments to post on reddit
def youtubeComments(vid_id):
    top5 = [('',0) for i in xrange(5)]
    topComments.getComment(vid_id, top5)

    for i in xrange(5):
        x,y = top5[i]
        newText = unicodedata.normalize('NFKD', x).encode('ascii','ignore')
        newText = newText.splitlines()
        if len(newText) != 1: #If the length of newtext is not 1, it means there were \n characters in the string. We join these together to get 1 string
            newText = ' '.join(newText)
        else:
            newText = newText[0]
        
        top5[i] = [newText, y]

    return top5

#Function that posts the response
def responsePost(bestComments):
    textToPost = """**The most liked comments on YouTube for this video are:**

Likes | Comments 
---------|---------
%s | %s 
%s | %s 
%s | %s 
%s | %s 
%s | %s 

*Hello, I am a bot that posts YouTube comments for videos.*
""" % (bestComments[0][1], bestComments[0][0],
       bestComments[1][1], bestComments[1][0],
       bestComments[2][1], bestComments[2][0],
       bestComments[3][1], bestComments[3][0],
       bestComments[4][1], bestComments[4][0])
    post.add_comment(textToPost)

    
#Initializing and logging in
user_agent = ("Things_YouTube_Says Bot 0.1")

r = praw.Reddit(user_agent = user_agent)

r.login(REDDIT_USERNAME, REDDIT_PASS)

#Selecting subreddit
subreddit = r.get_subreddit("test")

#Opening our database of posts replied to already
if not os.path.isfile('repliedPosts.txt'):
    posts_replied_to = []

else:
    with open('repliedPosts.txt','r') as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split()
        posts_replied_to = filter(None, posts_replied_to)

#Getting posts from reddit 
for post in subreddit.get_new(limit=10): #Can also be get_hot
    
    link = post.url
    link = unicodedata.normalize('NFKD', link).encode('ascii','ignore')
    
    if 'www.youtube.com' in link:
        if post.id not in posts_replied_to:

            #Getting the video id of the Youtube video
            start = link.index('watch?v=')+8
            #This is for videos in a playlist
            if '&' in link:
                end = link.index('&')
                video_id = link[start:end]
            #This is for normal linked videos
            else:
                video_id = link[start:]
                
            print video_id

            result = youtubeComments(video_id)
            print "Bot replying to : ", post.title
            
            responsePost(result)
        
            posts_replied_to.append(post.id)
            break #This break ensures that we do 1 video at a time. If it does not break, Reddit's ratelimit will return an error
        

with open("repliedPosts.txt", "a") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")

##    print "Score: ", submission.score



