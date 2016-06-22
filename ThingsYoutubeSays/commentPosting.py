def post(comments):
    for text, likes in comments:
        print text, type(text)
        print likes, type(likes)
        print
