from apiclient.errors import HttpError
from oauth2client.tools import argparser
from apiclient.discovery import build


def getComment(video_id, top5):
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    DEVELOPER_KEY = 'AIzaSyDax4ZKlDqcSahH4M6-I1u1NumzLUf_g7s'
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    try:
        minLikes = 0

        results = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            order="relevance",
            maxResults = 100
            ).execute()

        #Get the first set of comments
        for item in results["items"]:
        #threads.append(item)
          comment = item["snippet"]["topLevelComment"]
          text = comment["snippet"]["textDisplay"]
          likes = comment["snippet"]["likeCount"]
          
          if likes > minLikes:
             #Removing the last comment (also the one with the least likes)
             top5.pop()
             #Inserting the new comment
             for i in xrange(5):
                tupleToInsert = (text,likes)
                if i == 4:
                   top5.append(tupleToInsert)
                   break
                words, count = top5[i]
                if likes > count:
                   top5.insert(i, tupleToInsert)
                   break
             minLikes = top5[4][1]
              

        #Keep getting comments from the following pages
        while ("nextPageToken" in results):
            results = youtube.commentThreads().list(
              part="snippet",
              videoId=video_id,
              pageToken=results["nextPageToken"],
              textFormat="plainText",
              order="relevance",
              maxResults = 100
            ).execute()
            for item in results["items"]:
              #threads.append(item)
              comment = item["snippet"]["topLevelComment"]
              text = comment["snippet"]["textDisplay"]
              likes = comment["snippet"]["likeCount"]
              
              if likes > minLikes:
                 #Removing the last comment (also the one with the least likes)
                 top5.pop()
                 #Inserting the new comment
                 for i in xrange(5):
                    tupleToInsert = (text,likes)
                    if i == 4:
                       top5.append(tupleToInsert)
                       break
                    words, count = top5[i]
                    if likes > count:
                       top5.insert(i, tupleToInsert)
                       break
                 minLikes = top5[4][1]
            #print "Total threads: %d" % len(threads)

        
    
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)



