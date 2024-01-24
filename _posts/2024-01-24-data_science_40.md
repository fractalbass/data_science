---
layout: post
title:  "Mama Said There'd be Days Like This"
date:   2024-01-24 00:09:00 -0800
categories: general
---

# Experimentation Means Failure?

In the movie The Princess Bride there is a scene with Inigo and Dread Pirate Roberts having a sword fight on the Cliffs of Insanity. Inigo presses Roberts to remove his mask and reveal his identity.  When Inigo says, "I must know," Westley replies, "Get used to disappointment."

This is a great metaphor for working in data science.  If you really are doing data science, then you need to "Get used to disappointment."

# ROC and AUC

These three letter acronyms are important, particularly in the context of building classification models.  ROC or Receiver Operating Characteristic is a graph that shows the impact of threshold values on a binary classifier.  Area Under Curve, also often referred to as "lift", corresponds to the improvement that a model has over using a naive guess for the classification.  Any value of AUC that is below .5 shows that your model is actually WORSE that a random guess.  

Yes.  It happens.

![Bad AUC]({{ site.url }}/images/bad_auc.png)

This is an actual AUC from a project that I am working on.  

Yes.  I trained a binary classifier that is actually "dumber than dumb."

# The Point

Thomas Edison [once said](https://www.smithsonianmag.com/innovation/7-epic-fails-brought-to-you-by-the-genius-mind-of-thomas-edison-180947786/) 

> “I have not failed 10,000 times—I’ve successfully found 10,000 ways that will not work.”

"Finding ways that will not work" is part of experimentation.  It is a critical part of all science, it is how we find insights, and how we learn.

That is all for this extremely short blog post.  Carry on and keep finding ways that will not work!

- Miles

;)