#!/usr/bin/env bash

# Read command line parameters.
if [ $# -eq 0 ]
then
    echo "Error: specify TASKID to test."
    echo ""
    echo "Example:"
    echo "    judge.sh echoer"
    exit 1
fi
PROBLEM_CODE=$1

# Set base variables.
ROOT_DIR=`pwd`
PROBLEM_DIR=$ROOT_DIR/$PROBLEM_CODE

# Iterate over students.
for STUDENT_DIR in $PROBLEM_DIR/solutions/*/
do
    STUDENT_NAME=${STUDENT_DIR%*/}
    STUDENT_NAME=${STUDENT_NAME##*/}

    if [ -z "$2" ] || [ "$2" == "$STUDENT_NAME" ]; then
        echo ""
        echo "Testing student: $STUDENT_NAME"

        cd $STUDENT_DIR

        # Clean files from the previous run.
        rm -rf output 2>/dev/null
        mkdir output
        mkdir output/stdout
        mkdir output/stderr

        # Compile student's solution.
        if [ -f compile.sh ]
        then
            echo "    Compiling"
            bash compile.sh
        fi

        # Iterate over test cases.
        for TEST_CASE in $PROBLEM_DIR/testcases/*.in
        do
            TEST_CASE_BASENAME="`basename $TEST_CASE`"
            TEST_CASE_NUMBER="${TEST_CASE_BASENAME%.*}"

            echo "    Running test case $TEST_CASE_NUMBER"

            # Symlinking the testcase: student's solution expects a hardcoded file name.
            ln -f -s $TEST_CASE $PROBLEM_CODE.in

            # Run student's solution.
            bash run.sh 1>./output/stdout/$TEST_CASE_NUMBER-stdout.log 2>./output/stderr/$TEST_CASE_NUMBER-stderr.log

            # Saving the output for the test case.
            mv -f $PROBLEM_CODE.out ./output/$TEST_CASE_NUMBER.out
        done

        # Removing the symlink.
        rm $PROBLEM_CODE.in
    fi
done

cd $ROOT_DIR
