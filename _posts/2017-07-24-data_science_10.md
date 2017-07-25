---
layout: post
title:  "The Cat Returns"
date:   2017-07-24 00:10:30 -0500
categories: general
---
# My cat, Parker, has a superiority complex.

Readers of this blog are likely to recall that I have a cat named Parker.  Parker is known for several things in our house including his love for salmon, and his work at holding down our beds.  I believe in Parker's cat-mind, he sees himself like Prince Lune from the Studio Ghibli movie "The Cat Returns".

![Prince Lune]({{ site.url }}/images/prince_lune.png)

I think he may actually be a bit more like this cat from the same movie:

![King Cat]({{ site.url }}/images/king_cat.png)

Regardless of which cat Parker most closely resembles, stats from LinkedIn show that when I mention him, my blog posts get more clicks.

![Cat post views]({{ site.url }}/images/Blog_Views.png)

> BTW, check out my post on 
[Trump's Tweeting habits, titled "Yuge Data."](http://datascience.netlify.com/general/2017/06/30/data_science_7.html)  It wasn't my most popular post, but I think it is the most interesting.

Anyway, if you like cat pictures, your in luck.  This post has several.  I fully expect my stats to skyrocket!

## Introduction

A couple posts ago, I wrote about training neural networks to play video games.  In that post, I started with trying to use a convolutional neural network, and then opted to go with a dense feed-forward neural network instead.  In this post, I am going to return to talking about convolutional neural networks.  

For an overview of different types of neural networks, I would recommend [The Asimov Institute's Neural Network Zoo](http://www.asimovinstitute.org/neural-network-zoo/).  This site has an excellent list of the different kinds of neural networks, and what they are well suited for.

## TensorFlow Image Recognition

[TensorFlow.org](https://www.tensorflow.org/tutorials/image_recognition) provides several tutorial on CNNs (Convolutional Neural Networks.)  These tutorials include one on [Inception-v3](https://arxiv.org/abs/1512.00567).  Unlike my other posts on neural nets, where I looked at training the models, this post actually starts with a model that has already been trained.

First, we will take a quick look at the model, and then see how it categorizes a few images.

## Inception-v3 Architecture

The Inception-v3 network is a 42-layer neural network that includes several different kinds of network layers.  A complete description of the network is included in [this paper](https://arxiv.org/pdf/1512.00567.pdf).

The paper also covers a number of design principles that the developers of the Inception-v3 network followed.  I will not delve too deeply here, and simply point you, good reader, to the reference above for more information about the network.  You may want to break out your linear algebra and linear programming text books.  :)

# BUT WHERE ARE THE CAT PICTURES?!

(Hang on. We'll get to them shortly.)

##  Classifying images.  The cute panda.

[The github repo for Tensorflow models](https://github.com/tensorflow/models) includes a ready-to-run python script that can be used to classify images using Inception-v3.  The code even comes with a reference to a pre-defined image that my daughter loves.

![Cropped Panda]({{ site.url }}/images/cropped_panda.jpg)

The Inception-v3 model classifies this image as follows:

>giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca (score = 0.89107)<br>
> indri, indris, Indri indri, Indri brevicaudatus (score = 0.00779)<br>
> lesser panda, red panda, panda, bear cat, cat bear, Ailurus fulgens (score = 0.00296)<br>
> custard apple (score = 0.00147)<br>
> earthstar (score = 0.00117)<br>

From the distribution of these values, we can see that the model is pretty confident that the image is a panda.  Well, of course it is.  This is pretty much a slam-dunk for the network, particularly if you consider some of the features.  The sharp contrast of white and black, and the clear contours leave little doubt as to what it is.  But, credit where credit is due.  The network pretty much nails it.  Let's continue to see how the classifier does with some of my own images.

<hr/>

## Pen

![Pen]({{ site.url }}/images/pen.jpg)
> ballpoint, ballpoint pen, ballpen, Biro (score = 0.93985)<br>
> fountain pen (score = 0.04640)<br>
> paintbrush (score = 0.00252)<br>
> rubber eraser, rubber, pencil eraser (score = 0.00156)<br>
> lipstick, lip rouge (score = 0.00156)<br>

This was just something that I saw on my desk.  The network did a pretty good job with this one.  The network is pretty confident this is a ballpoint pen (not just a "pen" mind you), and it was correct.

<hr/>

## Lego Car

![Lego Car]({{ site.url }}/images/lego_car.jpg)
> racer, race car, racing car (score = 0.58064)<br>
> sports car, sport car (score = 0.18145)<br>
> car wheel (score = 0.01995)<br>
> tow truck, tow car, wrecker (score = 0.01637)<br>
> cab, hack, taxi, taxicab (score = 0.01329)<br>

I was curious if I could confuse the network with this one.  It didn't...  unless you were hoping that this would be classified as a "toy car".

<hr/>

## Guitar Pick

![Guitar Pick]({{ site.url }}/images/guitar_pick.jpg)
> pick, plectrum, plectron (score = 0.87724)<br>
> mask (score = 0.00917)<br>
> ping-pong ball (score = 0.00602)<br>
> balloon (score = 0.00520)<br>
> carton (score = 0.00366)<br>

I wasn't sure how this would go, but the network seemed to do just fine.  This is a guitar pick.  Since I am on the theme of music, I figured I would try a few others.

<hr/>

## Bass (6 String Ibanez)

![Bass]({{ site.url }}/images/bass.jpg)<br>
> electric guitar (score = 0.97459)<br>
> acoustic guitar (score = 0.00602)<br>
> pick, plectrum, plectron (score = 0.00213)<br>
> stage (score = 0.00116)<br>
> banjo (score = 0.00046)<br>

Ah ha!  Tricked you!  This is NOT an electric guitar.  It is an electric bass!  A bass sounds an octave below the lowest strings on an electric guitar.  At first, I thought that the 6 strings (because it is a FANCY electric bass) would fool the network.  As it turns out, that wasn't it.  As we will see with the next sample...

<hr/>

## Bass (Fender)
![Fender Bass]({{ site.url }}/images/bass_fender.jpg)<br>
> electric guitar (score = 0.97975)<br>
> acoustic guitar (score = 0.00783)<br>
> pick, plectrum, plectron (score = 0.00214)<br>
> stage (score = 0.00059)<br>
> banjo (score = 0.00026)<br>

Grrr...  This is an electric bass!  In fact, it isn't just any electric bass, it is a Fender Jazz Bass.  It is the same kind of bass that [Jaco Pastorius](https://en.wikipedia.org/wiki/Jaco_Pastorius) played.  (This one is different from Jaco's in that it was manufactured years later and is black rather than "Tobacco Sunburst".)  I am disappointed that the convolutional neural network can tell the difference between a "pen" and a "ballpoint pen", but it cannot distinguish between a guitar and a bass.  Shameful.  Furthermore, "banjo?!"  Seriously?! Whatever.  (Heavy sigh.)

<hr/>

## Flowers

![Flowers]({{ site.url }}/images/flowers.jpg)
> pot, flowerpot (score = 0.22127)<br>
> earthstar (score = 0.08891)<br>
> greenhouse, nursery, glasshouse (score = 0.06861)<br>
> hip, rose hip, rosehip (score = 0.06536)<br>
> strawberry (score = 0.02462)<br>

Now, this one surprised me.  This is a flower, but not in a pot.  An [Earthstar](http://www.bromeliads.info/cryptanthus-earth-stars/) is a plant, and not a flower.  This is some kind of Lily, I think.  We planted it years ago, and I don't recall the name.  Please email me if you know what it is.

Another interesting thing to note on this one is that "Earthstar" came up once before.  If you were paying close attention, you will recall that the CNN listed Earthstar as a possible category (with very low confidence) for the "cute panda".

<hr/>

## Moth

![Moth]({{ site.url }}/images/moth.jpg)<br>
> hermit crab (score = 0.52525)<br>
> necklace (score = 0.11775)<br>
> hair slide (score = 0.02804)<br>
> chain (score = 0.01688)<br>
> rock crab, Cancer irroratus (score = 0.01479)<br>

Er, what?!  This surprised me.  It is not even close to a hermit crab.  This is a huge moth that our family saw on our recent trip to the [Key West Butterfly and Nature Conservatory](https://www.keywestbutterfly.com/).  We can see, however, that the networks confidence is not terribly high.  You may have noticed that the same lack of confidence also happened with the previous image.

<hr/>

## Gopher?

![Gopher]({{ site.url }}/images/gopher.jpg)
> fox squirrel, eastern fox squirrel, Sciurus niger (score = 0.40793)<br>
> marmot (score = 0.24043)<br>
> cliff, drop, drop-off (score = 0.22557)<br>
> wombat (score = 0.01557)<br>
> koala, koala bear, kangaroo bear, native bear, Phascolarctos cinereus (score = 0.00727)<br>

Our family came across this little guy on a recent trip to western North Dakota.  The model fairly accurately identifies this creature as a kind of squirrel.  It turns out that it is actually a [thirteen-lined ground squirrel](https://en.wikipedia.org/wiki/Thirteen-lined_ground_squirrel).

Some North Dakota folk refer to these creatures as "Gophers".  In Minnesota, where I live, we commonly think of Gophers as either the mascot of [The University of Minnesota](https://twin-cities.umn.edu/athletics) or as nasty creatures hell-bent on destruction, and not as cuddly little guys.

![Gopher]({{ site.url }}/images/real_gopher.jpg)

> beaver (score = 0.88776)<br>
> porcupine, hedgehog (score = 0.01643)<br>
> marmot (score = 0.01089)<br>
> guinea pig, Cavia cobaya (score = 0.00342)<br>
> otter (score = 0.00255)<br>

Don't let those teeth fool you like they probably did the CNN.  The image above is a real [gopher](http://www.victorpest.com/advice/rodent-library/gophers)!  

So, if the above picture is a real gopher, what does the CNN think the U of M's mascot is?

![Goldy Gopher]({{ site.url }}/images/goldy_gopher.png)

> teddy, teddy bear (score = 0.75890)<br>
> toyshop (score = 0.01518)<br>
> nipple (score = 0.00805)<br>
> brown bear, bruin, Ursus arctos (score = 0.00512)<br>
> comic book (score = 0.00422)<br>

Hmmm.  Maybe we should just push on.

<hr/>

## Zoe

![Zoe]({{ site.url }}/images/zoe_zoom.jpg)
> tabby, tabby cat (score = 0.87688)<br>
> tiger cat (score = 0.08732)<br>
> Egyptian cat (score = 0.00134)<br>
> Persian cat (score = 0.00050)<br>
> lynx, catamount (score = 0.00032)<br>

Now we're getting to the good stuff.  The above picture is Parker's lovely sister, Zoe.  The model is pretty sure that she is a cat, which she is.  Just ask her.  Zoe, *IS* a princess!

<hr/>

## His Royal Highness, Parker

![Crazy Parkler]({{ site.url }}/images/crazy_parker.jpg)

> quilt, comforter, comfort, puff (score = 0.53268)<br>
> cougar, puma, catamount, mountain lion, painter, panther, Felis concolor (score = 0.07981)<br>
> lion, king of beasts, Panthera leo (score = 0.05694)<br>
> Egyptian cat (score = 0.02617)<br>
> tabby, tabby cat (score = 0.01700)<br>

Ohhh PLEASE!!!  I get the quilt or comforter thing...  but cougar, puma, catamount, mountain lion?!  Please don't tell Parker, or he will start to think he is really the King of the Family!!!  

<hr/>

## Conclusion

As we have seen here, convolutional neural networks are one option for categorizing images.  TensorFlow.org provides tutorials on convolutional neural networks (as well as networks of other types.)  Many of the models are pre-trained, and ready to be used to analyze images. 

I hope you have enjoyed this latest installment.  Check back soon for more posts on topics in data science and machine learning!
