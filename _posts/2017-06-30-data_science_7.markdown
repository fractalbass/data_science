---
layout: post
title:  "Bayesian Inference Part 2: Data Science, Its Yuge!"
date:   2017-06-30 00:08:00 -0500
categories: general
---
# Bayesian Inference Part 2: Data Science, It's Yuge!


![Yuge Data]({{ site.url }}/images/its_yuge.jpg)

## Introduction

In this post I will look at using some Bayesian techniques to analyze President Trump's posts to twitter over time.  Trump's has tweeted over 32,000 times since 2009.  The data provides an excellent source of raw material for bayesian techniques.

First, however, we will take a step back and review some of the basics of Bayesian Inference.
   
## Gentle Introduction to Bayesian Inference.

The classic example used in the introduction to Bayesian Inference is to consider flipping a coin.  If we assume for a moment that we don't know that the probability of flipping a coin is 50% heads and 50% tails.  To figure out what the probability was, we might decide to actually run an experiment and flip a coin to see.  

Lets say our experiment went like this:

| Attempt       | Result       
| ------------- |:-------------:|
|1|tails|
|2|heads|
|3|tails|
|4|tails|
|5|tails|
|6|heads|
|7|tails|
|8|heads|
|9|heads|
|10|tails|

Based on our experiment, we would see that we got 4 heads and 6 tails.  The more times we flip our coin, we would start to see our percentages start to converge.  Here we can start to see that the probability is somewhere around 0.5.  If we repeat the experiment and flip the coin 100 times, we would see that 40/60% split start to get closer to 50/50%.  The idea of repeating the experiment multiple times, and updating beliefs is central to Bayesian thinking. 

At the center of Bayesian this approach mathematically is Bayes Theorem, which looks like this:

![Bayes Theorem]({{ site.url }}/images/bayes_theorem.png)

A great explanation of the Bayesian Inference can also be found at [http://nbviewer.jupyter.org/github/psinger/notebooks/blob/master/bayesian_inference.ipynb]()

I want to stress one important aspect of Bayesian thinking.  As we increase the number of trials, the probability density function starts to get very narrow.  This means that as the number of number of experiments (trials) increases, we be come increasingly confident in the range for the probability of our coin flip.  We will never by absolutely certain of the underlying probability but we can become increasing confident.  Let's see what this looks like in terms of confidence intervals.  (Note: These confidence intervals were 
The confidence interval for 10 flips...

![Bayesian Coin Flip]({{ site.url }}/images/coin_flip_10_ci.png)

The confidence interval for 100 flips...

![Bayesian Coin Flip]({{ site.url }}/images/coin_flip_100_ci.png)

The confidence interval for 1000 flips...

![Bayesian Coin Flip]({{ site.url }}/images/coin_flip_1000_ci.png)

Note:  The code for the above graphs can be found in the git repo: [https://github.com/fractalbass/bayesian_trump]()

# What does this have to do with @realDonaldTrump, or vice versa?

As I mentioned in the introduction, President Trump is a great source for raw twitter data.  His 32000+ tweets going back to 2009 provide a great data set for trying out some Bayesian techniques.  The first challenge in dealing with those tweets, is how to get ahold of them, however...

## Obtaining the data

The repo [https://github.com/mkearney/trumptweets]() has instructions for how to download all of the Trump tweets using R.  I particularly enjoyed this part...

<pre>
> ## run function to download Trump's twitter archive
> djt <- trumptweets()
    Downloading 31157 tweets...
    You're halfway there...
    Huzzah!!!
</pre>

Using the above program, we can download the tweets and put them into a .CSV file and then switch back to python for the rest of our analytic tasks.  In addition to just analyzing the frequency of trumps tweets, I also have some interest in seeing how these tweets have changed tone over time.  One way to do that is the Natural Language Tool Kit, or NLTK as it is commonly referred to.  In the [git repo]([https://github.com/fractalbass/bayesian_trump]()) associated with this blog post is a python class and test that I created to encapsulate using NLTK to assess the positive or negative sentiment of each Trump tweet.  The code leverages Bayesian techniques to train a classifier based on a set of known data, or corpus.  Below is the basic test for the SentimentAnalyzer class, followed the class itself. 

<pre>

import unittest
import SentimentAnalyzer as analyzer


class SentimentAnalyzerTest(unittest.TestCase):

    def test_analyze_sentiment(self):

        sa = analyzer.SentimentAnalyzer()

        self.assertTrue(sa.analyze_sentiment("This is a happy tweet.  Have a nice day.")=="pos")
        self.assertTrue(sa.analyze_sentiment("I am angry.  He is very disonest.  Sad.")=="neg")
</pre>

And the class...

<pre>
# --------------------------------------------------------------
#  By Miles R. Porter
#  Painted Harmony Group, Inc
#  June 26, 2017
#  Please See LICENSE.txt
# --------------------------------------------------------------

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.tokenize import TweetTokenizer


class SentimentAnalyzer:

    classifier = None
    tknzr = TweetTokenizer()

    def __init__(self):
        def word_feats(words):
            return dict([(word, True) for word in words])

        negids = movie_reviews.fileids('neg')
        posids = movie_reviews.fileids('pos')

        negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
        posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

        negcutoff = int(len(negfeats))
        poscutoff = int(len(posfeats))

        trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
        # testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
        print('Train based on %d documents.' % (len(trainfeats)))

        self.classifier = NaiveBayesClassifier.train(trainfeats)

    def analyze_sentiment(self, raw_text):
        tokenized_text = [self.tknzr.tokenize(raw_text)]
        txt = dict((t, True) for t in tokenized_text[0])
        results = self.classifier.classify(txt)
        return results
        
</pre>

We can now create a file that contains not only the tweet information, but also an indication of if the tweet was positive or negative.


    

### Analyzing the data

## Conclusion

## More Resources



 