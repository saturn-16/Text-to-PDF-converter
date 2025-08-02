# Text to PDF Converter

A simple, user-friendly web application for converting rich text content into a downloadable PDF file. This project is built with Flask and features user authentication, dark mode, and a modern, glassmorphism-inspired design.

The structure of folder should look like this :-
your-project-name/
├── .gitignore
├── app.py

├── LICENSE.md

├── requirements.txt

├── README.md
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── scripts.js
│   └── google_icon.svg
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── register.html
└── site.db (this file is generated when you run the app)

## Features

-   **Rich Text Editor:** Use a modern, feature-rich editor to write and format your text with bold, italics, lists, and more.
-   **PDF Conversion:** Instantly convert your formatted text into a PDF document.
-   **User Authentication:** Securely log in with a username and password or use the "Sign in with Google" option via OAuth.
-   **Dark Mode:** A stylish dark theme toggle for comfortable viewing.
-   **Clean and Professional UI:** A minimalist, glassmorphism design that provides an elegant user experience.

## Technologies Used

-   **Backend:** Python, Flask
-   **Database:** SQLite (for development)
-   **Authentication:** Flask-Login, Flask-Bcrypt, Authlib (for Google OAuth)
-   **PDF Conversion:** xhtml2pdf
-   **Frontend:** HTML5, CSS3, JavaScript
-   **Rich Text Editor:** Quill.js

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Python 3.7 or higher
-   pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   **On Windows:**
        ```bash
        venv\Scripts\activate
        ```
    -   **On macOS and Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up Google OAuth Credentials:**
    * Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
    * Go to **APIs & Services > Credentials** and create a new **OAuth client ID** for a "Web application."
    * Add `http://127.0.0.1:5000/auth/google/callback` as an **Authorized redirect URI**.
    * Copy your **Client ID** and **Client Secret**.

6.  **Configure the application:**
    * Open `app.py`.
    * Replace the placeholder values with your own secret key and Google credentials:
    ```python
    app.config['SECRET_KEY'] = 'your_strong_secret_key'
    
    oauth.register(
        name='google',
        client_id='YOUR_GOOGLE_CLIENT_ID',
        client_secret='YOUR_GOOGLE_CLIENT_SECRET',
        # ... rest of the configuration
    )
    ```

### Running the Application

1.  **Start the Flask server:**
    ```bash
    flask run
    ```
    If you see a `site.db` file already in the directory, and you are getting a `no such column` error, you must delete the `site.db` file and restart the server to create a new database with the correct schema.

2.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000`.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.
