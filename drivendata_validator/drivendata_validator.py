#!/usr/bin/python2

import sys
import json

import pandas as pd
import numpy as np


class DrivenDataValidationError(Exception):
    """ Custom Exception class for validation errors that we can anticipate. These messages
        are returned to the user. Other unanticipated exceptions get a generic message we pass to the user.
    """

    def __init__(self, message, errors=None):
        # Call the base class constructor with the parameters it needs
        super(DrivenDataValidationError, self).__init__(message)

        self.errors = errors


class DrivenDataValidator(object):
    """ Validator class.

        Accepts a dictionary that is passed to pandas.read_csv -- for options see:
        http://pandas.pydata.org/pandas-docs/stable/generated/pandas.io.parsers.read_csv.html
    """

    def __init__(self, **read_csv_kwargs):
        self.validation_kwargs = read_csv_kwargs

        # default validation kwargs for pd.read_csv() if read_csv_kwargs is empty
        if not self.validation_kwargs:
            self.validation_kwargs = {
                "index_col": 0,
                "skipinitialspace": True
            }

    def validate(self, format_path, submission_path, skip_validating_dataset=False):
        """ Validates that a submission is in the proper format

        :param format_path: a string that is the path to the submission format file
        :param submission_path: a string that is the path to the actual submission to validate
        :return: The data frame for the submission if we pass
        """

        # load the data
        format_df = pd.read_csv(format_path, **self.validation_kwargs)

        # automatically validate and return the dataframe if we're comparing something to itself.
        # Refs:
        #  - Aristotle's law of identity, 'Metaphysics', 1st century CE
        #  - "A is A." - 'Atlas Shrugged', Ayn Rand, 1957  <- lulz
        #
        if format_path == submission_path:
            return format_df

        submission_df = pd.read_csv(submission_path, **self.validation_kwargs)

        # just return the unadulterated df if we know this is what we're after
        if skip_validating_dataset:
            return submission_df

        # verify that the headers match
        if np.any(format_df.columns.values != submission_df.columns.values):
            error_str = 'CSV Headers do not match. Submission requires that first line is: "{}" You submitted: "{}" '

            # get all of the headers
            format_headers = [format_df.index.name if format_df.index.name else ""] + \
                             format_df.columns.values.tolist()

            sub_headers = [submission_df.index.name if submission_df.index.name else ""] + \
                          submission_df.columns.values.tolist()

            raise DrivenDataValidationError(error_str.format(",".join(format_headers),
                                                             ",".join(sub_headers)))

        # verify the submission has the proper number of rows
        if len(format_df.index) != len(submission_df.index):
            error_str = 'Submission has {} rows but should have {}.'
            raise DrivenDataValidationError(error_str.format(len(submission_df.index),
                                                             len(format_df.index)))

        # verify the submission has the right row ids
        if np.any(format_df.index.values != submission_df.index.values):
            error_str = 'IDs for submission are not correct.'
            raise DrivenDataValidationError(error_str)

        # verify that the dtypes parse properly
        if np.any(format_df.dtypes != submission_df.dtypes):
            error_str = "Unexpected data types in submission. " \
                        "\n Expected dtypes: \t'{}' \n Submitted dtypes: \t'{}'"
            raise DrivenDataValidationError(error_str.format(format_df.dtypes.values.tolist(),
                                                             submission_df.dtypes.values.tolist()))

        # verify that there are no nans if we don't expect any nans (pd.isnull handles all dtypes)
        if pd.isnull(submission_df.values).any() and not pd.isnull(format_df.values).any():
            error_str = 'Your submission contains NaNs or blanks, which are not expected. Please change these to ' \
                        'numeric predictions. See ids: {}'

            # figure out which rows contain nans
            nan_mask = pd.isnull(submission_df.values).astype(int).sum(axis=1).astype(bool)
            nan_ids = submission_df.index.values[nan_mask]

            raise DrivenDataValidationError(error_str.format(nan_ids.tolist()))

        return submission_df

    def is_valid(self, format_path, submission_path, print_errors=False):
        """ A wrapper around validate to return True/False
        """
        try:
            self.validate(format_path, submission_path)
            return True
        except Exception as e:
            if print_errors:
                print e.message

            return False

def main():
# args are submission format, submission file, [optional] kwargs_json
    if len(sys.argv) not in [3, 4]:
        print "Usage: python DrivenDataValidator.py <path_to_submission_format_file> " \
              "<path_to_your_submission_file> [<path_to_pandas_read_csv_kwargs_json>]"

    else:
        print "Checking all of your ducks to see if they are in a row...\n"

        read_csv_kwargs = {}
        if len(sys.argv) == 4:
            with open(sys.argv[3], "r") as json_file:
                read_csv_kwargs = json.load(json_file)

        try:
            validator = DrivenDataValidator(**read_csv_kwargs)
            validator.validate(sys.argv[1], sys.argv[2])
            print "Nice work, amig[a|o] Your submission is valid. Submit it on www.drivendata.org!"

        except DrivenDataValidationError as anticipated_error:
            print "Caught anticipated error. Fix the below and retry."
            print "--------------------------------------------------"
            print anticipated_error.message

        except Exception as e:
            print "Unanticipated error. What have you done??"
            print "-----------------------------------------"

            # re-raise so y'all can read the trace
            raise

if __name__ == "__main__":  # pragma: no cover (NB: tested with subprocess, so we don't see the coverage)
    main()