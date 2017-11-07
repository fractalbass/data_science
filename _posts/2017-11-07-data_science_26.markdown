---
layout: post
title:  "Central Limit Theorem, Standard Deviation and Hadoop Combiners"
date:   2017-11-07 00:09:00 -0500
categories: general
---
# Central Limit Theorem and Hadoop Combiners.


![Paintchipart]({{ site.url }}/images/paintchipart.jpeg)<br>
Paintchip Art by [Peter Combe](https://www.ignant.com/2014/10/21/paint-chip-art-by-peter-combe/)

## Introduction



One of the fundamental concepts of statistics is the central limit theorem, which states:

> If a sequence of Independent identically distributed random variables each has a finite variance, then as their number increases, their sum (or, equivalently their arithmetic mean) approaches a normally distributed random variable. (1)

In this post, we will explore how the Central Limit Theorem relates to one of the quizzes of the Udacity Hadoop Mapreduce course.  I believe that the course sets a pretty dangerous precedent with it's very brief, and very wrong implementation of using a mean function as both a reducer and combiner.

## Udacity Hadoop Combiners Quiz

I recently finished a quiz in the Udacity Hadoop MapReduce online course.  The quiz was on combiners and basically focused on showing how using combiners can be used to optimize mapreduce jobs.  

The quiz used a data set that contains product sales information.  Each record in the set represents an individual item sold and includes, among other things, the cost of the item and the date.  The exercise focuses on showing how computing the average sales by day of week can be optimized by using combiners.  

[This site contains a nice overview of what is going on with Hadoop combiners.](https://www.tutorialspoint.com/map_reduce/map_reduce_combiners.htm)

In the exercise, the student first runs a mapper that outputs each sale as the combination of a day of week as the key, and the value of the sale.  My mapper looks like this:

```python
class DOWMapper():

    logging.basicConfig(filename='mapper.log')
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    sysin = sys.stdin
    sysout = sys.stdout

    def save_data(self, key, value):
        self.sysout.write("{0}\t{1}\n".format(key, value))

    def parse_date_amt(self, line):
        amt = None
        weekday = None
        try :
            fields = line.split('\t')
            weekday = datetime.strptime(fields[0], "%Y-%m-%d").weekday()
            amt = fields[4]
        except Exception as ex:
            logging.WARN("Error {0} raw data: {1}".format(ex.message, line))
        return self.days[weekday], float(amt)

    def map(self):

        for line in self.sysin:
            amt, weekday  = self.parse_date_amt(line)
            self.save_data(amt, weekday)

#Do the work
if __name__ == "__main__":
    mapper = DOWMapper()
    mapper.map()
```

The reducer then computes the average amount of sales for each day of the week...

```python
class DOWReducer():

    sysin = sys.stdin
    sysout = sys.stdout

    def save_data(self, key, value):
        self.sysout.write("{0}\t{1}\n".format(key, value))

    def get_average(self, l):
        total = 0
        for x in l:
            total = total + x
        return total/len(l)
...

    def reduce(self, q):
        result = None
        current_day = None
        day_sales = list()
        count_days = 0
        for line in self.sysin:
            fields = line.split()
            if len(fields) == 2:
                if current_day is None:
                    current_day = fields[0]

                if fields[0] != current_day:
                    #Done with this day.  Summarize and print
                    ave = self.get_average(day_sales)
                    self.save_data(current_day, ave)
                    if current_day == q:
                        result = ave
                    day_sales = [float(fields[1])]
                    current_day = fields[0]

                else:
                    day_sales.append(float(fields[1]))

        ave = self.get_average(day_sales)
        self.save_data(current_day, ave)
        if current_day == q:
            result = ave
        return result
```

You may wonder why I have written my own function to return an average.  Keep in mind that I am dealing with python 2.6 because the Udacity virtual box image is running on an ancient version of CentOS.  (See my previous post.)

At any rate, the mapper and reducer produce the following results:

```text
Friday	250.223089314
Monday	250.009331149
Saturday	250.084703253
Sunday	249.946443251
Thursday	249.872024327
Tuesday	249.738227929
Wednesday	249.851167194
```

Again, this shows the average sales by the day of the week for the overall dataset.

The point of the exercise was to use the reducer as a combiner as well to improve performance.  To see how that works, let's first check out the number of input records that the reducer had to process for this job:

![Reducer input 1]({{ site.url }}/images/reducer_input_1.png)

Mapreduce jobs consist of multiple mappers but only a single reducer.  For calculating some statistical values, this can be an issue as it puts a lot of computation burden on the reducer.  In order to get around that, combiners can be used.  In the case of the quiz in Udacity, the student is asked to used the reducer as the combiner as well.  The results of doing this are that the workload on the final reducer is much lighter and the job finishes more quickly.

![Reducer input 2]({{ site.url }}/images/combine_reduce_input.png)

As you can see from the above screen shot, the reducer has a significantly smaller workload (28 vs 298,218) when running with combiners.

However, if we look at the resulting data we can see something pretty shocking...  The result are actually different!

```text
Friday	250.555395612
Monday	250.165178255
Saturday	250.248274952
Sunday	249.878222802
Thursday	249.707828286
Tuesday	249.614816971
Wednesday	249.640674892
```

## What is happening?!

Essentially the combiner is acting as a sampler for the data, and the reducer is summarizing the data back from those samples.

Consider this example:

Let's save I have a population of really boring numbers [1,2,3,4,5,6,7,8].

Now, let's say that I break the data up into samples of different sizes.  It just so happens that my samples cover the entire set and are not random, but that is fine.  In fact it is exactly what the Hadoop combiner is doing; grouping up the results of the various mappers into samples.

Here are my samples:
<pre>
[1,2], average = 1.5
[3], average = 3
[4,5,6], average = 5
[7,8], average = 7.5
</pre>

Here the average of the sample means is 4.25.  However, the average of the entire population is 4.5.

In the case of the Udacity quiz, we have no idea if the combiners are actually sampling the same number of records.  And, even if they were, the central limit theorem states that the distribution of multiple samples of the same size would be normal.  We cannot simply take random samples from our population, take the mean of the means and say that is the same as the overall all average.  

The point of the exercise is to show that combiners can help reduce the bottleneck created by a single reducer.  I get that.  It still bothers me a little bit that what they were doing sets a bad precedent for a way to compute the population mean.

## A Few Words About Standard Deviation

While planning this post, I had originally planned to look at the combiner quiz question, but used standard deviation rather than sample mean.  I did that because I thought that using a standard deviation reducer also as a combiner would cause problems.  After working with this, I realized that I didn't even need to go that far.  However, I wanted to take a moment and explore the issue of calculating the standard deviation of the overall population using a single reduce job.

First off, I wanted to start with a test for calculating the standard deviation of a list.  Again, numpy would have made this trivial... but I am forced to run on Python 2.6.  So, here is my test:

```python
    def test_reducer_stdev(self):
        reducer = Reducer()
        l = [1,2,3,4,5,6]
        stdev = reducer.get_stdev(l)
        self.assertTrue(stdev==1.707825127659933)
```

Is it a perfect test?  No.  But it will work for my purposes here.

Here is the code to satisfy the test:

```python
    def get_stdev(self, l):
        total = 0.0
        for x in l:
            total = total + x
        a = total/len(l)
        v = 0.0
        for x in l:
            v = v + math.pow((a - x),2)

        stdev = math.sqrt(v/len(l))
        return stdev
```

One thing to note is that I have implemented the standard deviation of a population, not a sample.  They are different.  The population version of standard deviation is computed by first computing the variance for a set of data.  The variance is the sum of the square of the difference of each value in the set to the mean.  The standard deviation is then the square root of the variance.  A sample standard deviation is computed by using a different formula. For more info on the difference between sample and population standard deviation [check out this reference at statistics.leard.com](https://statistics.laerd.com/statistical-guides/measures-of-spread-standard-deviation.php)

Now, when I use the above technique and compute the standard deviation of sales by day of week WITHOUT combiners, I get the following:

<pre>
Friday	144.367101002
Monday	144.321171506
Saturday	144.401207177
Sunday	144.330561505
Thursday	144.339164506
Tuesday	144.205156383
Wednesday	144.255242005
</pre>

Which is a dramatically different result than if we use the reducer also as a combiner:

<pre>
Friday	62.4788765514
Monday	62.2390897986
Saturday	62.356315781
Sunday	62.3390116105
Thursday	62.3801593718
Tuesday	62.4122299749
Wednesday	62.2977859358
</pre>

# Conclusion

Hadoop combiners provide an excellent way to optimize results in map reduce jobs.  That said, it is vital that data scientists and big data engineers keep in mind some of the basic rules of statistics when using combiners.  The Udacity course only offers a very brief introduction to the topic, and they set a dangerous precedent for using combiners in conjunction with statistical methods for computing population means.

I hope you have enjoyed this exploration of statistics and Hadoop combiners.  Stay tuned for more topics in data science, machine learning, and related topics.

The code, such that it is, is available in my github repo:

[udacity_hadoop_playground](https://github.com/fractalbass/udacity_hadoop_playground)


## More Resources

- (1)  Harper Collins Dictionary of Mathematics. ISBN 0-06-271525-9
- Statistics, The Exploration and Analysis of Data.  ISBN  0-314-93172-4
- [Leard.com Post on Standard Deviation](https://statistics.laerd.com/statistical-guides/measures-of-spread-standard-deviation.php)
- [calculator.net page for computing standard deviation](http://www.calculator.net/standard-deviation-calculator.html?numberinputs=1%2C2%2C3%2C4&x=57&y=15)
- [Youtube video on Central Limit Theorem](https://www.youtube.com/watch?v=JNm3M9cqWyc) 