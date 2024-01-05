---
layout: post
title:  "Collaborative Filtering for Mere Mortals!"
date:   2024-01-05 00:09:00 -0800
categories: general
---

# A mere mortals guide to collaborative filtering.  

I recently went thru an advanced course on Google on collaborative filtering.  It was good, but DANG.  It was a little mathematically intense.  I thought I would go thru a similar exercise here to show how collaborative filtering can be used to make recommendations... and give a very basic code example.  For my example, I will use a MovieLens dataset similar to the one in the Google example.  I will use some comments from the approach outlined in "Data Mining for Business Analytics" by Shmueli, Bruce, Yahav, Patel, and Lichtendahl (ISBN 978-1-118-87936-8).  The approach specified in that text has examples in R, which are great... if you like R.  For those that don't, I will conclude this post with an example that uses the open-source Surprise package (Simple Python Recommendation System Engine).

## First, some background:

As outlined in the Google course, recommendation systems often typically have a three phase approach.  These phases include candidate generating, scoring and re-ranking.  In the candidate generation phase, two approaches; content-based filtering and collaborative filtering are used.  The goal of the candidate phase is to reduce the number of possible matches down to some reasonable number so that they can be scored.  

> For the sake of this discussion, we will use the terms "users" and "items" to represent the things that we are recommending to, and the things that we are recommending respectively.  

Content-based filtering focuses on similarities between items.  The example used in the Google tutorial is "If user A watches two cute cat videos, then the system can recommend cute animal videos to that user."  This approach has one big advantage in that the model doesn't need to worry about other users.  However, the model also requires that all the "items" have been tagged, and the quality of the results depends heavily on that tagging.

Collaborative-based filtering, on the other hand doesn't require prior tagging.  In this approach similarities between users drives the recommendations.  One of the big challenges of collaborative based filtering include the fact that the model cannot include new items.  This is referred to as the cold-start problem.  There are a few techniques that can help address this and other issues including WALS.  I am going to defer discussion on that approach for another blog post.  Ultimately, Collaborative based filtering has one huge advantage over content based filtering, and that is that it can make recommendations that seem "serendipitous."  For example, a user might enjoy watching cat videos and the system recommends other videos on knitting.  That association was "discovered" because other users that liked cat videos also liked knitting videos.  (It could happen.  Just sayin'.)

## The Basics of Collaborative Filtering:

There are two flavors of collaborative filtering, user-based and item-based.  In User based collaborative the algorithm follows these steps:

## User-based collaborative filtering:

1.  Identify those users that are most like the user of interest.
2.  Consider only those items that the user of interest has NOT purchased or ranked yet.
3.  Use the similar users items to recommend possible items to the user of interest.

## Item-based collaborative filtering:

The user-based approach is straight forward, but suffers from a big problem if the number of users is very large.  Namely, the first step can be very costly in terms of compute.  A less expensive approach is to do the filtering based on the items instead.  That approach has the following steps:

1.  Identify the ITEMS that were co-rated or co-purchased by any user with the item of interest.
2.  Recommend the most popular item or correlated item(s) among the similar items.  
3.  For any given user, look at their items... and let those items recommend other items.

For the purpose of this exploration we will continue with the item-based collaborative filtering approach.

## A Little Math:

In order to determine the items in step 1, we need to come up with some metric to measure how similar items are.  The metric often used for this is referred to as the Pearson correlation metric.  Euclidean can also be used, but "does not perform well for collaborative filtering as some other measures" (Shmueli, et al.  Pg 345.)  This is explained in some detail in the Google tutorial mentioned at the beginning of this post, and I won't elaborate on it further here in the interest of time.  (Not that you haven't fallen asleep already unless you are a super data analytics nerd like me.  :) )

The Pearson Correlation metric can be expressed as...

$$ Corr(I_1, I_2) = \frac {\sum(r_{1,i} - \bar r_1)(r_{2,i} -\bar r_2)} {\sqrt{\sum(r_{1,i} - \bar r_1)^2} \sqrt{\sum(r_{2,i} - \bar r_2)^2}} $$

('cause it ain't a good blog post without out some painful LaTeX, right?)

