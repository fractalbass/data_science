---
layout: post
title:  " Building a Deep Learning Desktop PC Part 2"
date:   2018-1-1 00:09:00 -0800
categories: general
---

# Building a Deep Learning Desktop PC Part 2
 
![Battling Tops]({{ site.url }}/images/battling_tops.jpg)

I clearly remember playing "Battling Tops" as a kid with my neighbor friend, Danny Eggestein.  We had hours of fun letting our tops smash into each other...  the last top spinning won.  

Installing software for the GeForce GTX 1080ti was a little like playing battling tops with Danny.  The tops were the Ubuntu and NVidia drivers for the 1080ti, and the arena was the Linux OS.  It was fun...  but not as fun as the real battling tops with Danny!

In my last post, I covered the steps to build a desktop deep learning PC from parts.  This post continues on that subject and will cover the steps necessary to install and configure Ubuntu 16.04, Cuda 8.0, Tensorflow, and Anaconda (Python) on that box.  

## A little background on why I decided to do this...

The underlying concepts for Deep Learning are not new.  Deep Learning is based on the use of artificial neural network algorithms (ANNs) implemented in some programing language.  Using ANNs typically consist of two phases: training the network and using the trained network to process or evaluate data.  Deep learning involves neural networks that are large, complicated and consist of many hidden layers.  At their most basic level, however, these networks are really just acting as mathematical functions that contain a vast number of parameters.  Training these networks involves using calculus and linear algebra to minimize the error between the output of the network and some known values.  The training process is iterative, and involves computing minor adjustments to the network parameters over and over in an effort to “dial in” the desired behavior.  Frameworks like Tensorflow and Keras take care of the underlying linear algebra and numerical computations involved with building and training neural networks, enabling data scientists to work at a much more abstract level.  These frameworks have also been optimized to make them run as fast as possible.  

One key concept that is sometimes overlooked or altogether not understood by people not familiar with ANNs in general is that to train an ANN, you need two things:  

Lots of data.<br>
Lots of processing power.<br>

There are no guarantees with ANNs in terms of their ability to actually “learn” a set of outputs based on a set of given inputs.  Because of this fact, developing ANNs that actually work involves a good deal of experimentation.  

