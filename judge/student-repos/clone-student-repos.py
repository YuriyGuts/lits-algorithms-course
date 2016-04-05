#!/usr/bin/env python

import subprocess
import sys


def main():
    student_repos = {
        "johndoe": "https://github.com/johndoe/algorithms",
        "janedoe": "https://github.com/janedoe/algorithms"
    }

    for name, url in student_repos.iteritems():
        subprocess.call("git clone {url} {name}".format(**locals()), shell=True)


if __name__ == "__main__":
    main()