That is great, but what does it mean?  It is important to understand that what we are really building behind the scenes is a matrix that associates users with items.  Our matrix, initially, is a very sparse because not every user has ranked every item.  The goal of the recommendation system, then, is to attempt to fill in the blanks in the matrix.  In order to do that, we can use a singular value decomposition approach (SVD) that generates three matricies, U, S, and V.  The U matrix represents the users, the V matrix represents the items, and the S matrix is diagonal matrix that is comprised of singular value such that the product of U,S and V approximates the original ratings matrix... with the gaps filled in.

Doing this requires a good deal of code that can potentially be very non-performant.  But, fear not... there are packages that make this entire process easy, performant and less error prone.  One such package for Python is the Surprise package.


## Doing This With Code (the easy way):

Fortunately, a number of packages make this process much easier than having to do it by hand.  The Surprise python package is a popular package for doing recommendation.  The following example shows how it can be used.  This example loads data from the ml-100k dataset, which can be found here: (https://grouplens.org/datasets/movielens/100k/0)

The following code loads the movie recommendations, uses the Singular Value Decomposition (SVD) algorithm to solve the recommendation matrix (this is also discussed in the Google tutorial), and displays the results of the predictions of the first 10 records in the test set.  (Note that there is a test/train split involved in the code.)

The data in the training set has values of 0.5 - 5.0  This indicates the "score" that the given user gave the given item.  In some recommendation systems, this score could be binary.

The results are pretty accurate, typically within 1 of the actual ranking provided by the user in the training set.


<pre>

import os
import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise.model_selection import cross_validate
from surprise.model_selection import train_test_split

class Recommender:

    def movie_rating_prediction(self):
        # Load the data
        reader = Reader(line_format='user item rating timestamp', sep='\t')
        movie_data = Dataset.load_from_file('data/ml-100k/u.data', reader=reader)

        # Perform cross-validation
        algo = SVD()
        cross_validate(algo, movie_data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

        # Train and test the algorithm
        trainset = movie_data.build_full_trainset()
        algo.fit(trainset)
        testset = trainset.build_testset()
        predictions = algo.test(testset)

        # Load movie titles
        movies = pd.read_csv('./data/ml-100k/u.item', sep='|', encoding='latin-1', header=None, usecols=[0, 1], names=['item', 'title'])

        # Display the item name, predicted rating, and actual rating for the first 10 rows in the test set
        print("\nItem Name, Predicted Rating, Actual Rating")
        for idx, pred in enumerate(predictions[:10]):
            movie_title = movies[movies['item'] == int(pred.iid)]['title'].values[0]
            print(f"{movie_title}, {pred.est:.2f}, {pred.r_ui:.2f}")


if __name__ == '__main__':
    recommender = Recommender()
    recommender.movie_rating_prediction()

</pre>

Running this code produces the following results:  

<pre>
Evaluating RMSE, MAE of algorithm SVD on 5 split(s).

                  Fold 1  Fold 2  Fold 3  Fold 4  Fold 5  Mean    Std     
RMSE (testset)    0.9432  0.9384  0.9431  0.9277  0.9324  0.9370  0.0061  
MAE (testset)     0.7432  0.7379  0.7443  0.7331  0.7341  0.7385  0.0046  
Fit time          1.02    1.04    1.02    1.01    1.19    1.06    0.07    
Test time         0.15    0.14    0.14    0.14    0.20    0.15    0.02    

Item Name, Predicted Rating, Actual Rating
Kolya (1996), 3.91, 3.00
Mrs. Doubtfire (1993), 3.48, 4.00
Muriel's Wedding (1994), 3.50, 4.00
Shall We Dance? (1996), 4.17, 3.00
Stand by Me (1986), 4.14, 5.00
Ace Ventura: Pet Detective (1994), 3.66, 5.00
Mrs. Brown (Her Majesty, Mrs. Brown) (1997), 3.71, 4.00
Raising Arizona (1987), 3.62, 4.00
Being There (1979), 4.30, 5.00
Truth About Cats & Dogs, The (1996), 3.61, 4.00
</pre>

## Conclusion:

In this post, I have outlined some of the steps used in typical recommendation systems.  We have discussed the difference between content-based filtering and collaborative-based filtering. From there, we took a look at some of the math (Pearson's correlation) and also how Singular Value Decomposition can be used to generate recommendations.  Lastly, we took a look at how the Surprise package in python can be used to easily implement a recommender system based on movie scores.

It should be mentioned here that the approach above is based on solving the user item matrix.  Other approaches also exist, including using deep neural networks.  I will save that discussion for another day.

I hope you have enjoyed this post!  Until next time...  

Miles
