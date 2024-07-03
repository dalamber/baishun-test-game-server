FROM python:3.11-slim

# Enable Python's fault handler for easier debugging of crashes
ENV PYTHONFAULTHANDLER=1
# Force the stdout and stderr streams to be unbuffered; this is useful in container logs
ENV PYTHONUNBUFFERED=1
# Set Python's hash seed to 'random' to provide a measure of security against certain hash-based attacks
ENV PYTHONHASHSEED=random
# Prevent Python from writing .pyc files to disk (useful in production to avoid writing bytecode to a possibly read-only filesystem)
ENV PYTHONDONTWRITEBYTECODE 1
# Disable the pip cache to save space in the final image
ENV PIP_NO_CACHE_DIR=off 
# Disable pip's periodic check for a new version to speed up builds
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
# Set a default timeout value (in seconds) for pip operations to avoid hanging builds
ENV PIP_DEFAULT_TIMEOUT=100

# Update the list of available packages and their versions, but it does not install or upgrade any packages.
RUN apt-get update
# Install Python 3, pip (Python package installer), build-essential (compilation tools), and python3-venv (virtual environment) packages.
RUN apt-get install -y python3 python3-pip build-essential python3-venv
# Create a directory named /codebase in the container's filesystem to hold the application code.
RUN mkdir -p /codebase
# Copy everything from the Docker context (i.e., the directory containing the Dockerfile) into the /codebase directory inside the container.
ADD . /codebase
# Set the working directory for any subsequent RUN, CMD, ENTRYPOINT, COPY, and ADD instructions in the Dockerfile to /codebase.
WORKDIR /codebase
# Install the Python dependencies specified in the requirements.txt file using pip.
RUN pip3 install -r requirements.txt
# Change the permissions of the main.py file within /codebase/src to make it executable.
RUN chmod +x /codebase/src/main.py
