---
layout: post
title:  "Neural Networks: Saving Humpty Dumpty"
date:   2017-07-14 00:16:00 -0500
categories: general
---
# Neural Networks: Saving Humpty Dumpty

![Neural Net Egg]({{ site.url }}/images/NeuralNetEgg.png)

## Introduction

This post is about a video game that I have written called "Neural Nest."  The game can be played by a person, or by an included neural network agent.  The neural network plays the game by making predictions about the best action in the game based on the layout of the pixels on the game display.  The agent has no knowledge of the internal workings of the game.  

### tldr;


The following collected statements are from my internal dialog while writing this post and the associated code. It is included here for people that don't have enough time, or interest to read the entire post.  (You know who you are.)  

> People are always saying "I saw your post...  I didn't read it though.  It was too long."


> "I should write a post about reinforcement learning neural networks."

> "Training nets to play video games is a good way to demo RL and convolution networks."

> "Everybody and their dog has written a post about convolution neural nets and python/pygame Atari games."

> "I should write my own game."

> "It should be very fancy!"

> "Uhhhh...  on the other hand, maybe it should be very very simple."

> "Now that the game works, I should do a convolution neural net to play it."

> "Uh oh.  Convolution neural networks take lots of time and computing resources."

> "Wait...  I don't need a convolution neural net to play the game that I just wrote.  I can just use a straight SGD (stochastic gradient descent) algorithm with a standard sequential neural net."

> "This isn't working.  Maybe this neural net stuff wasn't such a good idea."

> "WAIT!!!  I don't have good training data.  I should create synthetic training data."

> "Holy smokes, IT ACTUALLY WORKS!"

Feel free to skip ahead to the video at the end of the post.  For the genuinely curious, read on!

## Neural Nest

Neural nest is a game that I created specifically as something that a neural net could learn to play.  To that end, there are several things about the game that you may notice...

1.  It is simple.
2.  The resolution is pretty low (20x20)
3.  There are a limited number (3) actions that a player can make during game play

The game itself works like this:  Eggs randomly drop from the top of the game display.  The user controls a basket at the bottom of the screen to catch the eggs.  If an egg gets to the bottom of the screen before a player can catch it, the egg breaks.  Play continues for a set number of eggs.  The final success percentage (number of eggs caught / total number of eggs) is the players final score.

