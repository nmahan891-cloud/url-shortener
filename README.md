<div align="center">

# 🔗 Mahan URL Shortener

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📌 Project Introduction

**Mahan URL Shortener** is a complete and professional web application for shortening URLs with advanced features.

> **Note:** This project was built by a 14-year-old developer (Mahan).

---

## ✨ Features

- Shorten URLs with random or custom codes
- Set expiration dates for links
- User registration and login system
- Dashboard to manage links
- Complete statistics with daily and country charts
- QR Code generation for each link
- Bilingual support (Persian & English)
- Fully responsive design

---

## 🛠️ Technologies

| Technology | Description |
|------------|-------------|
| Flask 2.3.3 | Python web framework |
| SQLAlchemy 3.1.1 | ORM for database management |
| Flask-Login 0.6.3 | User authentication |
| QRCode 7.4.2 | QR Code generation |
| Pillow 10.4.0 | Image processing |

---

## 📥 Installation

### Prerequisites
- Python 3.10+
- pip
- git

### Setup Steps

**1. Clone the Project**
```bash
git clone https://github.com/nmahan891-cloud/url-shortener.git
cd url-shortener



Create Virtual Environment
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate

Install Dependencies
pip install -r requirements.txt

Configure Environment Variables
Create a .env file:

SECRET_KEY=your-super-secret-key-change-this-in-production

Run the Project
python run.py

View in Browser
http://127.0.0.1:5000

 Project Structure

 url_shortener/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── utils.py
│   ├── translations.py
│   ├── decorators.py
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── stats.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── profile.html
│       ├── about.html
│       ├── contact.html
│       ├── terms.html
│       ├── privacy.html
│       └── 404.html
├── static/
│   ├── style.css
│   └── script.js
├── instance/
│   └── urls.db
├── screenshots/
│   ├── Screenshot 2026-06-17 104837.png
│   └── Screenshot 2026-06-17 104904.png
├── requirements.txt
├── run.py
├── .env
└── README.md



<div align="center">

# 🔗 کوتاه‌کننده لینک ماهان

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📌 معرفی پروژه

**کوتاه‌کننده لینک ماهان** یک وب‌اپلیکیشن کامل و حرفه‌ای برای کوتاه‌سازی لینک‌ها با قابلیت‌های پیشرفته است.

> **توجه:** این پروژه توسط یک برنامه‌نویس ۱۴ ساله (ماهان) ساخته شده است.

---

## ✨ امکانات

- کوتاه‌سازی لینک با کدهای تصادفی یا دلخواه
- تنظیم تاریخ انقضا برای لینک‌ها
- سیستم ثبت‌نام و ورود کاربران
- داشبورد مدیریت لینک‌ها
- آمار کامل با نمودارهای روز و کشور
- تولید QR Code برای هر لینک
- پشتیبانی از دو زبان فارسی و انگلیسی
- طراحی ریسپانسیو برای همه دستگاه‌ها

---

## 🛠️ تکنولوژی‌ها

| تکنولوژی | توضیح |
|-----------|--------|
| Flask 2.3.3 | فریم‌ورک وب پایتون |
| SQLAlchemy 3.1.1 | ORM برای مدیریت دیتابیس |
| Flask-Login 0.6.3 | مدیریت احراز هویت |
| QRCode 7.4.2 | تولید کدهای QR |
| Pillow 10.4.0 | پردازش تصاویر |

---

## 📥 نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.10 یا بالاتر
- pip
- git

### مراحل نصب

**۱. کلون کردن پروژه**
```bash
git clone https://github.com/nmahan891-cloud/url-shortener.git
cd url-shortener
