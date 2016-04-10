# Place your custom verifier classes here, or create a dedicated .py file in this folder.

from hammurabi.grader.model import *
from hammurabi.grader.verifiers.common import AnswerVerifier


class GovernVerifier(AnswerVerifier):
    def __init__(self):
        super(GovernVerifier, self).__init__()

    def verify(self, testrun):
        certificates = set()
        prerequisites = {}

        with open(testrun.testcase.input_filename, "r") as input_file:
            for line in input_file:
                certificate, dependency = line.strip().split()
                if certificate not in prerequisites:
                    prerequisites[certificate] = set()
                certificates.add(certificate)
                certificates.add(dependency)
                prerequisites[certificate].add(dependency)

        have_certificates = set()

        with open(testrun.answer_filename, "r") as given_answer_file:
            for line in given_answer_file:
                certificate = line.strip()
                if certificate not in certificates:
                    testrun.result = TestRunFormatErrorResult(message="Unknown certificate: '{0}'".format(certificate))
                    return False
                if certificate in prerequisites and len(prerequisites[certificate].intersection(have_certificates)) < len(prerequisites[certificate]):
                    message = "Not all prerequisites for '{certificate}' have been satisfied.".format(**locals())
                    testrun.result = TestRunWrongAnswerResult(custom_message=message)
                    return False

                have_certificates.add(certificate)

        if len(have_certificates) != len(certificates):
            testrun.result = TestRunWrongAnswerResult(custom_message="The number of output certificates does not match the number of input certificates.")
            return False

        testrun.result = TestRunCorrectAnswerResult()
        return True
