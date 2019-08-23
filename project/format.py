def formatTweetText(text):
    '''
    replaces newline character with a space
    '''
    text = text.replace("\n", " ")

    return text

def format_username(username):
    if username[0] != '@':
        return '@' + username
    else:
        return username
