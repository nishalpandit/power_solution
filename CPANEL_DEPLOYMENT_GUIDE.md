# Complete Guide: Deploying Power Solution FastAPI on cPanel

This guide provides step-by-step instructions to deploy the **Power Solution Backend API** onto any standard **cPanel hosting** account (CloudLinux Phusion Passenger / "Setup Python App").

---

## What Has Been Prepared for cPanel

1. **`passenger_wsgi.py`**: The official entry point required by cPanel Phusion Passenger. It automatically bridges the FastAPI ASGI application to Passenger's WSGI interface using `a2wsgi`.
2. **`requirements.txt`**: Includes all required dependencies, including `a2wsgi>=1.10.0`.
3. **Absolute Upload Paths**: `main.py` dynamically anchors `uploads/` to `BASE_DIR`, preventing path resolution errors on Linux web servers.
4. **Database Readiness**: Uses SQLite (`db.sqlite3`) out-of-the-box with auto-table migrations, or can optionally connect to cPanel MySQL.

---

## Step 1: Create the Python Application in cPanel

1. Log into your **cPanel** dashboard.
2. Scroll to the **Software** section and click on **Setup Python App**.
3. Click the **Create Application** button in the top right.
4. Fill in the application settings:
   - **Python Version**: Choose **`3.10`**, **`3.11`**, or **`3.12`** (Recommended: `3.11`).
   - **Application root**: Enter the folder path where project files will live, for example: `power_solution` (or `api.yourdomain.com`).
   - **Application URL**: Select your domain/subdomain and path:
     - For a dedicated subdomain: select `api.yourdomain.com` (leave subfolder blank).
     - For a subfolder: select `yourdomain.com` and type `api` in the box.
   - **Application startup file**: Enter `passenger_wsgi.py`.
   - **Application Entry point**: Enter `application`.
   - **Passenger log file**: (Optional) `passenger.log`.
5. Click **CREATE** (in the top right corner).
6. cPanel will generate a virtual environment and display a command at the top of the page, e.g.:
   ```bash
   source /home/yourusername/virtualenv/power_solution/3.11/bin/activate && cd /home/yourusername/power_solution
   ```

---

## Step 2: Upload Project Files to cPanel

### Option A: Via cPanel File Manager (Easiest)
1. On your local machine, zip the project files:
   - **Include**: `main.py`, `passenger_wsgi.py`, `requirements.txt`, `api/`, `core/`, `uploads/`, and optionally `db.sqlite3` (to keep your existing seeded products/data).
   - **Exclude**: `env/`, `__pycache__/`, `.git/`, and `scratch/`.
2. In cPanel, open **File Manager**.
3. Navigate to the **Application root** folder you specified in Step 1 (e.g. `/home/yourusername/power_solution`).
4. Click **Upload** and upload your `.zip` file.
5. Right-click the uploaded `.zip` file and click **Extract**.

### Option B: Via Git Version Control in cPanel
1. In cPanel, click **Git Version Control**.
2. Clone your repository directly into the application root directory.

---

## Step 3: Install Dependencies

### Method 1: Using the cPanel Web UI
1. Go back to **Setup Python App** and click the **Edit (pencil)** icon on your application.
2. Scroll down to the **Configuration files** section.
3. In the input box, type `requirements.txt` and click **Add**.
4. Click the **Run Pip Install** button that appears next to `requirements.txt`.
5. Wait for cPanel to finish installing packages. A success notification will appear.

### Method 2: Using cPanel Terminal (Fastest)
1. Open **Terminal** from your cPanel dashboard.
2. Paste the virtual environment command copied in Step 1:
   ```bash
   source /home/yourusername/virtualenv/power_solution/3.11/bin/activate && cd /home/yourusername/power_solution
   ```
3. Run pip install:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## Step 4: Verify File & Directory Permissions

Ensure the web server has permission to read and write to the database and upload folders:
1. In cPanel **File Manager**:
   - `uploads/` folder: Permission **`755`**
   - `uploads/products/`: Permission **`755`**
   - `uploads/categories/`: Permission **`755`**
   - `uploads/payments/`: Permission **`755`**
   - `db.sqlite3`: Permission **`664`** (Read & Write for User and Group)
2. If using cPanel Terminal:
   ```bash
   chmod 755 uploads uploads/*
   chmod 664 db.sqlite3
   ```

---

## Step 5: Restart the Application

1. In cPanel, go to **Setup Python App**.
2. In the list of applications, click the **Restart** icon (circular green arrow) next to your app.

---

## Step 6: Test Your Live API

1. Open your browser and navigate to your configured URL:
   - **Root Health Check**:
     ```
     https://api.yourdomain.com/
     ```
     *Expected response:*
     ```json
     {"message": "Power Solution API is running"}
     ```

2. **Interactive Swagger Documentation**:
   ```
   https://api.yourdomain.com/docs
   ```
   *You will see the complete, live Swagger UI with all 31 endpoints ready to test directly in browser.*

3. **Check an Endpoint**:
   ```
   https://api.yourdomain.com/api/products
   https://api.yourdomain.com/api/purchases/next-po-number
   ```

---

## Step 7: Update Your Flutter App Base URL

Once your cPanel API is live, update your Flutter app's base URL:

```dart
// Before (Local development)
static const String baseUrl = 'http://192.168.1.59:8000/api';

// After (cPanel Live Deployment)
static const String baseUrl = 'https://api.yourdomain.com/api';
```

---

## Optional: Connecting to cPanel MySQL Database

If you want to use cPanel's MySQL/MariaDB instead of SQLite:

1. In cPanel, go to **MySQL Databases**.
2. Create a new database: e.g. `yourusername_powersolution`.
3. Create a new user with a secure password and assign **ALL PRIVILEGES** to the database.
4. Install PyMySQL in your virtual environment:
   ```bash
   pip install pymysql cryptography
   ```
5. In cPanel **Setup Python App**:
   - Scroll down to **Environment variables**.
   - Click **Add Variable**:
     - **Name**: `DATABASE_URL`
     - **Value**: `mysql+pymysql://yourusername_dbuser:YourPassword@localhost/yourusername_powersolution`
6. Click **Save** and **Restart** the application.
7. FastAPI will automatically detect the `DATABASE_URL` and create all tables in MySQL!

---

## Troubleshooting Common cPanel Issues

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| **500 Internal Server Error** | Missing dependency or import issue | Check `passenger.log` or run `python passenger_wsgi.py` in cPanel Terminal to see exact traceback. |
| **sqlite3.OperationalError: unable to open database file** | Permission issue | Run `chmod 664 db.sqlite3` and ensure the parent directory is writable (`755`). |
| **Changes not reflecting** | Passenger cached the old code | Click **Restart** in "Setup Python App", or run `touch tmp/restart.txt` inside the app root. |
| **CORS errors in Flutter** | Domain restriction | `main.py` already includes `CORSMiddleware` with `allow_origins=["*"]`, allowing Flutter web and mobile to connect seamlessly. |
