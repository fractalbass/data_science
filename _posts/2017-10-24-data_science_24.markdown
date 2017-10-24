---
layout: post
title:  What is a p-value?
date:   2017-10-24 00:12:00 -0500
categories: general
---

# Introduction

![stats_binomial]({{ site.url }}/images/p-value.png)

At a recent A.I. meet-up in the Twin Cities, I found myself talking to a couple of other folks.  I made a statement about how so many people mess up the concept of a confidence interval.  [See this post for more details](http://datascience.netlify.com/general/2017/09/06/data_science_16.html).  One of the individuals mentioned that when he interviews potential candidates for positions, he often likes to ask them about what their definition of a p-value is.  I assumed that the p-value he was talking about was the one that I am familiar with from Bayesian techniques ([see this post](http://datascience.netlify.com/general/2017/06/27/data_science_6.html)) where p(A) is the probability of event A occurring.  

I knew that couldn't be it, and so I sheepishly looked at my shoes.  Not one to walk away from not knowing the answer to something that I should, this post is MY "mea culpa".  So, without further ado, lets explore the concept of a p-value.   

#  Probability and Statistics

I think of probability as going from a known population and making statements about the likely makeup of samples.  For instance, you have a bag with 25 green and 37 red M&Ms.  Probability provides tools for answering questions like "How many red and green M&Ms are you likely to have if you pick out 4 at random.

I think of statistics as going from a sample and making statements about a population.  Statistics also allows us to test hypothesis about a population from sampled values.  It is in this type of a statistics problem that we encounter p-values.

Let's look at an example:

# Six Sided Die Problem

Let's say that I have a 6 sided die.  Is this die fair if I get 4 sixes when I role the die a total of 36 times?

This is a binomial distribution problem and can be written as so:

> X ~ B(36,p)  

or  "The distribution X is a Binomial Distribution with 36 trials and a probability of p."  This is a binomial problem because there are two cases: that I rolled a die and got a 6, or I didn't get a six.

In our problem above, if our hypothesis is that the die is fair we would expect P to be 1/6.  We call this the Null Hypothesis or H<sub>0</sub>.

> H<sub>0</sub> : P = 1/6

There are two alternative hypothesis that represent the fact that the die is not fair.  Based on my data, I am only concerned about the lower tail.  Remember that in my test, I rolled the die 36 times, and I got 4 sixes.  So, my alternative hypothesis is:

> H<sub>1</sub> : P < 1/6

In order to test this, we need one other piece of information.  That information is the significance level of my test.  In this case, we will use a 5% level of significance.  That value is often referred to as the alpha value or ⍺.       

So, we will reject our H<sub>0</sub> if:

> Reject H<sub>0</sub> if P(x<=4 | x~B(36,1/6)) <= 0.05

In this case, I can use this [handy calculator](http://stattrek.com/online-calculator/binomial.aspx) like so...

![stats_binomial]({{ site.url }}/images/stats_binomial.png)

...to come up with the following:

> Reject H<sub>0</sub> if 0.260676511336664 <= 0.05

Since the above is NOT true, I DO NOT reject H<sub>0</sub>  

Based on the above, there is evidence that the die is fair.

# So what is the "p-value"

In the above problem, we may have been tempted to say that the "p-value" was 1/6, or the probability that we assume to be true under the null hypothesis.

But, that is not the classical definition, and is what I believe my colleague was referring to.

The Harper Collins dictionary of mathematics defines a p-value as: "the probability that a given Test Statistic takes either the observed value or one that is less likely under the Null Hypothesis.  If fixed in advance, this is the significance level of the test."  

I prefer the definition from my handy and well worn copy of "Introduction to Probability and Statistics by J.S. Milton and Jesse C. Arnold...

"...the P value is the smallest level at which we could have preset ⍺ and still have been able to reject H<sub>0</sub>."  In this test, that value would have been 0.260676511336664.

# Conclusion

So, there you have it.  Should you run into the p-value question in an interview, you will now have this nice blog post to refer too.  

I hope you have enjoyed this exploration of the basic binomial distribution and p-values.  Stay tuned for more topics in data science and machine learning.