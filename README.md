Project Structure:
```
crypto_airdrop_manager/
│
├── app.py                 # Main Flask application files
│
├── templates/             # Folder for HTML templates
│ └── index.html           # Home page template
│
├── airdrop_manager.db     # SQLite database (auto-generated)
│
└── README.md              # Documentation
```

# README.md

# Crypto Airdrop Manager

A Flask-based web application to manage cryptocurrency testnet airdrop links in one place.

## Features

- Add testnet airdrop links with name and description
- View all links in a user-friendly interface
- Open links individually in a new browser tab
- Open all links at once with one click
- Remove unnecessary links

## Requirements

- Python 3.6+
- Flask

## Installation

1. Clone the repository or download the source code

2. Create and activate a virtual environment (optional but recommended)
```
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies
```
pip install flask
```

4. Run the application
```
python app.py
```

5. Open a browser and access the application at the address:
```
http://127.0.0.1:5000/
```

## Usage

1. **Adding a New Project**
- Click the "Add New Project" button
- Fill in the project name, URL, and optional description
- Click "Save"

2. **Opening a Link**
- Click the "Open Link" button on the project card to open the URL in a new tab
- Click the "Open All" button in the header to open all URLs at once

3. **Deleting a Project**
- Click the "Delete" button on the project card you want to delete
- Confirm the deletion in the modal that appears

## Database

This application uses SQLite as its database. The database file `airdrop_manager.db` will be created automatically the first time the application is run.

## Further Development

Some ideas for further development:
- Project categorization feature
- Adding status for each project (Unclaimed, Claimed, Pending, etc.)
- Authentication system for multi-users
- Database backup and restore
- Integration with crypto wallets
