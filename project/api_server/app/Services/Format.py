import re
import nltk
nltk.download('stopwords')
import string
from nltk.stem.porter import PorterStemmer


class Format():
    stem = PorterStemmer()
    stopwords = set(nltk.corpus.stopwords.words('english') + ['it\'s', 'w/', '\'s'])


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
        if username[0] == '@':
            return username[1:]
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

    @staticmethod
    def remove_stopwords(input_text_split):
        """
        :param input_text: an array of strings
        :return: an array of strings
        """
        output_text_split = [word for word in input_text_split if word not in Format.stopwords]
        return output_text_split

    @staticmethod
    def stem_words_str(input_text):
        """
        :param input_text_split: An string of words
        :return: a string of words
        """
        input_text_split = input_text.split()
        stemmed_output = [Format.stem.stem(word) for word in input_text_split]
        return ''.join(stemmed_output)

    @staticmethod
    def stem_words_list(input_text_split):
        """
        :param input_text_split: An array of strings
        :return: an array of strings
        """
        stemmed_output = [Format.stem.stem(word) for word in input_text_split]
        return stemmed_output

    @staticmethod
    def remove_punctuation(text):
        return text.translate(str.maketrans('', '', string.punctuation + '—' + '“' + '…' + '\’' + '\”'))

    @staticmethod
    def denoise_tweet(tweet_text):
        tweet_text = tweet_text.lower()
        tweet_text = Format.remove_hyperlinks(tweet_text)
        tweet_text = Format.remove_picture_links(tweet_text)
        tweet_text = Format.remove_hashtags(tweet_text)
        tweet_text = Format.remove_mentions(tweet_text)
        tweet_text = Format.remove_picture_links(tweet_text)
        tweet_text = Format.remove_punctuation(tweet_text)
        tweet_text_split = tweet_text.split()
        tweet_text_split = Format.remove_stopwords(tweet_text_split)

        return " ".join(tweet_text_split)
