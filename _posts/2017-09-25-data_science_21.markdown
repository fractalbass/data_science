---
layout: post
title:  Now What?!  Serving a Trained Keras/TensorFlow Model
date:   2017-09-25 00:09:00 -0500
categories: general
---

# Introduction

Congratulations!  You have managed to write a deep learning model that actually seems to work!  Now what?  The whole point of this deep learning stuff is to actually cut it loose on some real data, right?  Sometimes, I think, we can spend too much time focusing on the training aspect of our models but overlook the ultimate goal.

![Ship in A Bottle...]({{ site.url }}/images/ship_in_a_bottle.jpg)

One of the things that I dislike about raw TensorFlow is that it is build with, and depends on protocol buffers.  Protobufs are a "favorite child" of the brainy folks at Google.  I have several complaints about protobufs that I won't go into here, except to say that they require code generation and make it harder to troubleshoot issues.  Serving models with the google TensorFlow Server requires the use of protobufs.  There is, however, a much easier way.

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

# Conclusion

So, it is very possible to serve up fairly complex Keras models for image processing that don't require the full blown TensorFlow server, or protobufs.  It maybe that there are situations where processing requirements may force us to a full blow server, or a more complex solution.  That said, I think that there may be value in many application to avoid [premature optimization](http://wiki.c2.com/?PrematureOptimization) in favor of baby steps toward a workable solution.

Granted, this post only goes part of the way there. The next step would be to get a model running on some type of backend system.  Look for that in my next post.

In the meantime, I wanted to mention that I do have some capacity at this time to help out on data science projects.  If you are looking for additional consultants to help with your data science project (machine learning or whatever) please feel free to contact me at the address below.

Until next time..


   