---
layout: post
title:  ""
date:   2017-06-21 09:00:00 -0500
categories: general
---

## Background

A few years ago an individual that I worked with recommended a book by Emily Lambert titled [The Futures](https://www.amazon.com/Futures-Speculator-Origins-Biggest-Markets/dp/0465018432).  I was contracting for a small starup that was trying to create an online commodities exchange for human blood products.  It while it may sound gross, but the human blood market is very highly suboptimal.  For more info, check out [this article](http://www.wptv.com/news/local-news/investigations/blood-money-what-you-didnt-know-about-your-blood-donation).

### Back to commodities.

I have been doing my research at the CoCo Space in downtown Minneapolis.  The space is inside the old Minneapolis Grain Exchange trading area. One of the coolest things about the space is that the "big board" for commidities prices is still up.  As mentioned in Lambert's book, futures trading is a 0-sum game.  In other words for every winner, there is a looser.  Very briefly, futures trading involves buying and selling futures contracts...

> A futures contract, quite simply, is an agreement to buy or sell an asset at a future date at an agreed-upon price.

At the risk of oversimplifying the system, it works like this: a futures trader will buy a farmer's crop under contract at a set price in advance.  Then, the trader will turn around and sell that contract (essentially the crop) to someone else, hopefully at a higher price.  To the farmer, this is great because they lock in their corp at a given price.  If the trader is able to re-sell the contract at a higher price, then they, they pocket the difference.  If they are not able to re-sell for a profit... or worse, not resell at all... they suffer a loss.  (And the potential problem of what to do with the commodity once it has been harvested.)  

Lambert's book includes many great stories.  Be sure to check it out.

One of the interesting tools in data science is the tool of regression.  In today's blog post, I am going to explore using two different regression techniques against some commodities trading data (the cost of soybeans).  We will see how different regression techniques point to some very different potential trends.

## The Data