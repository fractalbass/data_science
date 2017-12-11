---
layout: post
title:  "Google Cloud Machine Learning"
date:   2017-12-11 00:09:00 -0500
categories: general
---

# Introduction

![Google Machine Learning!]({{ site.url }}/images/google_ml.png)

I have been spending a bit of time lately working on a Kaggle.com challenge related to voice recognition.  More information about the challenge can be found [on the Kaggle site](https://www.kaggle.com/c/tensorflow-speech-recognition-challenge).  My approach can be found in 

Steps

1. Configure Dev Environment
2. Initiate project
3. What...  Python 2.7 only?!
4. Redo project for Python 2.7
	- Use the python distribution of 2.7.14 and install it on the Mac
	- Use virtualenv to create a virtual environment for python 2.7
	- Install all the required libraries ($> pip install ____) ... 
		- numpy
		- keras
		- tensorflow
		- Pillow
		- h5py
		- using pip install ____
3. Verify that the thing works locally.  Ok.  It works.  So how do I get it up to google?

#  Going through the ML Training demo as a starter.

1.  Enable google cloud stuff, et:  
- Install the google cloud SDK:  https://cloud.google.com/sdk/
- Go through the tutorial https://cloud.google.com/ml-engine/docs/getting-started-training-prediction
## Notes:

 that because I am using zshell, wildcards with paths may not work as expected.  So, it may be necessary to change commands to include single quotes,  eg:  

```text 
gsutil -m cp 'gs://cloudml-public/census/data/*' data/
```
I had some trouble getting tensorboard to work when running the model on the server.  The error I was getting was:

```text
2017-12-06 14:23:43.164730: I tensorflow/core/platform/cloud/retrying_utils.cc:77] The operation failed and will be automatically retried in 1.35008 seconds (attempt 1 out of 10), caused by: Unavailable: Error executing an HTTP request (HTTP response code 0, error code 6, error message 'Couldn't resolve host 'metadata'')
```

Which, to some engineer at google, is a way of saying that my authentication wasn't correct.  (Or is the result of said condition.)  To get around it, I entered the following command based on a StackOverflow questions:

```text
gcloud auth application-default login
```
That enabled tensorboard to start working.

![Tensorboard]({{ site.url }}/images/tensorboard.png)    

# Part 2.  Can I get my model to train up there.

##  First I need to put my training files up there

I first need to copy all of the pre-processed image files to google storage so that I can load them from my script.  To do that, I will use only the 10 image directories need for the kaggle voice challenge problem.  The google console makes this pretty easy.  I logged into the google console, and then created a bucket.  Next, I just uploaded the files I wanted.

The google console provides a mechanism for uploading the files, but because the number of files that I wanted to upload was so large, the browser really had a tough time.  I finally canceled the upload via the browser and use the command line utility.  I had already converted these files from audio format to MFCC files.  The original files are from the [Kaggle Tensorflow Voice Challenge](https://www.kaggle.com/c/tensorflow-speech-recognition-challenge).  

e.g.

```text
gsutil -m cp -r kaggle_10/ gs://kaggle_voice_data
```

I did have some concern about how much this is going to cost, having run this for a day now, I think I am going to be OK.  

![Billing]({{ site.url }}/images/google_billing.png)  

Now that I have the files up there, I turned my attention to trying to run my own machine learning model in the cloud.

## Second I need to put my code up there

The code that I am working with is based on my work around the [Kaggle Tensorflow Voice Challenge](https://www.kaggle.com/c/tensorflow-speech-recognition-challenge).  This challenge involves identifying spoken words in audio files.  My code for this project is in [github.com](https://github.com/fractalbass/kaggle_tf_audio)

One of the things to note about this code is that google, for some crazy reason only supports python 2.7.  This has been the case with google for some time, that they seem to be behind in their support of python versions.  Anyway, it was not to difficult to setup a virtualenv for python 2.7 and modify the code so that it work in that version of python.

After looking at the code that google provided as an example of their machine learning stuff, I attempted to run my code locally in the same way that is mentioned in their tutorial[in their tutorial](https://cloud.google.com/ml-engine/docs/getting-started-training-prediction).  

This uncovered an unfortunate issue.  My code was using the "flow_from_directory" as a way to load the data.  I needed a way to load the data from google cloud storage.  To facilitate that, I modified the way that my trainer worked and added a mechanism to load the training data from google cloud storage.

##  Getting the trainer to run locally.

Before running the code on google cloud machine learning, I first followed the path recommended above with the Census data set.  In that exercise, the code is first run locally to confirm that everything works before it is submitted to the cloud for training there.  After some trial and error, I was able to first get the code to run from the command line as a simple python program, and eventually by using the gcloud command for running the file locally.  Here is what my command looked like:

```bash
gcloud ml-engine local train --package-path trainer --module-name trainer.google_model_trainer --job-dir=$MODEL
```

Where $MODEL is set the local of the google storage bucket that I am using.

Once I go this to work, I tried to run my trainer on the cloud by removing the "local" from the above statement.  It was a long shot...  and it didn't work.  There are several things that need to be done first.

1. The dependencies for my project needed to be declared
2. I needed to remove all of the graphing related code and dependencies.
3. I needed to correctly specify all of the commands required to submit the job to google.

For the first part, I created a setup.py file per [the recommendations of Google quickstart](https://cloud.google.com/ml-engine/docs/packaging-trainer).  My setup.py looks like this:

```python
from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['Keras>=2.1.2', 'scikit-learn>=0.19.1', 'urllib3>=1.22', 'h5py>=2.7.1', 'google-cloud-storage>=1.6.0']

setup(
    name='trainer',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='My trainer application package.'
)
```

For the second point above, I just removed all of the calls to matplotlib, etc.

For the last part, I finally created a bash script to execute the command for me.  That script looks like this:

```bash
#!/bin/bash
if [$1 eq ""]
then
    echo Please include a job name!
else
    rm -rf *.pyc
    rm -rf ./train/*.pyc
    gcloud ml-engine jobs submit training $1 --module-name trainer.google_model_trainer --package-path=trainer --job-dir=gs://kaggle_voice_data
    echo Training started.
fi
```

Getting to that point took me about 10 trial and error attempts.  Finally, however, I got it to work!

![ML Log]({{ site.url }}/images/ml_log.png)  

# Conclusion

As you can see from the last screen grab above, I trained the network twice.  The first time I used trained based on 1000 test images in batch sizes of 32, and over 5 epochs.  That took 00:23:06 in the cloud.  The next run I trained again on 1000 images, and batches of 32, but I let the program run for 50 epochs.  As expected, it took about 10 times as long.  03:52:??.  By comparison, when I ran the same code locally, it took 02:46:00 approximately.  So, the cloud is significantly slower:

![ML Build Times]({{ site.url }}/images/Google_ML_Training_Times.png)

The bad news is that, at least considering the way that my job was configured, it trained considerably slower on the google cloud than it did on my local machine.  

The good news is that by running my build on google, I was free to use my Mac for other things!

The final accuracy of the model was somewhat disappointing...  around 25 percent when I submitted it to Kaggle for evaluation.  However, that is not too surprising due to the fact that I only used 1000 training patterns for each category of word.  I will be running the training again on the complete training set and with 100 epochs to see if I can increase my accuracy.

I will post an update to this blog when I have complete that setup.

I hope you have enjoyed this post on using Google Cloud Machine Learning for training convolutional neural networks that run on Tensor Flow and use the Keras framework.  Stay tuned for more blog posts on topics in machine learning and data science!

In the meantime...  If you happen to have lasted through this entire post, thank you.  I am currently looking for my next gig in data science and/or machine learning.  (FTE, Contract or Contract to Hire).  Please reach to to me at the email address below if you know of any positions or are interested in chatting with me!








