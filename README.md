# 🎓 LMS Project (Learning Management System)

A full-stack Learning Management System (LMS) built using **Django**, designed to simulate a real-world online learning platform with role-based functionality and payment integration.

---

## 🚀 Features

* 🔐 User Authentication (Custom User Model)
* 👨‍🎓 Student Dashboard
* 👨‍🏫 Instructor Role Support
* 📚 Course Creation & Management
* 🎥 Video-based Learning Content
* 💳 Payment Integration (Razorpay - Test Mode)
* 📊 Course Enrollment System
* 📁 Organized static & media handling

---

## 🛠 Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite (Development), PostgreSQL (Production-ready)
* **Payment Gateway:** Razorpay (Test Integration)

---

## ⚠️ Important Note

> This project is built for **learning and demonstration purposes only**.

* The courses and videos included in this project are **dummy/sample content** created to showcase functionality.
* The payment gateway (**Razorpay**) is integrated in **test mode only** and is used purely for demonstration.
* This is **NOT a production-ready application**.

---

## 📂 Project Structure

```
lms/
├── accounts/
├── courses/
├── payments/
├── templates/
├── static/
├── media/
├── manage.py
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/VaibhavJD0911/lms.git
cd lms
```

---

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run migrations

```bash
python manage.py migrate
```

---

### 5. Run server

```bash
python manage.py runserver
```

---

## 🔐 Environment Variables (For Deployment)

Create a `.env` file or add environment variables:

```
SECRET_KEY=your_secret_key
DEBUG=True

# PostgreSQL (Production)
DATABASE_URL=your_database_url

# Razorpay
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret
```

---

## 🌐 Deployment

This project is ready to be deployed on platforms like:

* Render
* Railway

---

## 📌 Future Improvements

* REST API integration
* React frontend
* Real payment validation
* Course reviews & ratings
* Admin analytics dashboard

---

## 👨‍💻 Author

Developed by VaibhavJD

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