<hr>
![xkcd machine learning]({{ site.url }}/images/xkcd_neural_network.png)<br>
[XKCD Machine Learning](https://xkcd.com/1838/)
<hr>
<br>
A computer that can very quickly perform the training portion of the ANN “workflow” can be a significant factor in the success of any deep learning project.  While there are cloud based solutions for training deep networks, including those provided by Microsoft Azure, Amazon AWS and Google Cloud Compute, these services can be somewhat expensive.  They are also a bit limited due the fact that training an ANN can require significant amounts of data to be passed into the network.  Cloud platforms do offer solutions for moving data around, but they are never as quick or as easy as using local disk.  Using cloud computing can also incur significant costs for high performance instances.  And, unless high performance instances are used, cloud computing ANN training solutions typically perform worse than a dedicated desktop PC.  

## Getting Started...

So, here we are.  In my last post, I covered the steps I took to design, acquire, and build a desktop PC that includes specific hardware for working with ANNs and deep learning.  In this post, I will go over the steps required to configure the following software on that box:

1. Ubuntu 16.04
2. NVidia CUDA toolkit and CuDNN frameworks
3. Anaconda Python
4. Tensorflow with GPU support
5. Development Tools (GIT, Pycharm, etc.)

## Installing Ubuntu.

Installing Linux has become very easy compared to the days when it required the use of about 15 floppy disks.  (Yes, I have done that…  I know.  I am dating myself.)  In the relatively not to distant past, the preferred way of installing linux was to use an installation CD or DVD.  Now, however, CD and DVD drives are starting to go the way of the floppy disk.  In the case of my new machine, I didn't include a DVD drive.  Instead, I used a USB “thumb-drive” for my install.  To do this, you must download Ubuntu, and then “burn” the Ubundtu ISO to the USB device.  You’d think this would be no big deal.  Unfortunately, the ISO images provided by Ubuntu are not compatible with the graphical Mac disk utility.  (My other computer is a Mac).  The workaround is to use a command line tool to write the ISO image to the USB drive.

[This post](http://osxdaily.com/2015/06/05/copy-iso-to-usb-drive-mac-os-x-command/) shows how to go about this process.  An example of that command looks like this:
<pre># Note:  You must adjust this to meet the configuration of your system
sudo dd if=~/Desktop/ubuntu-16.04.3-desktop-amd64.iso of=/dev/sdb bs=1m</pre>

Once the thumb drive has been created, it can be inserted into the new computer and used to boot up the system.  It may be necessary to make adjustments in your BIOS in order to boot from USB.  That will depend on the motherboard and BIOS you are using.  

The Ubuntu site recommends that you first try and run Ubuntu from the disk before you go through the process of installing it.  Of course, I didn’t do that.  :)

## Installing video drivers.

Ubuntu does an excellent job of detecting hardware installed on your computer.  It automatically detected the NVIDIA card (GeForce GTX 1080 ti) and tried to load drivers to run it.  However, the drivers that Ubuntu tried to use to run the card don’t work with the 1080ti.  Furthermore, in the case of this machine, I don’t really want to use the NVIDIA card for graphics anyway.  So, to get around that little issue, it is necessary to prevent Ubuntu for trying to use the Nvidia card.  

Note:  Calling my GPU “the NVidia card” may be confusing.  The card does contain chips made by Nvidia.  However, the card itself is manufactured by [EVGA](https://www.evga.com/products/product.aspx?pn=11G-P4-6696-KR)

Ubuntu uses a utility called [modprobe](http://manpages.ubuntu.com/manpages/artful/man8/modprobe.8.html) to intelligently and dynamically install drivers in the Linux kernel.  In order to prevent Ubuntu from trying to use the NVidia card, we need to make sure that modprobe doesn’t try to load drivers for it.  That can be done by editing the file:

/etc/modprobe.d/blacklist-nouveau.conf with the following contents:
<pre>blacklist nouveau
options nouveau modeset=0</pre>


Once this is done, you will need to run 

<pre>
sudo update-initramfs -u  
sudo depmod -a
</pre>

And then reboot your computer.  (The depmod line is probably not required if you reboot.)

It can be tricky to edit the file above because of the fact that it is involved with a video driver.  The driver attempts to load automatically, and when it does it may not allow the default XWindows window manager to run.  The symptom that I saw was that I could boot my box, and get to the Ubuntu graphical login screen.  However, after I entered my password, my screen was filled with messages similar to those described in [this post](https://bbs.archlinux.org/viewtopic.php?id=199578).  To get around that, you can press  Ctrl+Alt+F1. That will drop you into a terminal window where you can log into Ubuntu in text mode.

Another option might be to delay putting the Nvidia card in the box until you have had a chance to blacklist the nouveau drivers as shown above.

At any rate, once I was able to get past the Nvidia Ubuntu issue, I tried to install various combinations of CUDA and CUDNN, Tensorflow, and Python.  That was very frustrating and time consuming.  The great thing about linux is that it is so open.  Unfortunately one of the weaknesses is that, even for a distribution like Ubuntu, there is a tremendous variety when it comes to versions of the linux kernel, device drivers (Nvidia) and language tools like Tensorflow.  Ultimately, I found a set of instructions posted to a GIT repo by William Falcon.  Those instructions generally worked.  I have forked that repo and made a few slight changes here:

https://github.com/fractalbass/tensorflow-gpu-install-ubuntu-16.04

I have also submitted a PR to William to see if my changes can be brought into his original repo.

As a summary, here are the steps that you need to complete.  For complete instructions please [refer to my GIT repo](https://github.com/fractalbass/tensorflow-gpu-install-ubuntu-16.04).

1. Update apt-get
2. Install apt-get dependencies (JDK, python, build tools, etc.)
3. Install the NVidia drivers (from Nvidia but NOT the video driver.)
4. Confirm the NVidia driver install
5. Install the CUDA tool kit (cuda_8.0.61_375.26_linux.run)
Make sure you DO NOT INSTALL THE VIDEO DRIVER
6. Install CUDNN (cudnn-8.0-linux-x64-v6.0.tgz)
7. Update ~/.bashrc:
8. Install miniconda
9.  Reload bashrc
10. Create conda virtual environment
11. Activate conda virtual env
12. Install tensorflow with GPU support (pip install tensorflow-gpu)
13. Test tf install

<pre>
# start python shell   
python

# run test script   
import tensorflow as tf   

hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
</pre> 

Again, full instructions for the above can be found here:  

https://github.com/fractalbass/tensorflow-gpu-install-ubuntu-16.04

# Performance

Now that the environment is setup and configured.  It is worthwhile to check the overall performance of the new box.  To do that, I used a project that I am working on that involves using tensorflow to recognize spoken words in audio files.  

The code that I am working on actually involves training 10 convolutional neural networks each with 6 layers and runs over a total of 20 epochs.  That is relatively small training job, but it serves to illustrate the improved performance of the GPU over just using a CPU.  Here are the results (drum roll please...)

<pre>
Non GPU System Training Time:  4146 Seconds
GPU Based System:  816 Seconds

Total reduction in training time:  80.3183%
</pre>

I'll take an 80% reduction in training time any day!

I hope you have enjoyed this post on installing various software components to enable a desktop PC for deep learning.

Check back for more posts on data science and machine learning.







