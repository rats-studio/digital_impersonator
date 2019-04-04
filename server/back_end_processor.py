import random
import string
import spacy
import pandas as pd
from pprint import pprint
# from spacy import displacy
from collections import Counter
import en_core_web_sm
import random
import warnings
from server.memify import Meme


class Quote(object):

    @staticmethod
    def quote(user_input):

        nlp = en_core_web_sm.load()

        pd.set_option('max_colwidth', 120)
      
        # warnings.filterwarnings('ignore')

        tw = pd.read_csv("tweets_trump1.csv", low_memory = False)
        tw = tw[tw["screen_name"] == "realDonaldTrump"]
        tweets = tw[["screen_name", "text"]]
        tweets["text"] = tweets["text"].replace(r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)
        tweets["text"] = tweets["text"].replace(r'https?:\/\/.*[\r\n]*', '', regex=True).replace(r'www\S+', '', regex=True)
        tweets["text"] = tweets["text"].replace(r'RT @\S+:', '', regex = True)
        tweets["text"] = tweets["text"].replace(r'[_"\-;%()|.,+&=*%]', '', regex = True)
        tweets["text"] = tweets["text"].replace(r'@\s+', '', regex=True)
        tweets["text"] = tweets["text"].replace(r'@\S+', '', regex=True)
        tweets["text"] = tweets["text"].replace(r'&amp', 'and', regex=True)
        tweets["text"] = tweets["text"].str.replace(".@", "@")
        tweets["text"] = tweets["text"].replace(r'\n','', regex=True)
        tweets["text"] = tweets["text"].str.replace("w/", "with")
        tweets["text"] = tweets["text"].str.replace("- ", "")
        tweets["text"] = tweets["text"].str.replace("--", "")
        tweets["text"] = tweets["text"].str.replace("RE:", "")
        tweets["text"] = tweets["text"].str.replace('(&amp)', '')
        #tweets["text"] = tweets["text"].str.replace(r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", "")
        tweets["text"] = tweets["text"].replace('\n', ' ').replace('\r', '')

        tweets1 = tweets["text"]

        # tweets shape of the column
        tweets1.shape

        # transform the tweets to strings to be read by spaCy
        tweets2 = tweets1.to_string(header=False, index=False)
        tweets2 = tweets2.replace('\n', ' ').replace('\r', '').strip()

        # visualize with displacy how the dependencies look on a sample

        doc =  nlp(tweets1.sample().values[0])

        # displacy.render(doc, style="dep", jupyter=True, options={'distance': 90})

        # split the tweets since the spaCy parser cannot work on a huge corpus
        tweets3 = tweets2[0:1000000]
        doc = nlp(tweets3)
        doc1 = nlp(tweets2[1000000:2000000])
        doc2 = nlp(tweets2[2000000:3000000])
        doc3 = nlp(tweets2[3000000:4000000])

        # list of docs
        docs = [doc, doc1, doc2, doc3]

        ners = Counter()
        def get_ner(corpus, collection):
            for ent in corpus.ents:
                ners[ent.text, ent.label_] +=1
                
        for i in docs:
            get_ner(i, ners)
            
        ner = ners.most_common(20)
        ner

        # get verbs following a subject
        # Finding a verb with a subject from below — good
        verbs = set()
        for possible_subject in doc:
            if possible_subject.dep_ == 'nsubj' and possible_subject.head.pos_ == 'VERB':
                verbs.add(possible_subject.head.lemma_)

        # get adjectives and nouns
        def get_adj_noun(corpus, collection):
            for token in corpus:
                try:
                    if token.pos_ == "ADJ":
                        if corpus[token.i +1].pos_ == "NOUN":
                            collection.append([str(token), str(corpus[token.i+1])])
                except IndexError:
                    pass
                        
        adj_nouns = list()
        for i in docs:
            get_adj_noun(i, adj_nouns)
            

        #try out some examples
        r = random.choice(adj_nouns)
        s = "I am an expert in "
        s += r[0]
        s += " "
        s += r[1]
        s += ". - Donald (the bot) Trump"


        ger = Counter()

        def get_top_gerunds(corpus, collection):
            for token in corpus:
                if token.tag_ == "VBD":
                    collection[str(token.text).lower()] +=1
                    
        for i in docs:
            get_top_gerunds(i, ger)
            

        g = random.choice(list(ger.keys()))
        g1 = random.choice(list(ger.keys()))
        g2 = random.choice(list(ger.keys()))
        s1 = "I have "
        s1 += str(g).lower()
        s1 += ", "
        s1 += str(g1).lower()
        s1 += " and "
        s1 += str(g2).lower()
        s1 += " without being scared. -Donald (the bot) Trump"


        c = Counter()

        def get_top_verbs(corpus, collection):
            for token in corpus:
                if token.tag_ in ["VB", "VBG", "VBP", "VBD", "VBN", "VBZ"]:
                    collection[str(token.lemma_).lower()] +=1
                
        for i in docs:
            get_top_verbs(i, c) 

        c2 = Counter()
        def get_words_after_is(corpus, collection):
            for token in corpus:
                try:
                    if token.text == "is" and corpus[token.i+1].text == "a":
                        if corpus[token.i +2].tag_ == "NN" and corpus[token.i+2].pos:
                            collection[str(corpus[token.i +2]).lower()] += 1
                except IndexError:
                    pass
                
        for i in docs:
            get_words_after_is(i, c2)

        # Get top nouns in singulas and plural

        c1 = Counter()

        def get_top_nouns(corpus, collection):
            for token in corpus:
                if token.tag_ in ["NN", "NNS"]:
                    c1[str(token.text).lower()] +=1

        # run the function
        for i in docs:
            get_top_nouns(i, c1)
        c1.most_common(10)


        # Try noun_chunks


        nc = set()
        def get_noun_chunks(doc, collection):
            for np in doc.noun_chunks:
                collection.add(np.text)


        get_noun_chunks(doc, nc)

        # ### Functions


        def get_dependencies(doc, collection, dep1 = None, dep2 = None, dep3 = None):
            """get the dependencies (up to 3) and store them in separate collections as lists
            dependencies available are (examples): dobj, nsubj, csubj, aux, neg, ROOT, det, quantmod etc."""
            try:
                if dep2 == None:
                    for token in doc:
                        if token.dep_ == dep1:
                            collection.append([str(token.text)])

                elif dep3 == None:
                    for token in doc:
                        if token.dep_ == dep1:
                            if doc[token.i +1].dep_ == dep2:
                                collection.append([str(token.text), str(doc[token.i+1].lemma_)])
                else:
                    for token in doc:
                        if token.dep_ == dep1:
                            if doc[token.i +1].dep_ == dep2 and doc[token.i +2].dep_ == dep3:
                                collection.append([str(token.text), str(doc[token.i+1].text), str(doc[token.i+2].text)])
            except IndexError:
                pass


        def get_tags(doc, collection, tag1, tag2):
            """get 2 tags in the documents"""
            for tag in doc:
                if tag.tag_ == "tag1":
                    if doc[tag.i + 1].tag_ == "tag2":
                        collection.add([str(tag), str(doc[tag.i+1])])

        def get_dependencies_lemmatized(doc, collection, dep1 = None, dep2 = None, dep3 = None):
            """get the dependencies (up to 3) and store them in separate collections as lists
            dependencies available are (examples): dobj, nsubj, csubj, aux, neg, ROOT, det, quantmod etc."""
            try:
                if dep2 == None:
                    for token in doc:
                        if token.dep_ == dep1:
                            collection.append([str(token.text), str(doc[token.i+1])])

                elif dep3 == None:
                    for token in doc:
                        if token.dep_ == dep1:
                            if doc[token.i +1].dep_ == dep2:
                                collection.append([str(token.text), str(doc[token.i+1].lemma_)])
                else:
                    for token in doc:
                        if token.dep_ == dep1:
                            if doc[token.i +1].dep_ == dep2 and doc[token.i +2].dep_ == dep3:
                                collection.append([str(token.lemma_), str(doc[token.i+1]), str(doc[token.i+2])])
            except IndexError:
                pass


        def deps_printout(sentence):
            """Prints out the text, tag, dep, head text, head tag, token lemma and part 
            of speech for each word in a sentence"""
                        
            doc1 = nlp(sentence)

            for token in doc1:
                print("{0}/{1} <--{2}-- {3}/{4} {5} {6}".format(
                    token.text, token.tag_, token.dep_, token.head.text, token.head.tag_, token.lemma_, token.pos_))


        # ### Templates:
        # - In order to get a sense of what we need, there is a function that simply displays the dependency tree: 

        deps_printout("The beauty of me is that I am very rich.")


        # Template 1

        # get dependencies for the template You should never try To
        def get_ngrams_for_template1():
            adv_acomp = []
            for i in docs:
                for i in docs:
                    get_dependencies(i, adv_acomp, dep1 = "advmod", dep2 = 'acomp')
            return adv_acomp

        t1_src = get_ngrams_for_template1()

        def template1(source):
            # complete the sentence and return it
            a1 = random.choice(source)
            temp1 = "The beauty of me is that I am " + " ".join([x for x in a1])
            temp1 += ". - Donald (the bot) Trump"
            return temp1

        template1(t1_src)


        # Template 2


        def get_ngrams_for_template2():
            # Get ROOT + AMOD + DOBJ IN THE FORM OF VERB + ADJ + NOUN
            van = []

            for i in docs:
                for token in i:
                    if token.dep_ == "amod" and token.pos_ == "ADJ":
                        if i[token.i + 1].dep_ == "dobj" and i[token.i+1].pos_ == "NOUN" and i[token.i+1].tag_ == "NN"                     and i[token.i+2].dep_ == "punct":
                            van.append([str(token.text).lower(), str(i[token.i+1].text).lower()])
            return van
            
        t2_src = get_ngrams_for_template2()

        def template2(source):
            v = random.choice(source)
            start = "Is there such a thing as an "
            start1 = "Is there such a thing as "
            start2 = "Is there such a thing as a "
            end = "? - Donald (the bot) Trump"
            if len(v[1]) <=2:
                pass
            elif v[0][0] in["a", "e", "i", "o", "u"]:
                temp2 = start + " ".join([x for x in v]) + end
            elif v[0] == "great":
                temp2 = start1 + " ".join([x for x in v]) + end
            else:
                temp2 = start2 + " ".join([x for x in v]) + end
            return temp2



        template2(t2_src)


        # Template 3


        # show the dependencies in the sample
        deps_printout("My Twitter has become so powerful that I can actually make my enemies tell the truth.")



        def get_ngrams_for_template3():
            det_d = []
            for i in docs:
                get_dependencies_lemmatized(i, det_d, dep1 = "ccomp", dep2 = 'det', dep3 = "dobj")
                
            return det_d

        t3_src = get_ngrams_for_template3()

        def template3(source1, source2):
            a2 = random.choice(source1)
            a3 = random.choice(source2)
            
            t = "My Twitter has become an "
            t_1 = "My Twitter has become a "
            mid = ", I can actually make my enemies "
            end = ". - Donald (the bot) Trump"
            
            if len(a3[0]) <= 2:
                pass
            elif a3[0][0] in ["a", "e", "i", "o", "u"]:
                #a = (*a3, sep=" ")
                temp3 = t + " ".join([x for x in a3]) + mid + " ".join([x for x in a2]) + end
            else:
                temp3 = t_1 + " ".join([x for x in a3]) + mid + " ".join([x for x in a2]) + end
            return temp3


        template3(t3_src, t2_src)


        # Templates 4, 5 and 6


        def get_ngrams_for_template4():
            jjr = []
            for i in docs:
                for token in i:
                    if token.dep_ == "ccomp" and token.tag_ == "VBP":
                        if i[token.i+1].tag_ == "JJR" and i[token.i+1].text != "more":
                            jjr.append(str(i[token.i+1]).lower())
            jjs = []
            for i in docs:
                for token in i:
                    if token.dep_ == "det":
                        if i[token.i+1].tag_ == "JJS" and i[token.i+1].text != "most":
                            jjs.append(str(i[token.i+1]).lower())
            jj = []
            for i in docs:
                for token in i:
                    if token.dep_ == "advmod" and token.tag_ == "RBR":
                        if i[token.i+1].tag_ == "JJ" and i[token.i+1].text != "more":
                            jj.append(str(i[token.i+1]).lower())
            jj1 = set(jj)
            jj = list(jj1)
            
            jjr1 = set(jjr)
            jjr1.remove("less")
            jjr = list(jjr1)
            
            jjs1 = set(jjs)
            jjs = list(jjs1)
            return jj, jjr, jjs

        t4_src, t5_src, t6_src = get_ngrams_for_template4()

        def template4(source):
            
            jj = random.choice(source)
            jj1 = random.choice(source)
            
            
            start = "I think the only difference between me and other candidates is that I'm more "
            mid = " and more "
            end = ". - Donald (the bot) Trump"
            
            temp4 = start + jj + mid + jj1 + end
            return temp4


        def template5(source):
            jjr = random.choice(source)
            jjr1 = random.choice(source)
            
            start = "I think the only difference between me and other candidates is that I'm "
            mid = " and "
            end = ". - Donald (the bot) Trump"
            
            temp5 = start + jjr + mid + jjr1 + end
            return temp5

        def template6(source):
            jjs = random.choice(source)
            start = "I am NOT a shmuck. I am the "
            end = " there is. - Donald (the bot) Trump"
            
            temp6 = start + jjs + end
            return temp6


        template4(t4_src)


        template5(t5_src)


        template6(t6_src)


        # Template 7


        def get_ngrams_for_temp7():
            obj = []
            for i in docs:
                get_dependencies(i, obj, dep1 = "det", dep2 = "dobj")
            return obj

        t7_src = get_ngrams_for_temp7()

        def template7(source):
            
            o = random.choice(source)
            
            start = "I would say I'm the all-time judge of "
            end = ". - Donald (the bot) Trump"
            
            temp7 = start + " ".join([x for x in o]) + end
            return temp7

        template7(t7_src)


        # ## FINAL FUNCTION - randomizez the template


        functions = [template1(t1_src), template2(t2_src), template3(t3_src, t2_src), 
                    template4(t4_src), template5(t5_src), template6(t6_src), template7(t7_src)]


        def temp_output(funcs):
            """choose at random from a list of the template functions"""
            f = random.choice(funcs)
            return f
            

                

        # create Meme-obj with the response generated from Quote.reponse
        output = temp_output(functions)
        meme = Meme(output)
        filename = meme.save()  # meme.save() returns the name of the saved image

        return filename


if __name__ == "__main__":
    response = Quote.quote("This is just a test-string")
    meme = Meme(response)
    meme.display()