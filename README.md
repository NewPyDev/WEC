# 🚀 EcomManager Pro (SaaS Ready)

A powerful, mobile-first inventory and order management system built with **Django**. Designed for small businesses to track products, manage clients, and generate professional PDF invoices on the go.

<<<<<<< HEAD
![Dashboard Preview](https://raw.githubusercontent.com/NewPyDev/WEC/main/GH%20Dashboard.png)
=======
![Dashboard Preview]([https://github.com/NewPyDev/WEC/blob/319e9f2f4d7ff06eaee55a74fc82fbb25d5c79d7/GH%20Dashboard.png])
>>>>>>> c659c6641de351c105dc86e0559480016caebcbb

## ✨ Key Features

*   **📱 Mobile-First Design**: Fully responsive UI that works perfectly on phones (app-like experience) and desktops.
*   **📦 Smart Inventory**: Track stock levels, sizes (S, M, L, XL), colors, and profitability per item.
*   **🧾 Professional Invoices**: One-click generation of branded PDF invoices with QR codes for shipping.
*   **👥 Client Management**: Built-in CRM to track customer details and order history.
*   **🔒 Multi-Tenant Security**: Data is strictly isolated per user. Ideal for SaaS deployment (one instance, many paying users).
*   **📊 Analytics Dashboard**: Real-time insights into revenue, active orders, and stock value.

## 🛠️ Tech Stack

*   **Backend**: Python 3.10+, Django 4.2
*   **Database**: PostgreSQL (Production) / SQLite (Dev)
*   **Frontend**: Bootstrap 5, Custom CSS3 (Glassmorphism), JavaScript
*   **PDF Engine**: xhtml2pdf
*   **Deployment**: Ready for PythonAnywhere, AWS, or DigitalOcean.

## 🚀 Quick Start (Demo)

We have a public demo available!
*   **URL**: `(https://hamidaseike.pythonanywhere.com/accounts/login/)`
*   **Username**: `test`
*   **Password**: `test`

*(Note: The demo account is strictly isolated. You cannot see other users' data.)*

## 💿 Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/ecom-manager.git
    cd ecom-manager
    ```

2.  **Set up Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Create Admin User**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run Server**
    ```bash
    python manage.py runserver
    ```

## 🔐 Security Features

*   **Data Isolation**: Every view is protected with `request.user` filtering. Users can NEVER access another store's inventory.
*   **Secure Authentication**: Standard Django auth system.
*   **CSRF Protection**: Enabled on all forms.

## 💰 Monetization / White Labeling

This project is structured for easy white-labeling:
1.  **Logo Customization**: Users can upload their own company logo for invoices.
2.  **Scalable**: Postgres backend supports thousands of users.
3.  **Subscription Ready**: Verified data isolation makes it easy to add a Stripe subscription layer.

---
© 2026 EcomManager Pro. All Rights Reserved.
