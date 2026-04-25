# TMail – Terminal Gmail Client 📧

TMail is a **Terminal User Interface (TUI) Gmail client** built with **Python** using the **Textual framework**. It allows users to **read and send Gmail emails directly from the terminal** through a keyboard-driven interface.

The application integrates with the **Gmail API** using OAuth authentication and provides a simple yet powerful way to manage emails without leaving the terminal.

---

# Features

* 📥 **Read Emails**

  * View inbox messages
  * See preview of each mail side by side.
  * Browse emails using keyboard navigation
  * Open and read full email content


* 📜 **Email Viewer**

  * Complete emails displayed in separate screen.
  * Option to download attachments using `d` key.
  * Option to open the email in the browser.

* ✉️ **Send Emails**

  * Compose and send emails directly from the terminal.
  * send the mail just by pressing the `s` key.

* 🧭 **Keyboard Navigation**

  * Arrow keys to move through options
  * Enter to select
  * `p` to go back
  * `q` to quit
  * `up` and `down` keys to navigate menu
  * `v` to open the prview of mail
  * `d` to download the attachment.
  * `s` to send the mail.

* 🎨 **Terminal UI**

  * Built with **Textual** and **Rich** for a modern terminal experience

---

# Technologies Used

* **Python**
* **Textual** – Terminal UI framework
* **Rich** – Terminal rendering
* **Gmail API**
* **Google OAuth2**

---

# Project Structure

```
tmail/
│
├── screenshots/
│   ├── main_menu.png
│   ├── inbox_view.png
│   ├── email_viewer.png
│   └── compose_email.png
│
├── app.py
│
├── screens/
│   ├── read_mail.py
│   ├── view_mail.py
│   ├── send_mail.py
│   └── mock_emails.py
│
├── services/
│   ├── authenticate.py
│   ├── read_mail.py
│   └── send_mail.py
│
└── README.md
```

### Description

| File / Folder     | Purpose                                           |
| ----------------- | ------------------------------------------------- |
| `app.py`          | Main entry point of the application               |
| `screens/`        | UI screens for different parts of the application |
| `services/`       | Logic for interacting with the Gmail API          |
| `authenticate.py` | Handles OAuth authentication                      |
| `read_mail.py`    | Fetches emails from Gmail                         |
| `send_mail.py`    | Sends emails using Gmail API                      |

---

# Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/tmail.git
cd tmail
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install textual rich google-api-python-client google-auth google-auth-oauthlib
```

---

# Google Cloud Setup (Gmail API)

To allow the application to access your Gmail account, you must create a **Google Cloud project** and enable the **Gmail API**.

### Step 1 – Create a Google Cloud Project

1. Go to the **Google Cloud Console**
2. Click **Select Project → New Project**
3. Give your project a name
4. Create the project

---

### Step 2 – Enable Gmail API

1. Navigate to **APIs & Services → Library**
2. Search for **Gmail API**
3. Click **Enable**

---

### Step 3 – Create OAuth Client ID

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials**
3. Select **OAuth Client ID**
4. Choose **Desktop Application**
5. Create the client

---

### Step 4 – Download OAuth Credentials

Download the OAuth credentials file and place it in the project directory.

---

### Step 5 – Run the Application

When the application runs for the first time, a **browser window will open** asking you to log in to your Google account and authorize the application.

---

# Running the Application

Start the application with:

```bash
python app.py
```

You will see a menu similar to:

```
Read Mail
Send Mail
Exit
```

Navigate using the arrow keys and press **Enter** to select an option.

---

# Keyboard Shortcuts

| Key   | Action           |
| ----- | ---------------- |
| ↑ / ↓ | Navigate menu    |
| Enter | Select option    |
| p     | Go back          |
| q     | Quit application |

---

# Future Improvements

* Implement lazy loading
* Email search functionality
* Reply and forward support
* Pagination for large inboxes
* Multiple email account support

---

# License

This project is intended for **educational and learning purposes**.
