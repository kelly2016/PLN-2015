# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log2
from random import random
import operator
import time

class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)
        self.corpus = sents
        self.corpus_size = len(self.corpus)

        if self.n > 1:
            sents = list(map((lambda x: ['<s>']*(n-1) + x), sents))


        sents = list(map((lambda x: x+['</s>']),sents))

        for sent in sents:
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1


    #default built-in prob, obsolete now...
    def prob(self, token, prev_tokens=None):
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]
        return self.counts[tuple(tokens)] / float(self.counts[tuple(prev_tokens)])


    ###TODO###

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.
 
        tokens -- the n-gram or (n-1)-gram tuple.
        """
        return self.counts[tokens]


    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
 
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        if not prev_tokens:
            assert self.n == 1
            prev_tokens = tuple()


        hits = self.count((tuple(prev_tokens)+(token,)))
        sub_count = self.count(tuple(prev_tokens))

        return hits / float(sub_count)

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.
 
        sent -- the sentence as a list of tokens.
        """

        prob = 1.0
        sent = ['<s>']*(self.n-1)+sent+['</s>']

        for i in range(self.n-1,len(sent)-self.n+1):
            prob *= self.cond_prob(sent[i],tuple(sent[i-self.n+1:i]))
            if not prob:
                break

        return prob


    def sent_log_prob(self, sent):
        """Log-probability of a sentence.
 
        sent -- the sentence as a list of tokens.
        """

        prob = self.sent_prob(sent)
        if not prob:
            return float('-inf')
        return log2(prob)


class NGramGenerator(object):

    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self.trained_model = model


    def generate_sent(self):
        """Randomly generate a sentence."""
        counter = defaultdict(int)
        sent = ''

        for i in range(0,len(self.trained_model.corpus)):
            counter[self.trained_model.corpus[i][0]]+=1

        return "hoal"

        while not sent[-1]=='.':
            sent+=" "+self.generate_token(tuple(sent.split()[:self.trained_model.n-1]))

        return sent

    def generate_token(self, prev_tokens=None):
        """Randomly generate a token, given prev_tokens.
 
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        p = random()

            
        xs = list(x for x in list(self.trained_model.counts.keys()) if len(x)==self.trained_model.n)
        
        ys = {}
        ys = dict((elem[-1],self.trained_model.cond_prob(elem[-1],prev_tokens)) for elem in xs if self.trained_model.cond_prob(elem[-1],prev_tokens)>0)
        ys = sorted(ys.items(),key=operator.itemgetter(1),reverse=True)


        acc = ys[0][1]
        for i in range(0,len(ys)):
            if p < acc:
                res = ys[i][0]
                break
            else:
                acc += ys[i][1]

        return res



#LET'S DO SOME TESTING!

#from nltk.corpus import PlaintextCorpusReader


#sents = PlaintextCorpusReader('scripts/','shakespeare_no_signs.txt').sents()
#print("\r\ngenerando modelo 1-grama\r\n")
#t0 = time.time()
#model1gram=NGram(1, sents)
#print(time.time() - t0)
#print("\r\ngenerando modelo 2-grama\r\n")
#t0 = time.time()
#model2gram=NGram(2, sents)
#print(time.time() -t0)
#print("\r\ngenerando modelo 3-grama\r\n")
#t0=time.time()
#model3gram=NGram(3, sents)
#print(time.time() -t0)
#print("\r\ngenerando modelo 4-grama\r\n")
#t0 = time.time()
#model4gram=NGram(4, sents)
#print(time.time()-t0)


#trained1gram=NGramGenerator(model1gram)
#trained2gram=NGramGenerator(model2gram)
#trained3gram=NGramGenerator(model3gram)
#trained4gram=NGramGenerator(model4gram)

#print("\r\nGeneración de tokens con modelo entrenado de 1-grama:\r\n")
#fc = defaultdict(int)
#for i in range(0,100):
#    fc[trained1gram.generate_token()]+=1

#print (fc)
