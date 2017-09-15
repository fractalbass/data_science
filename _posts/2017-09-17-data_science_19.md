---
layout: post
title:  Group Think - Boosting Trees
date:   2017-09-14 00:09:00 -0500
categories: general
---


# Introduction

Are two heads better than one?  What about three?  Four?

What if the heads are not very smart?

In 2000, Alan Blinder and John Morgan of the National Bureau of Economic Research authored a paper on the subject titled ["Are Two Heads Better Than One, An Experimental Analysis of Group vs. Individual Decisionmaking](https://www.princeton.edu/~blinder/papers/00NBER7909.pdf).  They summed up their results as follows:

>* Do groups reach decisions more slowly than individuals? According to
these experimental results, what seemingly everyone believes (including the
authors, prior to this study) is simply not true: Groups appear to be no slower in
reaching decisions than individuals are.
* Do groups make better decisions than individuals? The experimental
answer seems to be yes. And the margin of superiority of group over individual
decisions is astonishingly similar in the two experiments--about 3 1/2%.

In the past I have written posts about using [ensemble approaches to data analysis](http://datascience.netlify.com/general/2017/08/15/data_science_15.html).  One of the most popular techniques that has been developed over the past two decades is Boosting Trees(1).  

In this post, I will explore using boosting techniques on various data sets.  

> Note:  There are several great post on this subject including [this one](http://blog.kaggle.com/2017/01/23/a-kaggle-master-explains-gradient-boosting/) by Ben Gorman.  In his blog Gorman writes that this topic has "...been butchered to death by a host of drive-by data scientists’ blogs."  I bristle at the word choices he makes in that statement, but I get his point.  I hope that my blog is NOT the kind of blog he is referring to.  If anyone out there feels it is, please reach out to me with your comments and suggestions.  I can be reached by email at the address at the bottom of this posting.  Even if you disagree with my grammar.  Come on people...

![Throw Me a Bone Here]({{ site.url }}/images/throw-me-a-bone-here.jpeg)

# Boosting Trees

In a boosting algorithm, the final classifier is made up of the weighted sum of a number of "weak classifiers".  You could say that it is like using a whole bunch of "not very smart heads" to come up with a smart decision.   

![boosting scheme]({{ site.url }}/images/adaboost_scheme.png)

(Note: The above formula is taken from [this document by Trevor Hastie of Standford Univ.](http://jessica2.msri.org/attachments/10778/10778-boost.pdf) It is identical to the one used in "The Elements of Statistical Learning", except for a variable name change.)

As the algorithm is built up, each successive classifier is forced to concentrate on the training observations that are missed by the previous classifier in the sequence(2).

[This site](http://arogozhnikov.github.io/2016/06/24/gradient_boosting_explained.html) provides some very nice visualizers to see how boosting working in smaller (three dimensional) data sets.

# Parker "Nappytimes"

To satisfy my own curiosity about this subject, I decided to see if I could verify that boosting does perform better over a given set of data.  The boosting algorithm works well when the data that is being classified (or regressed over) is non-linear in nature.  In order to achieve that goal, I turned to my cat Parker for assistance.  In their book, Hastie, Tibshirani and Friedman take a similar approach, but use a chi-squared random variable with 10 degrees of freedom and a Gaussian (Standard Normal) distribution.  I think that is cool, but very tough to visualize.  My approach uses only 3 dimensions.

To work on this data, I am returning to my trusty cat Parker.

![Parker again.]({{ site.url }}/images/parker_again.png)

I have created some data that represents the amount of time (minutes) Parker spends sleeping during the day; his "NappyTime".  The columns Sunshine and Night_Activity represent the total number of minutes of direct sunlight for that day and the number of minutes of activity that Parker had the night before.  Parker likes to take naps in the sunshine, and he will nap more if he was busy the previous night. 

```text
Day	Sunshine	Nite_Activity		NappyTimes1	0		0			752	0		100			3173	0		200			526...34	500		300			59035	500		400			55036	500		500			650 
```

If the data looks suspicious, that is because it is.  I generated the data with a function that looks like this:

N=INT(526+(((16 * (S - 320)) * (A - 320)^2)/1000000) + (RND()*100))

Where S is the amount of sunshine and A is the amount of previous night activity. INT returns only the integer part of the value and RND is a function that returns a random value between 0 and 1.

The data I generated can be visualized as a 3D surface:

![Parker Nappytimes]({{ site.url }}/images/Parker_Nappytimes.png)

In order to compare the data effectiveness, I wrote a python program that trains two models, a random forest and a boosting tree, to predict the number of minutes of sleep based on the data above.

Here are the results:

```python
Random Forest Relative Feature Importance:
100.0: Nite_Activity
91.81237501188771: Sunshine
Random Forest Accuracy (MSE) 7992.2222


Gradient Boost Relative Feature Importance:
93.59823608398438: Sunshine
100.0: Nite_Activity
Gradient Boost Accuracy (MSE) 5126.7367
```

We can see that the boosted tree model does significantly better than the Random Forest.  

Note:  The code for this blog post can be found on [github](https://github.com/fractalbass/gradient_boost).

# Something a bit more real...

[Kaggle.com](https://www.kaggle.com/dalpozz/creditcardfraud) has a data set that consists of over 280,000 anonymized European credit card transactions that have been categorized as authentic or fraudulent.

I created a program (creditcard\_fraud\_analyzer.py in the repo above) that does a comparison between a random forest model and a gradient boost classifier on the credit card data.  The goal of the model is to predict if a charge was fraudulent or real based on 20+ parameters in the table.  The program uses the standard sklearn random forest model and a python implementation of [XGBoost](http://xgboost.readthedocs.io/en/latest/).   

One of the most immediate things that I noticed about XGBoost is the large number of parameters that are available for tuning the model.

I ran the program once without tuning any of the parameters for the XGBoost classifier and got the following results:

<pre>
                 Results
--------- Random Forest Technique --------- 
Total Patterns=142404	Total Correct=142320

Score:0.9994101289289626

Elapsed time 0:00:53.224784

--------- Gradient Boost Technique --------- 
Total Patterns=142404	Total Correct=142325	
Score=0.9994452403022387

Elapsed time: 0:00:39.441435 
</pre>

Without any tuning, the XGBoost method correctly classified 5 records more than the random forest.  Considering that there were over 280,000 records in the data set, that is not really significant.

After playing with the tuning parameters a bit, I was able to get the program to return the following results:

<pre>
                 Results
--------- Random Forest Technique --------- 
Total Patterns=142404	Total Correct=142320 Score:0.9994101289289626
Elapsed time 0:00:52.425519


--------- Gradient Boost Technique --------- 
Total Patterns=142404	Total Correct=142326 Score=0.9994522625768939
Elapsed time: 0:01:54.226688
</pre>

Ultimately, I was able to improve the gradient boost results by one record.  Unfortunately, that also increased the overall execution time of the run by over a minute.  I managed to make the model perform much worse in terms of results and execution time when I was playing with the parameters.  (I'd use the term tuning, but that would imply that I have a much deeper understanding of all the parameters than is the case right now.)  To get a sense of how complicated XGBoost can be, [check out the docs on the tuning "knobs".](https://xgboost.readthedocs.io/en/latest//parameter.html)

XGBoost has become very popular as a tool for data categorization and prediction, but it is not a trivial tool.  About the only parameter you CAN change in a random forest is the number of trees.  XGBoost is a very different beast.

# Conclusions

Some of the techniques that I have attempted in this series of blog posts have been easy, and others not so much.  This one definitely falls on the more difficult side.  I leave this topic knowing much more than I did about gradient boosting, and much more confused about the parameters associated with the approach.  I settled on the credit card example after looking for various other data sets including ones related to baseball, soccer and revisiting the Titanic data.  In the end, it appeared to me that the gradient boosting methods work quite well when classifying data into a relatively small number of classes.  When I looked at the baseball data, and attempted to use gradient boosting with regression rather than classification, I got some pretty awful results.

This is definitely a topic that I will want to revisit in future posts.  It has also highlighted for me a couple of other techniques that I think I need to look into including bagging.  Look for that post soon.

I hope you have enjoyed this post.  If you have comments or questions, please feel free to reach out.

Miles.

# References

1.  Hastie, Trevor, Tibshirani, Robert and Friedman, Jerome.  "The Elements of Statistical Learning, Data Mining, Inference, and Prediction" Springer 2009.  ISBN: 978-0-378-84857-0.  Page 337.

2.  Hastie, Tibshirani and Friedman. Pg 338-339