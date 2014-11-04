![](https://drivendata.s3.amazonaws.com/images/drivendata.png)

DrivenData Submission Validator
===============================

Simple tool to run some sanity checks on submissions for [DrivenData](http://www.drivendata.org/) competitions before uploading. Designed to catch some of the most common errors with submission files, such as:

  * Mismatched headers
  * Wrong number of rows
  * Row IDs don't match
  * Wrong data types
  * Unexpected NaNs

Requirements
------------

There are two requirements for the validator:

 * Python: https://wiki.python.org/moin/BeginnersGuide/Download
 * `pip`: install with `python get-pip.py`


Installation
------------

You can install the validator using `pip` directly from github. Just run the command below:

```
pip install git+https://github.com/drivendataorg/drivendata-submission-validator.git
```

The command installs the validator to your `site-packages` directory so that you can import it with `import drivendata_validator` or run it from the command line with `dd-sub-valid`.

Basic usage
-----------

Here is the basic usage:

    dd-sub-valid <your answers file> <submission format file>

The first argument is your submission that you're getting ready to upload, and the second argument is the submission format (which you downloaded from us).


Passing keyword arguments (if necessary)
----------------------------------------

There is an optional third argument in case we need to pass special keyword arguments to `pandas`:

    dd-sub-valid <your answers file> <submission format file> <kwargs json file>

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

    $ dd-sub-valid examples/example_good_submission.csv examples/example_submission_format.csv 
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

    $ dd-sub-valid examples/bad_submission.csv examples/submission_format.csv 
    Checking all of your ducks to see if they are in a row...
    
    Caught anticipated error. Fix the below and retry.
    --------------------------------------------------
    CSV Headers do not match. Submission requires that first line is: "person,years.old" You submitted: "person,age"


Using the validator in your workflow
-------------

You can also use the validator as part of your python workflow by importing it. The usage is the same as at the commandline:

```python
from drivendata_validator import DrivenDataValidator

# no parameters unless we have a read_csv kwargs file
v = DrivenDataValidator()
```

There are two methods you can use on the `DrivenDataValidator` object. The first, `validate`, raises exceptions if there is anything wrong with the submission.

```python
v.validate('examples/submission_format.csv', 'examples/bad_submission.csv')
```

The above raises a `DrivenDataValidationError`. If your submission passes, it will return a pandas dataframe of your submission.

The second method is `is_valid` and it returns a `bool` so you can just use it for pass/fail. It calls `validate` internally. Optionally, it has a `print_errors` kwarg so that you can print the exception messages on failure.

```python
if v.is_valid('examples/submission_format.csv', 'examples/bad_submission.csv'):
    print "I am awesome."
else:
    print "I am not so cool."
```

The above prints "I am not so cool." If we also passed the parameter `print_errors=True`, then it would also print the exception method.



