#!/usr/bin/env python

import os
import subprocess


def main():
    update_git_repos()


def update_git_repos():
    workdir = os.getcwd()
    repos = [os.path.join(workdir, directory)
             for directory in os.listdir(workdir)
             if os.path.isdir(directory) and os.path.isdir(os.path.join(workdir, directory, ".git"))]

    for repo in repos:
        update_git_repo(repo)


def update_git_repo(repo):
    print "-" * 30
    print "Updating {0}...".format(os.path.basename(repo))
    
    os.chdir(repo)
    output, exitcode = get_program_output("git fetch --all && git reset --hard origin/master", shell=True)
    os.chdir("..")

    print ""


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
