---
layout: post
title:  "Responsible AI in an Irresponsible World"
date:   2025-10-21 00:20:00 -0500
categories: general
---

# Yeah.  It has been a while.

## Intro

Responsible AI, as I have been thinking of it, is made up of 6 pillars:

- Fairness / Bias
- Reliability / Safety
- Privacy / Security
- Inclusiveness
- Transparency
- Accountability

Originally, I was going make this about all of the above, but let's focus in something a bit more specific: Accountability. Typically, when I think of Accountability in RAI, I tend to think of "Making people accountable for AI".  And, that is definitely part of that pillar.  I seem to be reading more and more about sustainability and how it is also part of accountability.  Now, a TON of discussion and papers have been written about the sustainability aspects of training large language models.  This series from MIT is particularly informative:  

But, I believe that sustainability concerns (and frankly business concerns) don't end there.  I would like to explore two specific examples of how sustainability can play a role in GenAI at inference time.

## Simple Example 1.  Regression

I recently wrote a Jupyter notebook that did a comparison between using the deterministic approach to linear regression vs using an LLM.  Now, you may be thinking something along the lines of "That is just crazy!"  ...and you'd be correct.  I was curious, however, just how "crazy it was."  My experiment involved creating 1000 points that were normally distributed around a line.  I wanted to see just how much difference there would be in computation time between using a Scipy based algorithm vs using an LLM (OpenAI O3).  For this experiment, I went with GPT5.  One of the first problems that I ran into was dealing with getting all 1000 points stuffed into the LLM input tokens, so just to make things more simple, I decided to narrow down the problem to using 10 points.  My prompt was, basically, "Please use linear regression to determine the best fit line through the following set of points [(-3.00, -2.412), ...]".  The results were so lopsided that I then decided to handicap the Scipy approach and force it to use all 1000 points.  The following graph shows the different between the Scipy model and the LLM for accuracy and computation time. 



So, the LLM approach was actually 58950 slower than the Scipy approach!  I knew that it would be bad, but I didn't anticipate just HOW bad.  (I should note here that some of the LLM compute time was clearly spent sending the data back and forth to Azure OpenAI Foundry.  However, since there is no real option to run O3 on a local machine, that is no way around it. 

But, let's consider a second example... doing sentiment analysis on a dataset and see what we come up with...

## Simple Example 2.  Sentiment



## Bottom line.  Do you have to?  

## What next?

Attend my presentation at the Trimble Dimensions Conference in Las Vegas at the Venetian on Nov. 10th.

# Conclusion

Thanks, and see ya' in Vegas?

\- Miles

;)