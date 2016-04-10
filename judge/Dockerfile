FROM phusion/baseimage:0.9.18
MAINTAINER Yuriy Guts <yuriy.guts@gmail.com>

ENV DEBIAN_FRONTEND=noninteractive \
    TERM=xterm \
    EDITOR=nano \
    JUDGE_ROOT=/opt/lits-algorithms-judge

WORKDIR $JUDGE_ROOT
ADD . /tmp
RUN cd /tmp && /bin/bash Dockerfile.build.sh

CMD ["/sbin/my_init"]
