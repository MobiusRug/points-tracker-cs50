# Points Tracker

#### 🎥 Video Demo: [https://www.youtube.com/watch?v=2pNu_k93Qfo](https://www.youtube.com/watch?v=2pNu_k93Qfo)

#### 👤 Author: Bleider Roger Freitas dos Santos

#### 📚 Project for CS50x – Harvard's Introduction to Computer Science

---

## 🌐 Live Demo

You can try a temporary hosted version of the application at:  
🔗 [https://eldude.pythonanywhere.com](https://eldude.pythonanywhere.com)

> ⚠️ Note: This is a free-tier deployment, and performance may vary. Downtime or slow responses are expected occasionally due to resource limits.

---

## 📝 Description

**Points Tracker** is a lightweight, yet practical web application created to address a specific productivity challenge faced by public servants in Brazil, particularly analysts working for the **National Social Security Institute (INSS)**. These employees are responsible for analyzing a large number of administrative processes that citizens submit for benefits such as pensions, retirement, or social assistance.

Each of these administrative processes has a specific **point value** associated with it, depending on its complexity. The institution sets a **monthly points goal** for each employee, which they must achieve by distributing their work over the available business days. However, there is no built-in government system that allows them to see their progress in real time. This lack of visibility often forces workers to rely on personal spreadsheets, hand-written notes, or approximate estimations.

This is where **Points Tracker** comes in — a digital solution designed to bridge that gap. By allowing users to quickly log cases, track their current and cumulative point totals, and switch between months, it provides a more structured and accurate way to measure daily and monthly productivity.

### ✅ Key Features

- **User Authentication**  
    Users can register and log in with a username and password. All routes (except login/register) are protected by session validation.
    
- **Dynamic Form Submission**  
    The app features a form where users submit protocol numbers and select a case type from a dropdown. When a case type is chosen, the corresponding point value is automatically filled in.
    
- **Monthly Filter ("Competência")**  
    Users can choose a specific month and year to view their productivity. This is implemented with a custom dropdown that uses a compact calendar-like layout.
    
- **Today’s Productivity and Monthly Totals**  
    The dashboard shows both today's contributions and the full month's data (depending on the selected filter), complete with timestamps and scores.
    
- **AJAX-Powered Deletion**  
    Entries can be deleted instantly with a trash icon next to each row. This is handled asynchronously to improve user experience and avoid page reloads.
    

---

## 🛠️ Technologies Used

- **Python** – Backend logic and routing via Flask
    
- **Flask** – Lightweight web framework
    
- **SQLite** – Embedded database for local storage
    
- **HTML5 + CSS3** – Front-end structure and style
    
- **Bootstrap 5** – Responsive and clean layout
    
- **JavaScript (AJAX)** – Asynchronous deletion of entries
    
- **Jinja2** – Flask’s templating engine for rendering dynamic content
    

---

## 🗂️ Project Structure

controle_pontos_project/
├── app.py # Main Flask application
├── helpers.py # Login decorator and utilities
├── controle.db # SQLite database
├── static/
│ ├── styles.css # Custom CSS
├── templates/
│ ├── index.html # Main interface
│ ├── login.html # Login form
│ ├── register.html # Registration form
├── README.md # This file
└── requirements.txt # Dependencies (optional)


---

## 🚀 Running Locally

To run the project on your own machine, follow these steps:

1. **Clone the repository:**
    
    `git clone git@github.com:MobiusRug/points-tracker-cs50.git
    
2. **(Optional) Set up a virtual environment:**
    
    `python3 -m venv venv source venv/bin/activate   # On Windows: venv\Scripts\activate`
    
3. **Install the required packages:**
    
    `pip install flask werkzeug`
    
4. **Run the Flask server:**
    
    `flask run`
    
5. **Open your browser** and navigate to:  
    `http://127.0.0.1:5000/`
    

> ⚠️ Make sure Python 3 and Flask are correctly installed.

---

## 💡 Design Decisions

- **Minimalistic UI**: The interface is intentionally clean and simple, focused on reducing friction for repeated daily entries.
    
- **Custom Competência Selector**: Instead of using a traditional `<select>` or `<input type="month">`, a custom dropdown was created. This allowed full control over the display of months and navigation of years.
    
- **AJAX for Deletion**: Using JavaScript to delete entries asynchronously avoids reloading the page and preserves user context (like current month filter).
    
- **Flat Schema**: For simplicity and maintainability, the SQLite database has a single `producao` table with just the essential fields.
    
- **Login Decorator**: A `login_required` decorator ensures only logged-in users can access the dashboard and interact with the data.
    

---

## 📌 Limitations and Future Plans

While this project is already functional and solves a real-world problem, it has certain limitations that could be addressed in future iterations.

### Current Limitations:

- **No Admin Interface**: Point values for each case type are fixed in the database and cannot be edited through the UI.
    
- **No Mobile App**: While the interface is responsive, it’s not optimized as a Progressive Web App (PWA) or for offline use.
    
- **Basic Authentication**: There’s no password recovery, email verification, or session expiration.
    
### Planned Features:

- 📈 Charts showing daily/monthly performance over time
    
- 🧮 Automatic goal calculation (e.g., points/month)
    
- ⚙️ Admin panel to edit case types and values
    
- ☁️ Deployment on Render, Fly.io, or other scalable hosting services
    
- 📬 Email verification and multi-factor authentication
    

---

## 🙏 Final Note

This project was inspired by a genuine productivity challenge faced in the Brazilian public sector. It shows how basic web development skills can create solutions that bring immediate value to real people.

**CS50x** has been an incredibly valuable learning journey, and this final project is a reflection of how foundational computer science concepts can be applied to personal and professional contexts.

> “A small tool to solve a real-world problem in public service.”
