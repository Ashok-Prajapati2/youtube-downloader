# YouTube Video Downloader

![YouTube Logo](https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg)

A simple Flask-based YouTube video downloader that lets you download videos and audio in various formats using `yt-dlp`.

## Features

- Choose separate formats for video and audio.
- Download video only, audio only, or both.
- Get real-time progress updates.
- Easy deployment on cloud services like Koyeb.

## Screenshots

### Home Page
![Home Page](static/img/home.png)

## How to Use

### Prerequisites

- Python 3.9+
- `yt-dlp`
- `Flask`
- `Flask-SocketIO` (for real-time updates)

### Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Ashok-Prajapati2/youtube-downloader
    cd youtube-downloader
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Install Dependencies**

    Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. **Start the Flask Application**

    Use the `run.py` file to start the Flask development server:

    ```bash
    python3 run.py
    ```

2. **Access the Application**

    Open your web browser and go to `http://127.0.0.1:5000/`.

3. **Download a Video**

    - Enter the YouTube URL.
    - Select the desired video and audio formats.
    - Click the "Download" button.
    - Wait for the download to finish; the file will be saved in the specified output directory.

## Deployment

### Deployment on Koyeb

1. **Push Code to Koyeb**

    Follow Koyeb's documentation to deploy your code.

    Access your app at: [sore-desiree-student098-ee31c4ca.koyeb.app/](sore-desiree-student098-ee31c4ca.koyeb.app/)

2. **Set Up Environment Variables**

    - `FLASK_APP`: Set to `run.py`.
    - `YT_DLP_OPTIONS`: Set any options you need for `yt-dlp`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
