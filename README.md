# Black Bankers Scraper

A Python script to download course content including videos and PDF attachments from [Black Bankers](https://blackbankers.com.br/) learning platform.

## Prerequisites

- Python 3.x
- Required packages (listed in `requirements.txt`)

## Setup

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get your authorization token:
   - Open your browser and log into the [platform](https://blackbankers.app.cativa.digital/feed) feed
   - Press F12 to open Developer Tools
   - Go to the Network tab
   - Find a request containing "private" in its name
   - Click on the request
   - In the Headers section, scroll down to "Request Headers"
   - Find the "authorization" header
   - Copy the token part (after "Bearer ")

4. Create a `.env` file in the project root and paste your token:
```
AUTHORIZATION=your_token_here
```

## Usage

Simply run the script:
```bash
python spider.py
```

The script will:
- Create a directory structure based on course organization
- Download course videos in lowest quality to save space
- Save any PDF attachments
- Maintain the original course structure with modules and lessons


## Features

- Automatic directory creation and organization
- Video downloads using yt-dlp
- PDF attachment downloads
- Maintains course structure hierarchy
- Error handling for failed downloads


## Disclaimer

This tool is for personal use only. Make sure you have the right to access and download the content. Respect the platform's terms of service and content usage rights.