---
layout: post
title:  Now What?!  Serving a Trained Keras/TensorFlow Model
date:   2017-09-25 00:09:00 -0500
categories: general
---

# Introduction

Congratulations!  You have managed to write a deep learning model that actually seems to work!  Now what?  The whole point of this deep learning stuff is to actually cut it loose on some real data, right?  Sometimes, I think, we can spend too much time focusing on the training aspect of our models but overlook the ultimate goal.

![Ship in A Bottle...]({{ site.url }}/images/ship_in_a_bottle.jpg)

One of the things that I dislike about raw TensorFlow is that it is built with, and depends on protocol buffers.  Protobufs are a "favorite child" of the brainy folks at Google.  I have several complaints about protobufs that I won't go into here, except to say that they require code generation and make it harder to troubleshoot issues.  Serving models with the google TensorFlow Server requires the use of protobufs.  There is, however, a much easier way.

Much of the work that I have done with TensorFlow has involved using Keras as a front end to that powerful tool.  TensorFlow itself now includes the Keras library in the core TensorFlow distribution.

In this blog post, I will look at taking a complex image model and using Flask to create a simple server that presents a web endpoint for processing data with a trained Keras model.  And...  Tensorflow will be running under the covers.

#  The Model

The point of this blog post is not to create a model, but rather serve one up.  To move things along, I am going to start with an image processing model that was covered in [this post on the Keras blog](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html).  This is a cool model...  it can tell the difference between images of cats and dogs!  The model is related to this [Kaggle challenge](https://www.kaggle.com/c/dogs-vs-cats).

The data for my is structured in the same way as the above blog post, like so...

![Dogs and cats structure]({{ site.url }}/images/dog_cat_data_structure.png)

Training for the model was done by the main file referenced in the Keras blog post, with one important modification. 

```python
...
# Don't do this...
# model.save_weights('second_try.h5')
# Do this...
model.save('second_try.h5')
...
```
There is more to a model than just the weights, but rather the shape of the model as well.  Saving with "model.save" will include important information on the structure of the model, rather than just the weights.  Also, this doesn't require any protobufs.  We will see in a second how easy it is to re-constitute the model from the saved file.  

I trained the model using the settings in the file from the Keras blog. It took a couple hours, and was only at around 83% accuracy when training wrapped up.  Again, the point of this blog is not to get a perfect model going, but rather just to show how to expose a complex Keras CNN model using Flask.  So...  moving right along...

#  A Little Architecture...

One of the things that I really like to see in system architectures, as well as in application code, is the implementation of the principles of ["Separation of concerns"](https://en.wikipedia.org/wiki/Separation_of_concerns).  SoC is about keeping dislike code, components, etc separate from each other.  Doing so makes the overall system more manageable, and easier to comprehend.  In terms of creating deep learning systems, some examples of SoC would be to separate the model learning/training systems from the prediction/categorization functions.  Also, it would make sense to separate what ever mechanism for loading data into the model (visual interface, queue, whatever) from the prediction system.

And, now that I have made that clear, I am going to violate that principle... at least in part.

#  Flask

![Flask]({{ site.url }}/images/flask.png)
 
[Flask](http://flask.pocoo.org/) is a micro-framework for creating apps/services with python.  It provides a very simple mechanism for responding to web requests.  I have chosen to use it for the purposes of exposing the dog/cat Keras model.
 
For anyone that has worked in a standard web server environment (springboot, rails, etc) working with flask is pretty simple.  I will let the reader browse the docs, and will just cover the highlights of how I used the model.

The first thing you might notice is that I have not used classes, but rather just defaulted to plain old python scripting for the server class.  I prefer to use classes because I believe that it makes unit testing much easier.  Unfortunately, tests are sadly missing from this post.  Sorry.  I view this repo as a POC...  I know, lame excuse, right?

In looking at the main server file (the complete code is available [here](https://github.com/fractalbass/dogs_and_cats)), we have the following imports and the initial code that sets up the Flask app...

```python
# main.py
from flask import Flask, current_app, request, jsonify, redirect, url_for
from PIL import Image
import requests
from io import BytesIO
import logging
import numpy as np
import os
from werkzeug.utils import secure_filename
from keras.models import load_model
from keras import backend as K

#  Load saved model...
print("Loading model configuration.  One moment...")
model = load_model('./second_try.h5')
model.summary()
print("Configuration loaded.")
app = Flask(__name__)

#  This is by convention based on how the model was trained...
class_names = {0: 'CAT', 1: 'DOG'}

# Configure image specifications
img_width, img_height = 150, 150
K.set_image_dim_ordering('tf')
if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)


# We save the image and then process it.
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
```

The main imports are included here as a courtesy to my dedicated readers... because I hate it when people don't include those.

If you recall at the end of the last section, I made a big deal about using 

```python
model.save('second_try.h5')
```

That was so that we could do this...

```python
model = load_model(second_try.h5')
```

(Remember those imports?  Note that load_model is one of them!)

Next, we have some code that specifies how our images will be formatted and where the images will be saved.  Depending on the backend you chose to use with Keras (Therano, TensorFlow, CNTK, etc), the format of the images may be different.

Under the covers the model that we are using in this post is a convolutional neural network (CNN).  For more information about CNNs, check out [my blog post on that subject](http://datascience.netlify.com/general/2017/07/24/data_science_10.html).  

Once the initial have run in the python script, the Flask server will start up.  The command that does that is at the end of the script...

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
```

Here we are starting up the server to run on the local host and on port 8080.

From there, a number of the methods that are annotated in the file are used to serve up data.  There are two main ones that I am going to call out, including the endpoint that allows us to service up a static HTML page.

```python
@app.route('/')
def root():
    return app.send_static_file('index.html')
```

The above path required that I declared the Flask app like so at the beginning of the file...
```python 
app = Flask(__name__, static_url_path='')
```

The endpoint that processes files that get uploaded looks like the following.  The method saves the uploaded file in a directory on the server (which would probably need to be cleaned out from time to time), and then the trained Keras model takes over.  (The answer to your question is "Yes."  It would be possible to do this all in memory.  For now, I am just going with this route.)

```python
@app.route('/file/', methods=['GET', 'POST'])
def predict_by_file():
    classes = "ERROR PROCESSING FILE!"
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return "NO FILE SELECTED?!"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            classes = predict(file)

    return format_response(classes)
```

There is an index.html file that sits inside the "static" directory off the root of the project that looks like this:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Keras/Flask Image Processor Example</title>
</head>
<body>
<h1>
    Deep Learning Processing Server Example
</h1>
This server runs a deep learning model that attempts to tell the difference between pictures of cats and dogs.<br>
<br>
Please select a file that you would like to process...
<br><br>

<form name="someform" action="/file/" method="post" enctype="multipart/form-data">
    <input type="file" name="file"><br><br>
    <input type="submit">
</form>

</body>

</html>
```

> An important note: I spent way to much time trying to figure out why, when I started uploading files, they were all coming in as GET requests rather than POSTS.  I finally found a post on stack overflow that clued me into the fact that the action for the form tag needs to end in a "/" like so: 
> 
> ...action="/file/"  THAT LAST SLASH IS IMPORTANT!

So, when the server starts up, which happens when we just run the python file dog\_and\_cat\_server.py things should look something like this:

```text
Using TensorFlow backend.
Loading model configuration.  One moment...
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d_1 (Conv2D)            (None, 148, 148, 32)      896       
_________________________________________________________________
activation_1 (Activation)    (None, 148, 148, 32)      0         
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 74, 74, 32)        0         
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 72, 72, 32)        9248      
_________________________________________________________________
activation_2 (Activation)    (None, 72, 72, 32)        0         
_________________________________________________________________
max_pooling2d_2 (MaxPooling2 (None, 36, 36, 32)        0         
_________________________________________________________________
conv2d_3 (Conv2D)            (None, 34, 34, 64)        18496     
_________________________________________________________________
activation_3 (Activation)    (None, 34, 34, 64)        0         
_________________________________________________________________
max_pooling2d_3 (MaxPooling2 (None, 17, 17, 64)        0         
_________________________________________________________________
flatten_1 (Flatten)          (None, 18496)             0         
_________________________________________________________________
dense_1 (Dense)              (None, 64)                1183808   
_________________________________________________________________
activation_4 (Activation)    (None, 64)                0         
_________________________________________________________________
dropout_1 (Dropout)          (None, 64)                0         
_________________________________________________________________
dense_2 (Dense)              (None, 1)                 65        
_________________________________________________________________
activation_5 (Activation)    (None, 1)                 0         
=================================================================
Total params: 1,212,513
Trainable params: 1,212,513
Non-trainable params: 0
_________________________________________________________________
Configuration loaded.
```
You may see some warnings about the model not being compiled, and history not saved with the file.  Don't worry about those.  The model will run just fine, and the history is not something that we are interested in right now.

At this point, the server is up and running and ready to process requests on my local machine...


[Here is a ![Youtube]({{ site.url }}/images/youtube.png) video](https://www.youtube.com/watch?v=j5rcgwag7XU) that shows the Flask server processing a few files...  including one of my cat Parker.  


I cannot have a blog post that is about dogs and cats and not feature Parker.

![parker_again.png]({{ site.url }}/images/parker_again_sm.png)

# Going just one step further...

I was going to leave this post here, but I figured that I would take it to it's natural conclusion.  The goal of having the model running in a web server is to make it available.  So, let's do that.

Amazon has recently come out with an AMI (Amazon Machine Image) that includes a nice collection of pre-installed deep learning tools.  This is handy because it allows us to create machine instances (EC2 Instances) in the Amazon cloud very easily.  From there, it is possible to publicly expose trained deep learning models using the Flask technique that I have outlined above.  

![Flask]({{ site.url }}/images/IAmDeveloper.png)

(A little geeky humor.)

These steps use the [AWS Console](https://aws.amazon.com/console/).  AWS or Amazon Web Services is a cloud provider that we will use to publish our deep learning model server that we created with Flask.  There are other alternative services including Google Cloud Compute, and Microsoft Azure to name a few.

Here are the steps to following to create an EC2 Instance and access it with ssh.

## 1. Launch an instance.
![AMI_setup]({{ site.url }}/images/1_Launch_Instance.png)
## 2. Select a Deep Learning AMI
![AMI_setup]({{ site.url }}/images/2_Select_Deep_Learning_AMI.png)
## 3. Select the Instance Type
![AMI_setup]({{ site.url }}/images/3_Instance_Type.png)
## 4. Set configuration details
![AMI_setup]({{ site.url }}/images/4_Configuration_Details.png)
## 5. Set storage.  
Note: You will have to use 50GB storage for the deep learning AMI, which will bounce you out of the free tier, unfortunately.
![AMI_setup]({{ site.url }}/images/5_Storage.png)
## 6. Set the tags.
![AMI_setup]({{ site.url }}/images/6_Tags.png)
## 7. Configure the security groups.  
![AMI_setup]({{ site.url }}/images/7_Configure_Security_Groups.png)
## 8. Specify a SSH Keypair. 
(Note:  You need to click on "Launch" on the review page in order to get to the "Select an existing key pair or create a new key pair" dialog below.  I already have a Keypair set up and am using it.  You can create a new one also.  If you are not failure with using using key pairs and ssh to connect to EC2 instances, you can read about it [on Amazon's AWS site.](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html) 
![AMI_setup]({{ site.url }}/images/8_Select_Keypair.png)

## 9. Access the running instance.
After a few moments our machine will launch in AWS.  To get to that machine, you will need to go to the EC2 instances dialog, and find the public IP address...

![AMI_setup]({{ site.url }}/images/9_Public_IP_Address.png)

For us the address will be 54.208.33.27

Now, login in with ssh using the specified public IP address and the keypair we specified in step 8 above.

```text
ssh -v -i ./PHG_2016_Keypair.pem ec2-user@54.208.33.27
```

You should see a bunch of stuff go by and then:

```text
=============================================================================
       __|  __|_  )
       _|  (     /   Deep Learning AMI for Amazon Linux
      ___|\___|___|

The README file for the AMI ➜➜➜➜➜➜➜➜➜➜➜➜➜➜➜➜➜➜➜➜  /home/ec2-user/src/README.md
Tests for deep learning frameworks ➜➜➜➜➜➜➜➜➜➜➜➜   /home/ec2-user/src/bin
=============================================================================

Amazon Linux version 2017.03 is available.
[ec2-user@ip-172-30-0-213 ~]$
```

# Completing the environment setup

Great!  Now we have a server.  Let's take just a second to poke around...

First, note that GIT is already installed on our server!

```text
[ec2-user@ip-172-30-0-213 ~]$ git --version
git version 2.7.4
```

Also note that we have two versions of Python!

```text
[ec2-user@ip-172-30-0-213 ~]$ python --version
Python 2.7.12
[ec2-user@ip-172-30-0-213 ~]$ python3 --version
Python 3.4.3
```

For our purposes, let's set the instance to use Python3 by default...

```text
[ec2-user@ip-172-30-0-213 dogs_and_cats]$ sudo alternatives --set python /usr/bin/python3.4
[ec2-user@ip-172-30-0-213 dogs_and_cats]$ python --version
Python 3.4.3
```

Now let's check out Keras...  but before we do, let's tell keras to use the TensorFlow backend.  If we don't do that, Keras will default to the mxnet backend. To make the switch, edit the file /home/ec2-user/.keras/keras.json and change the backend from "mxnet" to "tensorflow".  

```text
{
    "epsilon": 1e-07,
    "image_dim_ordering": "tf",
    "floatx": "float32",
    "backend": "tensorflow"
}
```

To confirm that keras is configured to use TensorFlow, launch python and import that keras package as seen below.  You should see the line "Using TensorFlow backend."

```text
[ec2-user@ip-172-30-0-213 ~]$ python
Python 3.4.3 (default, Sep  1 2016, 23:33:38)
[GCC 4.8.3 20140911 (Red Hat 4.8.3-9)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import keras
Using TensorFlow backend.
```

Since the AWS instance, thanks to the AMI, comes pre-configured with git, all we need to do is import our get repo...

```text
[ec2-user@ip-172-30-0-213 ~]$ git clone https://github.com/fractalbass/dogs_and_cats.git
Cloning into 'dogs_and_cats'...
remote: Counting objects: 2227, done.
remote: Compressing objects: 100% (2219/2219), done.
remote: Total 2227 (delta 4), reused 2227 (delta 4), pack-reused 0
Receiving objects: 100% (2227/2227), 59.68 MiB | 16.34 MiB/s, done.
Resolving deltas: 100% (4/4), done.
Checking connectivity... done.
[ec2-user@ip-172-30-0-213 ~]$
```

>Note:  I am skimming over, at a dangerously high level, the involved topics of running Flask servers in AWS, using CI/CD (Continuous Integration and Continuous Deployment), and the larger issue of DevOps best practices.  :)
  
Next we need to install some python packages in order to get our server to work...

```text
sudo pip install Flask
sudo pip install h5py
sudo pip install keras --upgrade
``` 
(Note:  Keras is installed already, but the version is 1.x.  We need to upgrade the keras to 2.x for our dog_cat_server web app to work.)

Now, we can run our server...

```text
[ec2-user@ip-172-30-0-213 dogs_and_cats]$ python ./dog_and_cat_server.py
Using TensorFlow backend.
Loading model configuration.  One moment...
...
=================================================================
Total params: 1,212,513
Trainable params: 1,212,513
Non-trainable params: 0
_________________________________________________________________
Configuration loaded.
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```

Optional: to run the web app in the background, which will allow us to log out of our EC2 instance and not kill the server, do this...

```text
nohup python dog_and_cat_server.py &
```

Now we just point our browser at the IP of our EC2 instance and port 8080  (http://54.208.33.27:8080/)

![AMI_setup]({{ site.url }}/images/AWS_DL_Browser_1.png)

![AMI_setup]({{ site.url }}/images/AWS_DL_Browser_2.png)

And there you have it.  Our deep learning model running in AWS.  Clearly, there are a number of things that could be done at this point to harden this environment.  I am going to leave things here as this blog post is now REALLY long.

# Conclusion

So, it is very possible to serve up fairly complex Keras model for image processing that don't require the full blown TensorFlow server, or protobufs.  It maybe that there are situations where processing requirements may force us to a full blow server, or a more complex solution.  That said, I think that there may be value in many applications to avoid [premature optimization](http://wiki.c2.com/?PrematureOptimization) in favor of baby steps toward a workable solution.

In the meantime, I wanted to mention that I do have some capacity at this time to help out on data science projects.  If you are looking for additional consultants to help with your data science project (machine learning or whatever) please feel free to contact me at the address below.

Until next time..


   