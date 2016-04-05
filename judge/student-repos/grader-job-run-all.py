#!/usr/bin/env python

import subprocess
import sys


def run_command_chain(commands):
    for command in commands:
        exitcode = subprocess.call(command, shell=True)
        if exitcode != 0:
            print "Error: command '{command}' exited with code {exitcode}.".format(**locals())
            sys.exit(exitcode)


def main():
    run_command_chain([
        "python grader-job-step-1-git-update-all.py",
        "python grader-job-step-2-copy-into-grader.py",
        "python grader-job-step-3-grade-and-deploy-reports.py"
    ])


if __name__ == "__main__":
    main()
