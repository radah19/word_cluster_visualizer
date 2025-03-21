#!/bin/bash

# Set up Virtual Environment
python -m pip install virtualenv
python -m venv venv

# Activate Virtual Environment
source ./venv/bin/activate

# Install dependencies for server
python -m pip install -r requirements.txt

# Create Necessary Directories
mkdir cluster_visualizations