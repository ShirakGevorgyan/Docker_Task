# Assignments for Associate Data Engineer role at Krisp

### Instructions for building and running

\# Make sure you're on on a Linux system, whether natively or virtually. Certain distributions and versions may require additional dependencies to be installed manually.

On Debian-based derivatives:
$ sudo apt update
$ sudo apt install docker-compose

On Red Hat Enterprise Linux (RHEL) derivatives:
$ sudo yum update
$ sudo yum install docker-compose

*On newer versions YUM is an alias to DNF, a next-generation package manage, again based on RPM.

On Arch-based derivatives:
$ sudo pacman -Syu
$ sudo pacman -S docker-compose

On OpenSUSE-based derivatives:
sudo zypper refresh
sudo zypper install docker-compose

On Alpine-based derivatives:
$ sudo apk update
$ sudo apk add doctor-compose

sudo docker-compose up --build
to only run post-build, just omit the `--build` option.


Tested on Ubuntu 22.04.4 LTS (Jammy Jellyfish).


# Audio Recording and Sentiment Analysis Application

## Overview
This project is a Flask-based web application designed to record audio, analyze its sentiment, store the results in a MySQL database, and save the data in a CSV file. The application is fully containerized using Docker, allowing for easy setup and deployment. 

## Project Structure
The project is organized into several directories and files, each serving a specific purpose:

### 1. **app/**
This directory contains the main Flask application and its dependencies.

- **templates/**
  - `index.html`: This is the main HTML template used by the Flask application. It defines the user interface where you can start, stop, and shut down the recording. The template uses HTML and integrates with the Flask backend to dynamically update based on user actions.

- **app.py**: 
  - This is the core of the application. It defines the Flask routes (`/`, `/start`, `/stop`, `/shutdown`) and handles the main logic for recording audio, processing it, and interacting with the database.
  - **record_and_analyze_audio()**: A function that records 5 seconds of audio, processes it, and returns a dummy transcript and sentiment analysis result.
  - **create_table()**: This function ensures that the `user_metrics` table exists in the MySQL database. If it does not exist, the function creates it.
  - **insert_data()**: This function inserts a new record into the `user_metrics` table with the data obtained from the audio recording.
  - **Flask Routes**:
    - `/`: Renders the `index.html` template.
    - `/start`: Starts a new audio recording session, processes the data, saves it to the database and CSV file, and redirects back to the homepage.
    - `/stop`: Currently a placeholder for stopping the recording (if implemented).
    - `/shutdown`: Saves any unsaved data, stops the Flask server, shuts down the Docker containers, and clears the terminal.

- **Dockerfile**: 
  - Defines the Docker image for the Flask application. 
  - **Base Image**: Uses `python:3.8`.
  - **WORKDIR**: Sets `/app` as the working directory.
  - **RUN Commands**: Installs necessary system packages (`portaudio19-dev`, `alsa-utils`), installs Python dependencies listed in `requirements.txt`, and sets up directories for Flask templates and static files.
  - **ENV**: Configures environment variables for audio device settings.
  - **CMD**: Runs the Flask application when the container starts.

- **requirements.txt**: 
  - Lists the Python packages required by the Flask application, such as Flask, TextBlob, MySQL Connector, SoundDevice, etc. This file ensures all necessary dependencies are installed when the Docker image is built.

- **wait-for-it.sh**: 
  - A shell script that waits for the MySQL database to be ready before starting the Flask application. This script helps avoid race conditions during container startup.

### 2. **data/**
This directory is where the CSV files containing the recorded data are stored.

- **user_metrics.csv**: 
  - This file contains the data collected from the audio recordings, such as transcripts, sentiment scores, timestamps, etc. Each new recording session appends a new row to this file.

### 3. **db/**
This directory contains the Docker configuration for the MySQL database.

- **Dockerfile**:
  - Defines the Docker image for the MySQL database.
  - **Base Image**: Uses `mysql:8.0`.
  - Configures environment variables for the MySQL root password, database name, and user credentials.

- **docker-compose.yml**: 
  - The `docker-compose` configuration file that orchestrates the Flask and MySQL services.
  - **version**: Specifies the Docker Compose file format version.
  - **services**:
    - **app**: Defines the Flask application service.
      - **build**: Points to the `app` directory where the Flask Dockerfile is located.
      - **volumes**: Mounts directories for data persistence and PulseAudio integration.
      - **environment**: Sets environment variables for the Flask application.
      - **depends_on**: Ensures the MySQL service (`db`) is started before the Flask application.
      - **command**: Specifies the command to run when the container starts (`flask run`).
      - **privileged**: Allows the container to access audio devices.
    - **db**: Defines the MySQL database service.
      - **image**: Specifies the MySQL version to use.
      - **environment**: Sets environment variables for the MySQL root password, database name, and user credentials.
      - **ports**: Maps the MySQL port from the container to the host.
      - **volumes**: Mounts a volume for persistent MySQL data storage.

### 4. **index.html**
Located in the `app/templates/` directory, this file is the HTML template for the Flask web interface. It includes buttons for starting, stopping, and shutting down the recording process.

## Setting Up and Running the Containers

### Prerequisites
Before you start, ensure you have the following installed on your system:
- **Docker**: Used to containerize the application and manage dependencies.
- **Docker Compose**: Helps orchestrate multiple Docker containers.

### Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
