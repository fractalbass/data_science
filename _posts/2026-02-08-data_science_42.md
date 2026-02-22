---
layout: post
title: Dendrites Aren't Digital
date: 2026-02-22 00:00:00 -0500
categories: []
---

# Dendrites Aren't Digital
### How Artificial and Biological Neural Networks Differ
Miles Porter  
Feb 22, 2026

---

At a recent AI summit that I organized for my company, it became clear to me that not everyone fully understands the basics of generative AI, or artificial neural networks in general. As a result, now seems like a good time to pause and put down some of my thoughts on how artificial neural network systems differ from biological systems.

Some background: I studied applied mathematics at Colorado State University in the early 90s. One of the areas I focused on was pattern analysis and neural networks. Neural nets had been around for a while, actually going back to the 60s or before. What had changed in the 90s was that new advances in computing power were making it possible to run larger and larger neural networks. This was a time before cloud computing, and really even before the internet. Most of the networks that I worked on consisted of a few layers of fully connected nodes. However, their power seemed really amazing. One experiment we did was to train a neural network to learn the logistic map. I recreated that work using TensorFlow later here: https://github.com/fractalbass/simple_neural_net

Back in grad school, we didn't have TensorFlow and Keras, so we had to write the network algorithms by hand. I spent hours writing for-loops in C and dealing with how to numerically implement the gradient descent algorithm — literally to the point of tears.

And, aside from some mild emotional scarring, I was left with a huge realization: mathematically modeled neural networks are VERY DIFFERENT from biological "wet" neural networks that I had studied in my basic biology classes in some pretty fundamental and very important ways.  One of those has to do with how signals flow through artificial vs biological networks.

---

## Synchronized vs. Non-Synchronized Networks

In a numerical neural network, nodes and synapses are modeled, but the flow through the network is governed by strict timing. Signals flow from layer to layer and node to node in a preset order, and that order is critical. When training a neural network, a signal is passed into the network and the output is observed at the other end. That output is compared to some expected training value, and the error is then "back-propagated" back through the neural network and used to adjust the parameters of each node in order to reduce the error just a little bit. Then a new pattern is passed in and the output observed. That output is compared to the expected training value and the error is, again, back-propagated through the neural network. This process continues over and over and over. There are some slight variations on this process — such as saving up all the updates and applying them all at once (batch mode), or tweaking the method of calculating the errors — but essentially the process remains the same. The point here is that it is a VERY STRUCTURED process. That is necessary because the algorithm for minimizing the error coming out of the network depends on the chain rule in calculus.

$$\frac{d}{dx} f(g(x)) = \frac{df}{dg}\Big|_{g(x)} \cdot \frac{dg}{dx}$$

That $f(g(x))$ part is really important. Let's say that I have a 5-layer neural network, and I want to update the weights in the top layer based on some observed error. To do that, I would need to do the following:

$$
\frac{\partial L}{\partial w^{(5)}_{ij}}=\frac{\partial L}{\partial a^{(5)}_i}\cdot\frac{\partial a^{(5)}_i}{\partial z^{(5)}_i}\cdot\frac{\partial z^{(5)}_i}{\partial a^{(4)}_j}\cdot\frac{\partial a^{(4)}_j}{\partial z^{(4)}_j}\cdot\frac{\partial z^{(4)}_j}{\partial a^{(3)}_k}\cdot\frac{\partial a^{(3)}_k}{\partial z^{(3)}_k}\cdot\frac{\partial z^{(3)}_k}{\partial a^{(2)}_m}\cdot\frac{\partial a^{(2)}_m}{\partial z^{(2)}_m}\cdot\frac{\partial z^{(2)}_m}{\partial a^{(1)}_n}\cdot\frac{\partial a^{(1)}_n}{\partial z^{(1)}_n}\cdot\frac{\partial z^{(1)}_n}{\partial w^{(5)}_{ij}}
$$

Which is a friggin' mess.

But the important thing is that in order to do this, I need to compute partial derivatives for the 5th layer, then the 4th, then the 3rd, and so on up to the first layer, in order to update the weights in each layer. This is the core concept behind "back"-propagation of errors. If the network didn't have this preset structure, this becomes very, very difficult to do. The network needs to fire completely through one time, then everything stops and the error is computed before optimization can take place.

Biological neural networks differ from artificial neural networks in some other critical ways too:

1. Biological neural networks use both electrical and chemical signals.
2. Biological neural networks have extremely complex topologies that are constantly changing.
3. Biological neural networks don't have strictly synchronized digital timing.
4. Biological neural networks include neurons that fire at different speeds and delays.
5. Biological neural networks are decentralized and involve local plasticity rules rather than centralized gradient-based optimization.
6. Biological neural networks are analog systems, artificial neural networks are digital.

All of these factors combine to make back-propagation of errors essentially impossible in biological neural networks.

---

### Looking Ahead

Most artificial neural networks in practice follow what I described above in terms of their structure and algorithms. However, there are a few exceptions.  One of these exceptions can be found in a paper written in 1997, which proposed a "third generation" of artificial neural networks called "spiking neural networks": [Maass (1997) — "Networks of Spiking Neurons: The Third Generation of Neural Networks"](https://igi-web.tugraz.at/people/maass/psfiles/85a.pdf)

Spiking neural networks differ from traditional artificial neural networks in a couple of critical ways:

1. The neurons in a spiking neural network store up input signals until they reach some critical threshold and then fire.
2. The firing of a spiking neural network is binary (0 or 1). This kind of binary function is not differentiable, which means it cannot be optimized by gradient descent (the chain rule) or any other similar process.

Because of point 2, optimizing (training) a spiking neural network becomes a non-convex optimization problem — in other words, they are very difficult to train. However, quantum computing might provide a potential solution. Quantum annealing is an approach specifically designed for optimization problems. However, we are a long way from having this approach enter the mainstream of computing.

---

## Conclusion

What I hope readers take away from this post is that artificial neural networks — which are the foundation of the current "AI" buzz — differ in some really dramatic ways from biological neural networks.

Stay tuned for more articles on topics related to data science and AI.

---

*Notice: The content of this article was initially written by Miles Porter — a human. AI technology has been used to proofread and format the content. AI systems can hallucinate and make mistakes. It is important to verify and double-check the above content.*