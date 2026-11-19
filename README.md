# 🛒 ShopEasy – Full Stack E-Commerce Website

A full-stack e-commerce web application developed using **Python and Django**, providing separate experiences for buyers and sellers.

## 📌 Project Overview

ShopEasy is an online shopping platform designed to simplify product browsing, shopping cart management, and order processing. It provides role-based access for buyers and sellers, with dedicated dashboards and functionalities.

## 🎯 Project Objectives

- Develop a complete e-commerce application using Django.
- Implement buyer and seller authentication.
- Provide role-based dashboards and access control.
- Manage products, shopping carts, and customer orders.
- Understand real-world full-stack web development.

## ✨ Key Features

### 👤 Buyer Module
- Buyer registration and login.
- Browse available products.
- View product details.
- Add products to the shopping cart.
- Manage cart quantities.
- Checkout and place orders.
- View order information.

### 🏪 Seller Module
- Seller registration and login.
- Dedicated seller dashboard.
- Manage product information.
- View customer orders.
- Manage order-related operations.

### 🔐 Authentication & Security
- Custom user authentication.
- Role-based access control.
- Protected pages using Django authentication.
- Separate buyer and seller experiences.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| HTML5 | Page structure |
| CSS3 | Styling |
| Bootstrap | Responsive design |
| JavaScript | Interactive functionality |
| SQLite | Database |
| Git & GitHub | Version control |

## 📂 Project Structure

```text
ShopEasy/
│
├── shopeasy/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── store/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── templates/
├── static/
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Aminafaiza/E-Commerce-Website-ShopEasy.git
```

### 2. Navigate to the project directory

```bash
cd E-Commerce-Website-ShopEasy
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment (Windows)

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open your browser and visit:

http://127.0.0.1:8000/

## 📸 Screenshots

Screenshots of the application will be added here to demonstrate its main features and user interfaces.

## 🚀 Future Enhancements

- Online payment gateway integration.
- Product reviews and ratings.
- Email notifications.
- Advanced product search and filtering.
- Improved order tracking.

## 👩‍💻 Developed By

**Aminafaiza**

GitHub: https://github.com/Aminafaiza

---

*ShopEasy – Making Online Shopping Simple!*
