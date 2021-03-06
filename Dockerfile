FROM python:3.7-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install pipenv and compilation dependencies
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv && apt-get update && apt-get install -y --no-install-recommends gcc git pastebinit
# Install python dependencies in /.venv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv sync --dev
ENV PATH="/.venv/bin:$PATH"
# Create and switch to a new user
RUN useradd -m developer
WORKDIR /home/developer
# Install application into container
# COPY . .
# RUN chown -R developer:developer /home/developer
ENV PIPENV_COLORBLIND 1
USER developer 
ENTRYPOINT "/bin/bash"

# How to use this thing

# Install docker and make sure it's running (of course)
# On Windows, I recommend using PowerShell.

# Build the docker image
# docker build . -t city-scrapers-pitt

# If and when it successfully builds, you need to tell it
# where your city-scrapers-pitt repo is located locally.
# The part after the ":" should not change. That's where your
# repo will be inside the container itself.

# On windows you can do '/c/' to indicate the C drive.
# Example:
# docker run -it -v /c/Users/yourname/city-scrapers-pitt:/home/developer/city-scrapers-pitt city-scrapers-pitt:latest

# Now, you will be inside the docker container, and you can run commands inside of it.
# Example:
# cd city-scrapers-pitt; pytest

# Changes to the repo should still be handled and managed outside of the container.
# Changes inside the container, not in the mounted volume, will be lost when the docker process is stopped.

# You don't have to stop the docker container. You can just quit the docker container when you are done.
