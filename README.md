# Bank-System
A console-based Python banking system that supports user registration, secure login with password hashing, account creation, deposits, withdrawals, transfers, and transaction history. Data is saved in JSON/CSV format to ensure persistence across sessions.

Sure! Here's a clear and professional **project description** for your **OOP-based Bank System** in Python:

---

 🏦 Bank System – Project Description

 📌 Overview:
The **Bank System** is a console-based application developed in **Python** using the **Object-Oriented Programming (OOP)** paradigm. It simulates the core functionalities of a real-world banking platform, including user registration, account management, transactions (deposit, withdraw, transfer), and secure authentication.

This project serves as a practical demonstration of OOP concepts such as classes, inheritance, encapsulation, and file handling, while also implementing basic security practices like password hashing.

---

 🎯 Objectives:
- Create and manage user profiles
- Open and manage multiple bank accounts per user
- Perform financial operations (deposit, withdraw, transfer)
- Track and display transaction history
- Ensure secure access via login and hashed passwords
- Store and retrieve data using local files (JSON/CSV/Pickle)

---

 ⚙️ Core Features:

 👤 User Management:
- User registration with full name, phone number, and password
- Login system with authentication
- Passwords are hashed using `hashlib` for security
- Block user access after 3 failed login attempts

 💳 Account Management:
- Each user can create multiple bank accounts
- Unique account number generation
- Multiple currency support (default: USD)

 💰 Transactions:
- Deposit, withdraw, and transfer money between accounts
- Automatic creation of a transaction record for each operation
- Detailed account statements available for users

 💾 Data Persistence:
- All user and account data is saved to a file (JSON/CSV/Pickle)
- Data is automatically loaded on system startup

---

 🔒 Security:
- Encrypted (hashed) password storage
- Login attempts are limited to prevent brute force attacks
- Session-based access: user must log in to perform operations

---

 🧪 Test Scenarios:
- Registering a new user
- Logging in with valid/invalid credentials
- Creating a bank account
- Depositing and withdrawing funds
- Transferring money between accounts
- Viewing transaction history
- Verifying data persistence after restart

---

 💡 Optional Enhancements:
- Currency conversion with real or mock exchange rates
- Admin dashboard for viewing users and statistics
- Simulated notifications (SMS/email)
- GUI version using Tkinter

---

This project is ideal for anyone looking to strengthen their understanding of OOP in Python while building a real-world-style application with security, data storage, and multi-user interaction.

---
