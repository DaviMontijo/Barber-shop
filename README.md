<h1 align="center"> Barber Shop Management System & Relational Database</h1>

<p align="center">
  <img
    src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&pause=1000&color=2E9EF7&center=true&vCenter=true&width=550&lines=Barbershop+Management+System+%F0%9F%92%88;Python+%7C+Flask+%7C+SQLite3;Full+CRUD+%2B+WCAG+2.1+Accessibility;Project+under+continuous+development+%F0%9F%9A%80"
    alt="Typing SVG"
  />
</p>

---

### 📌 About the Project

**Estilo & Corte Barber Shop** is a web system designed to manage registration and operational control for a real-world barber shop. The application provides full **CRUD operations** (Create, Read, Update, and Delete) for professionals (**Barbers**) and **Services**, resolving the **N:M (Many-to-Many)** relationship between them using an associative junction table in the database.

This project was built focusing on core principles of **web development with Flask**, **relational database modeling (3NF)**, and **digital accessibility (WCAG 2.1 - Level AA)**.

> 🚀 **Project Evolution:** This repository will undergo **continuous implementations throughout the year**, adding new business features, backend optimizations, and interface enhancements.

---

### 🧠 Logic & System Architecture

#### 1. Resolving the $N:M$ Relationship
In the barber shop business domain, **a barber can perform multiple services**, and **a service can be offered by multiple barbers**.
- The association is managed through a pivot table (`barbeiro_servico`) within the `barbershop.db` file.
- The database enforces foreign key constraints with `ON DELETE CASCADE`. Removing a barber or a service automatically deletes their related links.
- To ensure reference integrity in SQLite3, the `PRAGMA foreign_keys = ON;` command is enabled upon establishing database connections.

#### 2. Optimized SQL Query (`GROUP_CONCAT`)
To display professionals along with their respective services without duplicating rows or overloading the database with unnecessary queries:
- The system uses a `LEFT JOIN` statement combined with the `GROUP_CONCAT(s.nome_servico, ', ')` aggregate function.
- This returns all services assigned to each barber consolidated into a single string, ready for Jinja2 template rendering.

#### 3. Codebase Organization
- **`app.py`**: Acts as the main controller for the Flask application, handling HTTP routes, POST/GET request processing, and template rendering.
- **`model.py`**: Centralizes data manipulation and persistence functions interacting with SQLite3.
- **`templates/`**: Contains HTML pages rendered by Jinja2.

---

### ♿ Accessibility (WCAG 2.1 - Level AA)

The interface was designed and audited according to international accessibility guidelines:

- **0 Violations on axe DevTools (`forms-label`):** Form controls (`<input>`) are explicitly linked to their corresponding `<label>` elements.
- **Score 100 on Google Lighthouse (`color-contrast`):** Text-to-background contrast ratio exceeds **7:1**, ensuring optimal readability.
- **Touch Target Size (`target-size`):** Interactive elements (such as service checkboxes) have appropriate physical target areas for ease of tapping and clicking.
- **Non-Reliance on Color Alone (`use-of-color`):** Error and success feedback messages incorporate descriptive text and visual indicators alongside color coding.
- **Responsive Design (`reflow`):** Adaptable layout for mobile screens powered by CSS media queries in `style.css`, eliminating horizontal scrolling.

---

### 🛠️ Technologies Used

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=py,flask,sqlite,html,css,git,github" alt="Technologies Used" />
  </a>
</p>

- **Backend Language:** Python 3
- **Web Framework:** Flask (Jinja2)
- **Database:** SQLite3 (`barbershop.db`)
- **Styling & Layout:** Semantic HTML5 & CSS3 (`style.css`)
- **Accessibility Audit:** Google Lighthouse & axe DevTools

---

### 📂 Repository Structure

```text
CRUD---Barber-shop/
├── static/
│   ├── css/
│   │   └── style.css            # Visual styles and WCAG accessibility rules
│   └── img/
│       └── barbearia.jfif       # Application image assets
├── templates/
│   ├── index.html               # Home page
│   ├── barbeiro.html            # Barber listing and registration view
│   ├── editar_barbeiro.html     # Barber editing form
│   ├── servico.html             # Service listing and registration view
│   └── editar_servico.html      # Service editing form
├── .gitignore                   # Git ignore rules
├── app.py                       # Flask application server and routing
├── barbershop.db                # SQLite3 relational database file
├── model.py                     # Database helper functions and business logic
└── README.md                    # Project documentation
