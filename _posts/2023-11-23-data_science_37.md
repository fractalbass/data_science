---
layout: post
title:  "Something Random"
date:   2023-11-23 00:09:00 -0800
categories: general
---
 
# Let's talk about some random stuff.

Recently, I came across a (very short) book by Andy Weir called Randomize.  You can [get if for free from Amazon](https://www.amazon.com/Randomize-Forward-collection-Andy-Weir-ebook/dp/B07VDJBKNJ).  I won't spoil it for you, but a main theme in the book is random numbers... or really the illusion of random numbers when it comes to computers.  It is a common beliefe that computers, being digital machines, are incapabile of creating true random numbers.  This is, for the most part true, however there are some [external devices that can do the trick](https://www.amazon.com/TrueRNG-V3-Hardware-Random-Generator/dp/B01KR2JHTA).

Random numbers and randomness are critical to the fields of probability and statistics, and underly the concept of stochastic models and optimization.  Random, or "stochastic" models stand in contrast to what is often referred to as "deterministic" models, which use a direct approach.  To understand the difference, consider two methods for estimating PI.  The method that Archimedes used, which involves [transcribing triangles inside of a circle](https://arxiv.org/pdf/2008.07995.pdf) would be considered deterministic.  In the Archimedes algorithm, you don't need any kind of randomness to do the calculations.

In contrast, the so-called "Monte Carlo" [approach for estimating Pi developed by John von Neumann and Stanislaw Ulam while working on the Manhattan project](https://sites.google.com/a/vt.edu/monte-carlo-simulation/history) involves randomly adding dots to a square with a circle enclosed inside.  This approach is considered stochastic as it requires the use of random numbers for the simulation to work.

In the field of analytics, we often rely on randomness (or the assumption of randomness) as we come up with estimates.  However, randomness can also provide huge challenges.  Things that are truly random are, by definition NOT predictable.  The problem that is often faced by data scientists is to try and predict things that are really not predictable.  We will come back to this later.

One of the most important things to understand is that not all "randomness" is the same.  This is probably best understood from the perspective of statistics.  Stats, which is the study of the properties of samples, and using that information to make statements about populations, is filled with the concept of collecting random samples.  When people say "pick a random number between 1 and 10", what they typically mean is to pick a number between 1 and 10 where each number has the same chance of being chosen.  It turns out that there are other ways to pick random numbers, however.  Consider this small change to the "pick a number between 1 and 10"...

Pick 5 random numbers between 1 and 10, and compute their average.  Now do that over and over again 100 times.  If I pick 5 random numbers, and take their average, clearly that answer is going to be random.  However... it is a special kind of random when I look at the 100 results of the above experiment.  What we are touching on here is the idea of distribution of random numbers.  If I say pick a random number between 1 and 10, that is called a "uniform" distribution.  However, when I look at the means, I am starting to approximate a different kind of random distribution called a "normal distribution".  The "normal" distribution can be generated based on a uniform distribution, as we have seen... but only if we have a really good uniform distribution.

So...  How do we do that in computers?