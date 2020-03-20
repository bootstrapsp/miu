FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8

# Install Python 3 & pip
RUN apt-get update -qq && \
    apt-get install -y software-properties-common python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install libindy
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CE7709D068DB5E88 && \
    add-apt-repository "deb https://repo.sovrin.org/sdk/deb bionic stable" && \
    apt-get update -qq && \
    apt-get install -y libindy && \
    rm -rf /var/lib/apt/lists/*

# Optianally set uid & gid at build time
ARG USER_ID
ARG GROUP_ID

# Create unprivileged user & group "app"
RUN groupadd -g ${GROUP_ID:-1000} app && \
    useradd -l -u ${USER_ID:-1000} -g app app && \
    install -d -m 0755 -o app -g app /home/app

USER app

# Install required python libraries
COPY --chown=app:app ./pyserverforindy/requirements.txt /app/pyserverforindy/requirements.txt
RUN pip3 install --no-cache-dir -r /app/pyserverforindy/requirements.txt

# Add project files to image
COPY --chown=app:app . /app

VOLUME /home/app/.indy_client

CMD ["python3", "/app/pyserverforindy/grpc_server/server.py"]

EXPOSE 50051
