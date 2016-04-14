#!/usr/bin/env bash

BUILD_DIR=`pwd`


# ----- Install system software -----

apt-get update
apt-get -y install curl wget rsync zip git nano mc htop
apt-get -y install software-properties-common
echo "Europe/Kiev" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata


# ----- Set up repositories ------

# Java
echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | debconf-set-selections
add-apt-repository --yes ppa:webupd8team/java

# Mono
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
echo "deb http://download.mono-project.com/repo/debian wheezy main" | tee /etc/apt/sources.list.d/mono-xamarin.list

# Node.js
curl -L https://raw.githubusercontent.com/nodesource/distributions/master/deb/setup_5.x | bash -

# Ruby
gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3


# ----- Install language tools -----

# Python
apt-get -y install python python-dev python-pip

# Java
apt-get -y install oracle-java8-installer && echo 'JAVA_HOME=/usr/lib/jvm/java-8-oracle' | tee -a /etc/environment

# Mono
apt-get -y install mono-complete

# Node.js
apt-get -y install nodejs

# Ruby
curl -sSL https://get.rvm.io | bash -s stable --ruby=2.3.0

# Scala
# Commented out right now - eats up too much container space and is not used by Hammurabi.
# wget -O scala-2.11.8.deb http://downloads.lightbend.com/scala/2.11.8/scala-2.11.8.deb && dpkg -i scala-2.11.8.deb && rm scala-2.11.8.deb


# ----- Copy contents to proper folders -----

cd "$BUILD_DIR"
mv -f hammurabi "$JUDGE_ROOT/"
mv -f student-repos "$JUDGE_ROOT/"
mkdir "$JUDGE_ROOT/problems"
mkdir "$JUDGE_ROOT/reports"

cd build-support
mv -f dotfiles/.??* ~/
mv -f problem-templates "$JUDGE_ROOT/"
mv -f custom-verifiers/*.py "$JUDGE_ROOT/hammurabi/hammurabi/grader/verifiers/"
mv -f grader.conf "$JUDGE_ROOT/hammurabi/hammurabi/conf/"
mv -f grader-job.conf "$JUDGE_ROOT/student-repos/"


# ----- Set up Hammurabi -----

# Promote submodule to independent Git repo.
cd "$JUDGE_ROOT/hammurabi"
rm -rf .git
git init
git remote add origin https://github.com/YuriyGuts/hammurabi
git fetch --all
git reset --hard origin/master
git branch --set-upstream-to=origin/master

# Set up dependencies.
cd "$JUDGE_ROOT/hammurabi" && pip install -r pip-requirements.txt
pip install awscli


# ----- Set up crontab -----

mkdir -p "$JUDGE_ROOT/logs"
cd "$BUILD_DIR/build-support"
crontab grader-job.crontab


# ----- Clean up -----

rm -rf /var/cache/oracle-jdk8-installer /var/lib/apt/lists/* /tmp/* /var/tmp/*
