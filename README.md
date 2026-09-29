Stock Helper

A simple, mobile-friendly web app for tracking shelf status while restocking a retail store. It helps spot two common problems: shelves that are running low with no product sent out, and full shelves that still have leftover boxes.

Built with Python, Flask, and SQLite.

Features
Add items with a name, aisle, shelf status, leftover box count, and an optional note
Update an item's status (Full, Low, Empty) and leftover boxes with one tap
Needs restock view: shows shelves marked Low or Empty
Extra boxes view: shows Full shelves that still have leftover boxes
Works in a phone browser, so nothing needs to be installed on the phone
Data is stored locally in a SQLite database that is created automatically
Tech stack
Python 3
Flask
SQLite
HTML and CSS (no external frameworks)
Getting started
1. Clone the repository
git clone https://github.com/YOUR-USERNAME/Stock_Helper.git
cd Stock_Helper
2. Create a virtual environment

On macOS or Linux:

python3 -m venv .venv
source .venv/bin/activate

On Windows:

python -m venv .venv
.venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Run the app
python app.py

Then open http://localhost:5001 in your browser.

Note: the app runs on port 5001 because port 5000 is used by AirPlay Receiver on newer Macs. You can change the port on the last line of app.py.

Using it on your phone
Connect your phone and computer to the same network (or connect the computer to your phone's hotspot).
Find your computer's local IP address. On macOS, run ipconfig getifaddr en0.
On your phone, open http://YOUR-IP-ADDRESS:5001.

Some Wi-Fi networks block devices from reaching each other. If the page will not load, try using your phone's hotspot.

Project structure
Stock_Helper/
    app.py               Flask app, routes, and database setup
    requirements.txt     Python dependencies
    templates/
        index.html       Main page and styling
Roadmap
Search box to find items quickly
Last updated time on each item
Barcode scanning with the phone camera
Simple reports on which items run low most often
Note

This is a personal learning project. It uses only sample data that you enter yourself and is not connected to any store system.
