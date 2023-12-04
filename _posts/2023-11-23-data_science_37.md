---
layout: post
title:  "Something Random"
date:   2023-11-23 00:09:00 -0800
categories: general
---
 
# Let's talk about some random stuff.

Recently, I came across a (very short) book by Andy Weir called Randomize.  You can [get if for free from Amazon](https://www.amazon.com/Randomize-Forward-collection-Andy-Weir-ebook/dp/B07VDJBKNJ).  I won't spoil it for you, but a main theme in the book is random numbers... or really the illusion of random numbers when it comes to computers.  

When I was reading this book (short story might be a better description), it occurred to me that inifinity is to calculus what randomness is to statistics and probability.  And, just like in Calculus and mathematical analysis where we have different kinds of infinity (countable vs uncountable), there are also different kinds of random numbers.  Here, I am thinking of distributions of random numbers.  When we talk about random numbers we usually think in terms of the so-called uniform distribution.  However, many random distributions exist.

# Not all random is the same.

Statistics, which is the study of the properties of samples and using that information to make statements about populations, is filled with the concept of collecting random samples.  When people say "pick a random number between 1 and 10", what they typically mean is to pick a number between 1 and 10 where each number has the same chance of being chosen.  It turns out that there are other ways to pick random numbers, however.  Consider this small change to the "pick a number between 1 and 10"...

Pick 5 random numbers between 1 and 10, and compute their average.  Now do that over and over again 100 times.  If I pick 5 random numbers, and take their average, clearly that answer is going to be random.  However... it is a special kind of random when I look at the 100 results of the above experiment.  What we are touching on here is the idea of distribution of random numbers.  If I say pick a random number between 1 and 10, that is called a "uniform" distribution.  However, when I look at the means, I am starting to approximate a different kind of random distribution called a "normal distribution".  There are many other kinds of random distributions.

todo:  Distribution Graphic.

# Stochastic vs Deterministic

Random numbers underly the concept of stochastic models and optimization.  Random, or "stochastic" models stand in contrast to what is often referred to as "deterministic" models, which use a direct approach.  To understand the difference, consider two methods for estimating PI.  The method that Archimedes used, which involves [transcribing triangles inside of a circle](https://arxiv.org/pdf/2008.07995.pdf) would be considered deterministic.  In the Archimedes algorithm, you don't need any kind of randomness to do the calculations.

In contrast, the so-called "Monte Carlo" involves randomly adding dots to a square with a circle enclosed inside.  This approach is considered stochastic as it requires the use of random numbers for the simulation to work.

[Similar techniques were used by John von Neumann and Stanislaw Ulam to solve problems related to radiation while working on the Manhattan project](https://bookdown.org/manuele_leonelli/SimBook/a-bit-of-history.html)

## Good Random vs Bad Random

When we think about using random numbers, we are quickly faced with a bit of a contradiction.  For the purposes of security, good random number should not be predictable, and should not be repeatable.  At the same time, many stochastic algorithms currently used would not be repeatable if they relied on truly random numbers.  And, without repeatability, algorithms that use stochastic processes would be very difficult to test, and results would be impossible to confirm.

For the sake of argument, let's consider that good random numbers are those that are independent, and identically distributed.  Furthermore, do NOT posess any kind of hidden pattern.  Digital computers are deterministic machines.  A computer needs to either rely on an external aparatus for generating random numbers.   [https://www.cloudflare.com/learning/ssl/lava-lamp-encryption/](Some of which have been fairly elaborate.)  Or, computers use  rely on algorithms called pseudo-random numbers generators, often called PRNGs.

Historically, some PRNGs have been better than others.  An interesting example of a once highly regarded PRNG was developed by IBM in the late 1960s.  This PRNG used a formula 

$$ V_{j+1} = V_j mod 2^{31} $$

Known as a linear congruential pseudorandom number generator or LCG, the above sequence provides seemingly random numbers as snown below.

![Randu]({{ site.url }}/images/randu.png)

However, to see the weekness or RANDU, one needs to simply consider each three consecutive values as coordinates in 3 dimensional space, and plot those values.  The following animation shows the obivous issue RANDU has.

![Randu]({{ site.url }}/images/randu.webm)

## Randomness and Regression

Randomness and particularly normal random variables play an important role in regression, particularly when it comes to goodness of fit.  Simple linear regression can be thought of as a best fit line thru a collection of datapoints.

![Regression]({{ site.url }}/images/regression1.png)

When we do a regression, one of the things that we pay special attention to is the difference between the original datapoints that we are trying to fit a line thru, and the difference between those points and the best fit line.  These differences are referred to as the "residuals".  When we do regression, we make the assumption that the residuals are randomly distributed according a normal distribution.  It is important that each residual is independent from the others, and that all the residuals follow this same distribution.  If this happens, and it frequently does, we can then use statistics to provide useful information include how much we can realy on the line that we fit, as well as do interesting things like build confidence intervals for our regression line.

![Residual Histogram]({{ site.url }}/images/residuals1.png)

## Sometimes, things are just random.

At Georgia Tech, I took a class on business analytics.  It was an iteresting, of not a bit scattered course, that covered aspects of finance, digital marketing, and a number of other topics.  One of the best things about the class was the book... that we never used.  (Not sure why.)  The book was “Data Mining for Business Analytics”.  ISBN:  978-1-118-87936-8 by Shmueli, Bruce, Yahav, Patel, Lichtendahl.   

Towards the end of the book, there was this great quote...  “Before attempting to forecast a time series, it is important to determine whether it is predictable, in the sense that its past can be used to predict its future beyond the naive forecast.”

In other words, sometimes things are just random based on what you know.  DON'T WASTE TIME TRYING TO PREDICT THEM!

A time series that follows a random patern is often referred to as a "random walk".  It turns out that there is a really easy technique to determine if a time series is a random walk, which involves fitting an AR(1} model.  An AR(1) model is simply a regression model where each term in the sequence is regressed back on the previous term.  Or... just take all the pairs in the time series defined by

$$ (X_n, X_{n-1}) $$

Now, plot those values and fit a line.  If the slope of the regression line is 1... meaning that the best guess for the any number in the sequence is just the number before it, we have shown that the sequence is a random walk.  Since this is a regression model under the hood, we can also look at the P-value for the coefficient in the underlying mode to get a sense of how reliable that coefficient is.  Here is an interesting example.  Here, I have taken the daily closing values of a company's stock (it happens to be Trimble, my current employer) from Jan 1, 2021 thru Oct 10, 2023.

![Trimble image 1]({{ site.url }}/images/trimble_walk_1.png)

Next, using the R programming language, I have fit an ARIMA(1,0,0) model (aka AR(1) as mentioned above) to the data.  

![Trimble image 1]({{ site.url }}/images/trimble_walk_1.png)

As illustrated above, the coefficient is really close to 1.  Continuing on to check the statistical reliability of the coefficient in the model, the P-value is nearly zero.  This means that the coefficient is highly reliable and we are looking at a random walk.

![Trimble image 2]({{ site.url }}/images/trimble_walk_2.png)

The bottom line here is that we have shown the stock above to be an essentially unpredictable random walk, and any efforts to fit a model based on JUST THIS DATA is not going to work.  Now, that does not necessarily mean that we couldn't find a different model with different predictor variables.  It just means that the sequence itself is not enough to go on when trying to do predictions.  

## Conclusion

So, the takeaways from this post are:

1.  Random is to stats what infinity is to calculus.
2.  There are good random (estimate pi and lava lamps) and bad random RANDU.
3.  There are different kinds of random (distributions).
4.  Randomness underlies our ability to state the statistical significance and confidence intervals of regression.
5.  Some stuff is just random, so don't waste your time trying to predict it.

I hope you have enjoyed this long overdue post.  I wish everyone a wonderful holiday season, and a happy new year!


