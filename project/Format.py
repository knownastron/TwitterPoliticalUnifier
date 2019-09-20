import re


def format_tweet_text(text):
    '''
    replaces newline character with a space, removes links

    :param text: the tweet text reformatted
    :return:
    '''

    text = remove_new_line(text)
    text = remove_hyperlinks(text)

    return text.strip()


def format_username(username):
    if username[0] != '@':
        return '@' + username
    else:
        return username


def remove_new_line(text):
    return text.replace("\n", " ")


def remove_hyperlinks(text):
    return re.sub(r"http\S+", "", text)


def remove_hashtags(text):
    return re.sub(r"#\S+", "", text)


def remove_mentions(text):
    return re.sub(r"@\S+", "", text)

def remove_picture_links(text):
    return re.sub(r"pic.twitter.com\S+", "", text)
