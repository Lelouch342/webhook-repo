# GitHub Webhook Listener Assignment

This project implements a GitHub webhook listener using Flask. It receives repository events, stores them in MongoDB, and displays live updates on a dashboard UI that refreshes every 15 seconds.

## Features

-   Receives GitHub webhook events
-   Handles Push, Pull Request, and Merge events
-   Stores event data in MongoDB Atlas
-   Prevents duplicate event entries
-   Displays live activity feed on UI
-   Auto refresh every 15 seconds

## Tech Stack

-   Python (Flask)
-   MongoDB Atlas
-   HTML, JavaScript
-   GitHub Webhooks
-   ngrok (for local webhook testing)

## Repositories Used

### webhook-repo 

This repository contains the main application code:
-   Flask webhook receiver
-   MongoDB integration
-   Events API
-   Dashboard UI

GitHub Link: `https://github.com/Lelouch342/webhook-repo`

### action-repo

This repository is used to generate GitHub events for testing the webhook integration.
It is used to:

-   Trigger push events
-   Create pull requests
-   Perform merge operations

These events are captured by the webhook server.
GitHub Link: `https://github.com/Lelouch342/action-repo`

## Project Structure


webhook-repo/ ├── app.py
├── templates/
│ └── index.html
├── static/
│ └── app.js
├── requirements.txt
├── .gitignore
└── README.md

## Setup Instructions

### Clone Repository

git clone https://github.com/YOUR_USERNAME/webhook-repo.git\
cd webhook-repo

### Create Virtual Environment

python -m venv venv

Activate: venv\Scripts\activate

### Install Dependencies

pip install -r requirements.txt

### Configure Environment Variables

Create a .env file:

MONGO_URI=your_mongodb_connection_string

### Run Application

python app.py

Server URL: http://localhost:5000

Dashboard URL: http://localhost:5000/dashboard

## Webhook Setup

Run ngrok:  ngrok http 5000

Add webhook in GitHub action-repo:

Payload URL: https://<ngrok-url>{=html}/webhook

Content type: application/json

Select: Send me everything

## Testing

Trigger events by:

-   Pushing commits
-   Creating pull requests
-   Merging pull requests

Events will appear automatically on the dashboard.

## Submission Repositories

-   webhook-repo
-   action-repo

## Notes

-   MongoDB credentials are not included in repository
-   .env file is ignored using .gitignore
-   ngrok is used only for local testing