[This video](https://youtu.be/QWpDDZr157M) shows me playing the game for a set of 10 eggs.

The game itself is written with the help of [pygame](https://www.pygame.org/wiki/about).  Pygame is a Python library that can be used to create video games.  The purpose of this post is not really to delve into pygame (I am trying to keep my posts under 10 pages because SOME PEOPLE seem to think that is a bit long. Again, you know who you are.) 



## Picking the right tool for the job

![Neural Net Egg]({{ site.url }}/images/xkcd_neural_network.png)

Originally, I was going to attempt to use a recurrent neural network to learn to play NeuralNest.  For a great article on RL nets and video games, check out [this blog post](http://karpathy.github.io/2016/05/31/rl/).  As I was attempting to follow some of the work of [Daniel Slater](http://www.danielslater.net/2016/03/deep-q-learning-pong-with-tensorflow.html) it occurred to me that I really didn't need to use a recurrent neural network to play the game.  I should still be able to use the pixels of the screen as input, and have the network move the nest either left or right.  I could train the network, however, to simply move the nest to the left or right based on the location (x coordinate) of the dropping egg.

![Neural Net Egg]({{ site.url }}/images/HurryUp.png)

##  Finding the right training data

My original attempt at getting training data, was to just let the game run, and as it did, compute the training value based on the location of the basket and the egg.  I then saved the data off into a CSV file that could later be used for training.  There were a couple of problems with that approach however.

First, the way that numpy, pygame, and keras handle data in arrays is not terribly consistent.  I was thinking that I could grab the data from the screen using pygame, and the data would be in a nice row x column matrix.  Thanks to some helpful unit tests, I found that that was not the case.  eg.

(Note that the .swapaxes call on the forth line!)

```python
  def get_surface_grayscale_array(self):
        gray_scale_array = []
        surface_array = pygame.surfarray.array3d(self.display_surface)
        surface_array = surface_array.swapaxes(0, 1)
        new_surface = np.reshape(surface_array, (self.surface_width * self.surface_height, 3))
        for x in new_surface:
            c = ((int(x[0])+int(x[1])+int(x[2]))/(255*3))
            gray_scale_array.append(c)
        return np.array(gray_scale_array, dtype=float)  
```

Also, the approach that I was taking was not updating the location of the basket.  Moving left or right depends not only on the location of the egg, but also on the location of the basket.  

In order to include various basket locations in the training data, I created a python script that programmatically created a training set that included each possible position of the eggs and the basket, and the correct direction to move.  Again, this may seem like a cheat, but I don't think it actually is.  In the end, the network will only be able to make suggestions based on the pixels on the screen.  I think of it more like trying to just provide the network with a full and complete education. :)

## Network Architecture

The network architecture that I used for the game is:

```python
        inputs = Input(shape=(screen_width*screen_height,))
        x = Dense(400, activation=K.sigmoid)(inputs)
        predictions = Dense(1, activation=K.tanh)(x)
        model = Model(inputs=inputs, outputs=predictions)
```

As you can see from the above, the network is a simple 3 layer network.  The first layer takes in all of the pixels on the screen.  The hidden layer has 400 nodes, and uses a sigmoid activation function.  Finally the output layer uses a arch-tangent function, which scales the data conveniently between negative and positive values...  though I believe that Keras would actually do that if we were to use a different activation function.

## Training Results

The following chart shows the network after it was trained in batches of 100 training vectors and with 2000 training epochs.

![Neural Net Egg]({{ site.url }}/images/synthetic_data_pass_1.png)

##  The super cool video!

And finally, here is the end result...

[Neural Net Agent Plays Neural Nest](https://youtu.be/Lysrs6Y1-Lc)

The neural network gets a score of 84%...  The basket in the game is 5 pixels wide, and the screen is 20 pixels across.  So, if the eggs are evenly distributed, we would expect the game to score around 25%. Clearly, the trained agent is doing something right.

## This is easy.  I wonder if...

One of the benefits of using sequential neural networks is that they have the ability to generalize.  In other words, they can often figure out what to do even if they have not be trained on the situation.  So, let's see how our neural network does if we make things a bit more difficult.  We could speed up the game by making the eggs drop faster.  That, however, won't have much effect.  The network grabs the screens one at a time, so the motion of the eggs doesn't have any impact.  Regardless of the egg speed, the network is acting on snapshots of the data.  

One way that we can make the situation more difficult is by increasing the number of eggs that fall at one time as well as speed the eggs.  Because the eggs fall at different rates (did I mention that) this can lead to impossible scenarios, so we probably will not see the network do as well.  In this video, the game drops another egg as soon as the one before it has fallen at least 7 squares.  It can also chose not to drop an egg and wait a few more cycles.  You can see the results in this video...

[Neural Net Agent...  Mission Impossible.](https://youtu.be/eF4ugkTBa1E)

In this video the agent success rate dropped to 62%. 

## How does this compare to a real person?

When I tried it at that level, I got...

```
 Game over.  Caught:39   Dropped:61  Success Rate=39% 
```

I'll spare you the video.  Suffice it to say that when I tried the game at that level, I lost more than a few Humptys.

## Conclusion

While Reinforcement Learning techniques are a proven way to train neural networks to play video games, based on the structure of the game we have shown that basic SGD neural nets perform well.  In addition to performing at training levels, the networks generalize well and can even exceed the ability of humans (me) at playing simple video games.

The code for this post (such that it is) is available on github at:  

[https://github.com/fractalbass/neuralnest](https://github.com/fractalbass/neuralnest)

Note:  This blog post and the associated code evolved over time.  As a result, the code is not as clean as I would have liked it to be.  I hope to return to this code in the future and clean it up a bit.

Thanks for checking out this post.  I have a couple more planned, so check back soon, or subscribe to the feed.



 
 