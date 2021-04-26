FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    # python:
    python3-pip python3-dev \
    # base system:
    build-essential \
    ccache \
    curl \
    dbus \
    gir1.2-gtk-3.0 \
    git \
    gobject-introspection \
    lcov \
    libbz2-dev \
    libcairo2-dev \
    libffi-dev \
    libglib2.0-dev \
    libgtk-3-0 \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    xauth \
    xvfb \
    # our specific deps:
    pkg-config \
    libgirepository1.0-dev \
    meson \
    ninja-build \
    appstream-util \
    libusb-1.0-0-dev \
    libudev-dev \
    gir1.2-appindicator3-0.1 \
    gnome-shell-extension-appindicator \
    # cleanup:
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip \
    && apt-get -y autoclean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*

# Use C.UTF-8 locale to avoid issues with ASCII encoding
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV CI true
