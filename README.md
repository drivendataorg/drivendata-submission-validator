DrivenData Submission Validator
===============================

Simple tool to run some sanity checks on submissions for DrivenData competitions before uploading. Designed to catch some of the most common errors with submission files, such as:

  * Mismatched headers
  * Wrong number of rows
  * Row IDs don't match
  * Wrong data types
  * Unexpected NaNs


Basic usage
-----------

Here is the basic usage:

    python drivendata_validator.py <your answers file> <submission format file>

The first argument is your submission that you're getting ready to upload, and the second argument is the submission format (which you downloaded from us).


Passing keyword arguments (if necessary)
----------------------------------------

There is an optional third argument in case we need to pass special keyword arguments to `pandas`:

    python drivendata_validator.py <your answers file> <submission format file> <kwargs json file>

If this JSON file is necessary, it will be provided in the same place we put the submission format.


Examples
--------

Let's say we have a very simple competition to predict the ages of six different people. The submission format file might look like this:

    person,age
    0,20
    1,20
    2,20
    4,20
    5,20

Perhaps we've data-scienced everything with a 500 layer convolutional neural network and we're ready to upload the following file:

    person,age
    0,26
    1,32
    2,19
    4,20
    5,27

We can verify that it's good to go:

    $ python drivendata_validator.py examples/example_good_submission.csv examples/example_submission_format.csv 
    Checking all of your ducks to see if they are in a row...
    
    Nice work, amig[a|o] Your submission is valid. Submit it on www.drivendata.org!

But what if something is wrong, such as in the following example? (Hint: the headers aren't exactly the same.)

    person,years.old
    0,26
    1,32
    2,19
    4,20
    5,27
    
The validator will give us an informative heads up about the problem:

    $ python drivendata_validator.py examples/bad_submission.csv examples/submission_format.csv 
    Checking all of your ducks to see if they are in a row...
    
    Caught anticipated error. Fix the below and retry.
    --------------------------------------------------
    CSV Headers do not match. Submission requires that first line is: "person,years.old" You submitted: "person,age"
