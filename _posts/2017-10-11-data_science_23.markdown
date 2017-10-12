---
layout: post
title:  Automated Testing in R 
date:   2017-10-10 00:09:00 -0500
categories: general
---

# Introduction

In my initial look at the R programming environment, I somehow missed information on how to do automated testing.  You can do testing in R quit easily.  The purpose of this blog post is to explore how to do basic automated testing in R.  This post will focus on using the "testthat" package.

#  Setting things up

I will be using version 1.0.2 of [the "testthat" package](https://github.com/r-lib/testthat) and [R Studio](https://www.rstudio.com/) version 1.1.383.    Before the "testthat" package can be used, it must first be installed.  That can be done as follows:

```
install.packages("testthat")
```

Note, if you ever need to see what packages you have installed in R, you can use this handy script.

```
ip <- as.data.frame(installed.packages()[,c(1,3:4)])
rownames(ip) <- NULL
ip <- ip[is.na(ip$Priority),1:2,drop=FALSE]
print(ip, row.names=FALSE)
```

This will result in a nicely formatted display of all installed packages and their versions:

```
      Package  Version
...
     testthat    1.0.2
...
```

# Starting with Tests

To start with a simple case, consider a function that returns the factorial of a value.  Rather than just start by writing code, let's see if we can test drive this feature.  Lets consider some test cases for what we would want the code to do.

```
Test Cases:
f(1) = 1 * 1 = 1
f(2) = 2 * 1 = 2
f(3) = 3 * 2 * 1 = 6  
```

Next we need to take a few steps to set up our testing directory structure.  The directory structure that I settled on looks like the following.

![RUnitTesting]({{ site.url }}/images/factorial_dir_structure.png)

This structure will work in conjunction with a program that acts as a harness to run the tests.  I named the test harness file run_tests.R, and it contains the following code:

```
library(testthat) 

source("/Users/milesporter/data-science/R_testing/factorial.R")

test_results <- test_dir("/Users/milesporter/data-science/R_testing/test/")
```

As is probably clear from the above short script, the "testthat" library will pick up tests that are in the folder specified in the call to test_dir().  The source statement specifies the thing that we are actually testing.  In this case we will be running our tests against the code in the factorial.R file.

> Warning:  This approach will load the code in the source() call...  however, the code that is loaded by source() does not automatically get unloaded.  You can see this clearly if you run your tests in RStudio.  The environment tab will show those functions that are available in the environment.  Before running the test for the first time, the factorial function is not listed.  However, after running the test, factorial() is left hanging around.  Tests that don't clean up after themselves are the bane of any TDDer.  It is not hard to overcome...  if you realize it is happening.

Lastly we need a file that we want to test.  At this point we might be tempted to write code that makes the test pass.  However, it is a good practice to write just enough code so that the test runs, but the tests themselves fail.  After you have a failing test, you can then go back and make the test pass.  One reason for doing this is that by writing the code so that the test fails, you can be assured that you are actually running the test.  For more info on the TDD practice, check out [this blog post on the agile alliance site](http://tinyurl.com/yczhe765).

Here is a simple function that runs, but fails our tests.  Some would say that this code "fails in a good way."

```R
factorial <- function(n)
{
  return(0)
}
```

With this code in place I can now run my test, and it fails as expected.

```R
> library(testthat) 
> 
> source("/Users/milesporter/data-science/R_testing/factorial.R")
> 
> test_results <- test_dir("/Users/milesporter/data-science/R_testing/test/")
123.
Failed -------------------------------------------------------------------------------------
1. Failure: Test factorial (@test_factorial.R#2) -------------------------------------------
factorial(1) not equal to 1.
1/1 mismatches
[1] 0 - 1 == -1


2. Failure: Test factorial (@test_factorial.R#3) -------------------------------------------
factorial(2) not equal to 2.
1/1 mismatches
[1] 0 - 2 == -2


3. Failure: Test factorial (@test_factorial.R#4) -------------------------------------------
factorial(3) not equal to 6.
1/1 mismatches
[1] 0 - 6 == -6


DONE =======================================================================================
```

In order to get my test to pass, I just need to implement the functionality in factorial.R and re-run my tests:

Here is the code under test:

```R
factorial <- function(n)
{
  if (n==0)
  {
    return(1)
  }
  else
  {
    return(n*factorial(n-1))
  }
}
```

Now when I run the run_test.R script, I can see that there are no error messages.

```R
> library(testthat) 
> 
> source("/Users/milesporter/data-science/R_testing/factorial.R")
> 
> test_results <- test_dir("/Users/milesporter/data-science/R_testing/test/")
....
DONE =======================================================================================
```

One of the nice things about the R "testthat" framework is that the test_dir function allows us to run all tests in a given directory.  This is particularly nice if we have many tests that we want to run.  It also makes it easy to "regression test" our code.  Once we have added a file to the testing directory, it gets included every time we run our tests.

# Conclusion

In summary, we have seen how we can use testthat in R Studio to effectively unit test R code.

This was a pretty high level view of "testthat".  Some of the things that I didn't show in this post were:

-  validating exceptions
-  testing R packages
-  using automated testing in conjunction with continuous deployment

Some of those topics are covered in more detail in these blog posts:

- [R-Bloggers post on unit testing](https://www.r-bloggers.com/unit-testing-with-r/)
- [John Miles White's blog](http://www.johnmyleswhite.com/notebook/2010/08/17/unit-testing-in-r-the-bare-minimum/)

Also this book contains some resources for testing R packages:

- [R Packages by Hadley Wickham](http://r-pkgs.had.co.nz/)


Check back soon.  For my next blog post, I am planning on extending the basic R unit testing concepts to R packages.

Miles.








