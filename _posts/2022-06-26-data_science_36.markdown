---
layout: post
title:  "Azure ML? Seriously?  Yes.  Seriously!"
date:   2022-06-30 00:09:00 -0800
categories: general
---
 
## Introduction
 
I have been working full time on Data Science since mid 2017 (5 years).  During that time, I have made just about every ML mistake you can think of.  Use training data in the test set?  Yup.  Created a great deep learning model only to loose track of the model file and have to retrain?  Sure.  Tried to retrain a model, but couldn’t re-find the hyperparameters that worked well?  Done that.  Used an open source autoML package… that was based on Java and used Log4J… that was shown to have major security flaws… and then forced to retrain the autoML model again…. Aaand… still cannot remember what the first autoML model settled on?  Yeah.  Ran an inference model on a bare-metal EC2 instance that mostly sat idle, but has to have a boatload of RAM so it is way more expensive that it should be, even if it only “wakes up” part of the time.  Yeah.  Heck, I am not proud, I can even say that I wrote a MONSTER single-threaded-and-super-slow python app that sucks data out of a cloud data service, chugs on it, and then shoves the results back into the cloud data service... from scratch.

So, yeah.  I have made a ton of mistakes.  In December, I completed my MS in Analytics from Georgia Tech.  (See my earlier post.) That program helped me understand what professional analytics is about.  It turned me onto techniques like EDA, simulation, cross-validation, and feature engineering.  I learned and relearned about the math and statistics of why things work, and why they sometimes dont.  My masters courses also helped me learn about behaviors and best practices that help reduce the likelihood of making process and workflow mistakes.  But, even after all that, doing analytics and data science is hard.  Doing it well, is very hard.  

I am so happy that Microsoft has helped make it easier.

Now, if you would have said to me that I would write that line 5 years ago, I would have said you were crazy.  I have used Microsoft products in the past, but it has always been with some reluctance.  I don’t typically run Windows unless I cannot avoid it (I prefer to use Linux, or a Mac.)  Being a certified Novell Network Engineer (CNE… you young kids can just Google that), I never quite got over the fact that Microsoft basically killed that platform.  

But, with all of those good and less than good reasons, I ended up having to use Azure ML.  I must say that Microsoft does a very nice job of Machine Learning Platform as a Service.  Add to that how far Azure has come...  Well, if you working in Analytics or Data Science, it might be well worth your time to check out the platform.  And… you can try it out for free!  

Still need to be convinced why MS has developed a winning solution for analytics?  Ok.  I respect that.  Let me offer a few details to consider.  I'll break this down relative to how I tend to thing of analytics...

Data
Exploratory Analysis
Experiments
Modeling (AutoML, GUI Driven, Notebook Driven, Deep Learning)
Modeling based on massive data
Model Management
Model Deployment and...
Data

# Data

Let's start with Data.  As you can see above, I believe that data science and analytics literally begins and ends with data.  It is really crazy to me, then, how so many data science platforms don't really do data justice.  Azure ML has this covered by seamlessly integrating data into the ML environment.  What environment, you ask?  That environment is the Azure ML Studio.  If you are not familiar with Azure, and are with AWS (as I was) it works in sort of the same paradigm.  Azure has a TON of services that they offer through their portal.  Azure ML Studio makes using the various services involved in Azure ML easy.  When uploading data into Azure ML, you can save the data a number of ways.  However, the ML Studio makes it seamlessly easy to use.  The other thing that I like is that you can VERSION data sets.  Knowing what DATA you used to train a model is critical.  Change the training data, and of course you are going to change the model.  This is something that I don't think is addressed enough.  Sure, it is important to know your model hyperparameters... but what DATA did you use to train the model is an equally important question.

# Exploratory Analysis

Once you have data, a lot can be done just by looking at it.  This is something that was really stressed in several of my masters classes, and I agree.  Don't just assume that your data file is correct.  ACTUALLY LOOK AT IT.  This is easy in Azure ML Studio.  If you've imported the data, you can simply view the data.  You can also generate a dataset profile, which will provide some nice basics descriptive statistics for your data set.

# Modeling Training

Once you have understood your data, you will eventually want to start building some models.  Azure ML Studio uses the Jupyter notebook paradigm.  You can mix code and documentation in these notebooks as you would expect.

# Experiments



# Modeling Training with MASSIVE data

# Model Management

# Model Deployment

# (And it all comes back to) DATA

# Conclusion


