import random
import string

import nltk
# Uncomment and run only once - Kent
# nltk.download("stopwords")

import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

### BUILDING A SELF LEARNING BOT - RETRIEVAL BASED MODEL ###

# goal: select a response from a library of predefined responses
# use the message and context to reply
# using NLTK - Natural Language ToolKit


class Quote(object):

    @staticmethod
    def quote(user_input):

        # preprocess the text to lowercase letters to remove noise
        f = open("trump_sample_corpus.txt", encoding="utf-8")
        raw = f.read()

        raw = raw.lower()

        # tokenize the sentences
        sent_tokenizer = nltk.sent_tokenize(raw)
        word_tokenizer = nltk.word_tokenize(
            raw, "english", preserve_line=True)

        # stop words:
        stop_words = set(nltk.corpus.stopwords.words("english"))

        # instantiate the lemmatizer
        lemmer = nltk.stem.WordNetLemmatizer()

        l1 = lemmer.lemmatize("running")

        def LemTokens(tokens):
            return [lemmer.lemmatize(token) for token in tokens]

        remove_punct_dict = dict((ord(punct), None)
                                 for punct in string.punctuation)

        def LemNormalize(text):
            return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

        # sent1 = "We cannot continue to let Israel be treated with such total disdain and disrespect. They used to have a great friend in the U.S., but......."
        # print(sent1)

        # s1 = LemNormalize(sent1)
        # print(s1)

        # stop words:

        def response(user_input):
            stop_words = set(nltk.corpus.stopwords.words("english"))
            Tfidf = TfidfVectorizer(
                tokenizer=LemNormalize, stop_words=stop_words)
            tfidf = Tfidf.fit_transform(sent_tokenizer)
            vals = cosine_similarity(tfidf[-1], tfidf)
            idx = vals.argsort()[0][-2]
            flat = vals.flatten()
            flat.sort()
            req_tfidf = flat[-2]
            robo_response = sent_tokenizer[idx]
            return(robo_response)

        sent_tokenizer.append(user_input)
        word_tokens = word_tokenizer+nltk.word_tokenize(user_input)
        final_words = list(set(word_tokens))

        return response(user_input)


if __name__ == "__main__":
    print(Quote.quote(input("Input something\n> ")))
