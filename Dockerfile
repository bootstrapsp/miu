FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -qq && \
    apt-get install -y software-properties-common python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CE7709D068DB5E88 && \
    add-apt-repository "deb https://repo.sovrin.org/sdk/deb bionic stable" && \
    apt-get update -qq && \
    apt-get install -y libindy && \
    rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/pip3 /usr/bin/pip

ADD ./pyserverforindy/requirements.txt /app/pyserverforindy/requirements.txt
RUN pip install --no-cache-dir -r /app/pyserverforindy/requirements.txt

ADD . /app

CMD python3 /app/pyserverforindy/grpc_server/server.py

EXPOSE 50051
