#!/usr/bin/env python

import json
import subprocess
import sys


def main():
    with open("grader-job.conf", "r") as job_conf_file:
        job_conf = json.loads(job_conf_file.read())
        student_repos = job_conf["student_repos"]

    for name, url in student_repos.iteritems():
        subprocess.call("git clone {url} {name}".format(**locals()), shell=True)


if __name__ == "__main__":
    main()
