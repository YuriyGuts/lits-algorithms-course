#!/usr/bin/env python

import json
import os
import re
import subprocess
import sys


# An S3 bucket where the reports are hosted as a static website.
# The access keys will be taken from ~/.aws
s3_bucket = "To be loaded from grader-job.conf"
s3_region = "To be loaded from grader-job.conf"

# Assuming that hammurabi root is "../hammurabi".
hammurabi_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, "hammurabi"))
hammurabi_cmd = "python hammurabi.py grade"


def main():
    with open("grader-job.conf", "r") as job_conf_file:
        job_conf = json.loads(job_conf_file.read())
        s3_bucket = job_conf["aws_s3_bucket"]
        s3_region = job_conf["aws_s3_region"]

    report_dir = grade_solutions()
    exitcode = upload_reports_to_s3(report_dir, s3_bucket, s3_region)
    sys.exit(exitcode)


def grade_solutions():
    print
    print "Grading..."
    print

    grader_output, exitcode = get_program_output(hammurabi_cmd, cwd=hammurabi_root, shell=True)
    report_dir = ""

    for line in grader_output:
        match = re.search("CSV log: (.*)testruns.csv", line)
        if match:
            report_dir = match.group(1)

    if report_dir is None or report_dir.strip() == "":
        print "Cannot extract report folder from grader output."
        sys.exit(1)

    return report_dir


def upload_reports_to_s3(report_dir, bucket, region):
    print
    print "Uploading to S3..."
    print

    s3_upload_cmd = "aws s3 cp {report_dir} s3://{bucket}/ --recursive --exclude \"*\" --include \"*.csv\" --include \"*.html\" --include \"*.css\" --region {region}".format(**locals())
    print s3_upload_cmd

    _, s3_exit_code = get_program_output(s3_upload_cmd, shell=True)
    return s3_exit_code


def get_program_output(cmd, echo=True, *args, **kwargs):
    output = []

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, *args, **kwargs)
    output_iterator = iter(process.stdout.readline, b"")

    for line in output_iterator:
        output.append(line)
        if echo:
            print(line.strip("\n"))

    process.communicate()
    return output, process.returncode


if __name__ == "__main__":
    main()
