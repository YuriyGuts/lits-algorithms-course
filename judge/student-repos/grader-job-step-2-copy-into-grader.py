#!/usr/bin/env python

import json
import os
import shutil


def main():
    with open("grader-job.conf", "r") as job_conf_file:
        job_conf = json.loads(job_conf_file.read())
        problem_whitelist = job_conf["problem_whitelist"]

    # Assuming the repos are in the current folder.
    student_repos_root = os.path.dirname(os.path.abspath(__file__))
    
    # Assuming Hammurabi root is "../hammurabi".
    # Detecting problem root from Hammurabi config.
    hammurabi_root = os.path.abspath(os.path.join(student_repos_root, os.path.pardir, "hammurabi"))
    hammurabi_conf = os.path.join(hammurabi_root, "hammurabi", "conf", "grader.conf")
    try:
        with open(hammurabi_conf, "r") as conf_file:
            conf = json.loads(conf_file.read())
            grader_problem_root = conf["locations"]["problem_root"]
            if not os.path.isabs(grader_problem_root):
                grader_problem_root = os.path.join(hammurabi_root, "hammurabi", grader_problem_root)
        print "Detected problem root:", grader_problem_root
    except:
        grader_problem_root = os.path.abspath(os.path.join(student_repos_root, os.path.pardir, 'problems'))
        print "Could not read problem root from config. Assuming", grader_problem_root

    # Copying student solutions into problem root.
    for student_name in [subdir for subdir in os.listdir(student_repos_root)]:
        student_dir = os.path.join(student_repos_root, student_name)
        if not os.path.isdir(student_dir):
            continue

        for problem_name in [subdir for subdir in os.listdir(student_dir)]:
            problem_dir = os.path.join(student_dir, problem_name)
            if not os.path.isdir(problem_dir) or problem_name not in problem_whitelist:
                continue

            grader_problem_dir = os.path.join(grader_problem_root, problem_name)
            grader_student_dir = os.path.join(grader_problem_dir, "solutions", student_name)

            try:
                shutil.rmtree(grader_student_dir, ignore_errors=False)
            except:
                pass

            print "Copying: student '{student_name}', problem '{problem_name}'".format(**locals())
            shutil.copytree(problem_dir, grader_student_dir)


if __name__ == "__main__":
    main()
