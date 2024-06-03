```markdown
# RFP Tool Q&A

This repository contains a Streamlit application for an RFP Tool Q&A. The application uses Amazon Bedrock Agent Runtime to process user questions and provide responses along with summarized references and citations.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Docker Setup](#docker-setup)
- [Usage](#usage)
- [GitHub Setup](#github-setup)
- [License](#license)

## Overview

The RFP Tool Q&A application allows users to interact with an Amazon Bedrock Agent by entering questions and receiving detailed responses. The application provides a user-friendly interface to input session details and questions, and displays the agent's responses, summarized references, and citations.

## Features

- User input for Agent ID, Agent Alias ID, Session ID, and questions.
- Display of agent responses.
- Display of summarized references.
- Display of clickable citation links.

## Setup

### Prerequisites

- Python 3.7 or higher
- Docker (for Docker setup)

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/rfp-tool-qa.git
   cd rfp-tool-qa
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

### Running the Application

1. **Run the Streamlit application:**

   ```sh
   streamlit run app.py
   ```

2. **Access the application in your browser:**
   Open your web browser and go to `http://localhost:8501`.

## Docker Setup

### Prerequisites

- Docker

### Building the Docker Image

1. **Build the Docker image:**

   ```sh
   docker build -t rfp-tool-qa .
   ```

### Running the Docker Container

1. **Run the Docker container:**

   ```sh
   docker run -p 8501:8501 rfp-tool-qa
   ```

2. **Access the application in your browser:**
   Open your web browser and go to `http://localhost:8501`.

## Usage

1. **Set the session details:**
   - The `Agent ID` and `Agent Alias ID` should be updated in app.py file.
   - Enter a `Session ID` and your question. Example: `123` 

2. **Submit the question:**
   - Click the "Go" button to send the question to the agent.
   - View the response, summarized references, and clickable citations.

## GitHub Setup

### Initialize and Push to GitHub

1. **Initialize a Git repository (if not already done)**:
   ```sh
   git init
   ```

2. **Add all your project files to the repository**:
   ```sh
   git add .
   ```

3. **Commit your changes**:
   ```sh
   git commit -m "Initial commit with README and project files"
   ```

4. **Create a new repository on GitHub**:
   - Go to GitHub and create a new repository.

5. **Add the remote repository URL**:
   ```sh
   git remote add origin https://github.com/yourusername/rfp-tool-qa.git
   ```

6. **Push your changes to GitHub**:
   ```sh
   git push -u origin master
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---