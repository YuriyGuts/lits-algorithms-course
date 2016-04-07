FROM phusion/baseimage:0.9.18
MAINTAINER Yuriy Guts <yuriy.guts@gmail.com>

ENV DEBIAN_FRONTEND=noninteractive \
    TERM=xterm \
    EDITOR=nano \
    JUDGE_ROOT=/opt/lits-algorithms-judge

ADD . $JUDGE_ROOT
RUN /bin/bash "$JUDGE_ROOT/Dockerfile.build.sh"

CMD ["/sbin/my_init"]
