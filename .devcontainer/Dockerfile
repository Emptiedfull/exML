# Use the official Conda base image
FROM continuumio/miniconda3

# Set the working directory
WORKDIR /workspaces/<your-repo-name>

# Copy the environment file into the container
COPY requirements.yml .devcontainer/requirements.yml

# Install Conda environment
RUN conda env create -f .devcontainer/requirements.yml

# Activate the environment
RUN echo "conda activate myenv" >> ~/.bashrc