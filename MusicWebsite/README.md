# Underground Rap Studio Pro

A personal music library web application designed to collect, manage, and listen to my own rap tracks, beats, and lyrics in one secure place.

## The Story Behind The Project

I started this project with a strong vision for a music vault but with limited coding knowledge. Instead of letting that stop me, I took on the role of a project manager and system designer. 

This application was built through intensive pair programming with my AI assistant (Onur'S-AI). While the AI handled the heavy lifting of writing the core Python architecture, I directed the logic, managed the debugging process, and orchestrated the feature implementations. 

Through building this app, I learned fundamental software engineering concepts practically, including:
* How relational databases (SQLite) store and isolate user data.
* The importance of password hashing (SHA-256) for security.
* How to manage user sessions and state in a stateless web framework.
* Front-end customization using CSS and DOM manipulation.
* Overcoming platform-specific bugs (like iOS audio streaming limitations).

This project is not just a music player; it is a testament to my learning journey in software development.

## Key Features

* Multi-tenant Architecture: Secure user registration and login system with strict data isolation.
* Media Management: Upload audio files (MP3/WAV) alongside custom album cover art.
* Dynamic Lyrics Engine: Integrated lyrics display with pre-wrap formatting and a read-more/collapse mechanism.
* Local Database: Powered by SQLite to handle user credentials and track metadata securely.
* Premium UI/UX: A highly customized, responsive dark-themed interface built on Streamlit with advanced CSS styling.
* Session Persistence: URL query parameter integration to prevent unexpected logouts upon page refresh.

## How to Run Locally

1. Clone this repository to your local machine.
2. Ensure you have Python installed.
3. Install the required library by running:
   pip install streamlit
4. Start the application by running:
   python -m streamlit run app.py
