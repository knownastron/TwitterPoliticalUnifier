import re


class Format():
    @staticmethod
    def format_tweet_text(text):
        '''
        replaces newline character with a space, removes links

        :param text: the tweet text reformatted
        :return:
        '''

        text = remove_new_line(text)
        text = remove_hyperlinks(text)

        return text.strip()

    @staticmethod
    def format_username(username):
        if username[0] != '@':
            return '@' + username
        else:
            return username

    @staticmethod
    def remove_new_line(text):
        return text.replace("\n", " ")

    @staticmethod
    def remove_hyperlinks(text):
        return re.sub(r"http\S+", "", text)

    @staticmethod
    def remove_hashtags(text):
        return re.sub(r"#\S+", "", text)

    @staticmethod
    def remove_mentions(text):
        return re.sub(r"@\S+", "", text)

    @staticmethod
    def remove_picture_links(text):
        return re.sub(r"pic.twitter.com\S+", "", text)

    @staticmethod
    def remove_hashtags(text):
        return re.sub(r"#[\w]*", "", text)

    @staticmethod
    def remove_mentions(text):
        return re.sub(r"@[\w]*", "", text)

    @staticmethod
    def remove_punctuation(text):
        return text.translate(str.maketrans('','',string.punctuation + '—' + '“' + '…'))

    
