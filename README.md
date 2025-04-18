# Supplier Connect API

This is a simple RESTful API built with Python Flask for a **Supplier Connect** application. It provides basic user authentication, supplier listings, product details, and order submission functionalities for integration with a Flutter app.

## 🌐 Live API

[https://flutter-api-sigma.vercel.app/](https://flutter-api-sigma.vercel.app/)

---

## 🔐 Sample Login Credentials (Dummy Users)

| Username | Password |
|----------|----------|
| user1    | pass1    |

---

## 📦 Features

- User Login and Token-Based Authentication
- List All Suppliers
- View Supplier Details with Products
- Submit Orders with Items and Total Amount
- Uses SQLite for Local Data Storage

---

## 📋 API Endpoints

### 🔑 `POST /login`

Authenticate user and return session token.

**Request Body:**
```json
{
  "username": "user1",
  "password": "pass1"
}
