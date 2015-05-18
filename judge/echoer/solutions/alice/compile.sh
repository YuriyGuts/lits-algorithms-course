#!/usr/bin/env bash

# Set basic variables
JAVA_COMPILER=javac

# Compile
find . -name "*.java" -print | xargs $JAVA_COMPILER -O
