# 📬Feedback Board

A lightweight internal feedback management system , allowing customers to submit feedback through a beautiful glassmorphism UI, while admins manage and track statuses through a secure dashboard.

---

## ✨ Features

- **Public Feedback Form** — Customers submit a title and message with a smooth, RTL-friendly interface
- **Admin Dashboard** — Protected login page for admins to view all submitted feedback
- **Status Tracking** — Three-stage workflow: `ثبت شده` → `در حال بررسی` → `رسیدگی شده`
- **REST API** — Clean FastAPI endpoints for creating, listing, and updating feedback
- **Glassmorphism UI** — Dark-themed, animated interface with Vazirmatn font and RTL layout
- **Session-based Auth** — Simple and secure admin authentication using Starlette sessions
- **SQLite Database** — Zero-config local storage via SQLAlchemy ORM

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | [FastAPI](https://fastapi.tiangolo.com/) |
| ORM        | SQLAlchemy                        |
| Database   | SQLite                            |
| Validation | Pydantic v2                       |
| Templates  | Jinja2                            |
| Frontend   | Vanilla HTML/CSS/JS (RTL, Vazirmatn font) |
| Auth       | Starlette `SessionMiddleware`     |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/basalam-feedback-board.git
cd basalam-feedback-board

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
uvicorn main:app --reload
```

The app will be available at `http://127.0.0.1:8000`

---

## 📖 Usage

### Submitting Feedback (Public)

Navigate to `http://localhost:8000/` to access the public feedback form. Fill in a title and message, then submit.

### Admin Dashboard

1. Go to `http://localhost:8000/login`
2. Enter your admin credentials
3. View all submitted feedback and update their statuses

> ⚠️ **Before deploying**, change the admin credentials and `secret_key` in `main.py`.

---

## 🔌 API Endpoints

| Method  | Endpoint                        | Description                         |
|---------|---------------------------------|-------------------------------------|
| `GET`   | `/api/feedbacks`                | List all feedback entries           |
| `POST`  | `/api/feedbacks`                | Submit new feedback                 |
| `PATCH` | `/api/feedbacks/{feedback_id}`  | Update the status of a feedback     |

Interactive API docs are available at `http://localhost:8000/docs` (Swagger UI).

### Example: Submit Feedback

```bash
curl -X POST "http://localhost:8000/api/feedbacks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Delivery Issue", "message": "My order arrived late."}'
```

### Example: Update Status

```bash
curl -X PATCH "http://localhost:8000/api/feedbacks/1" \
  -H "Content-Type: application/json" \
  -d '{"status": "در حال بررسی"}'
```

---

## 📁 Project Structure

```
feedback-board/
├── main.py            # FastAPI app, routes, and auth logic
├── models.py          # SQLAlchemy database models
├── schemas.py         # Pydantic request/response schemas
├── database.py        # Database engine and session setup
├── requirements.txt   # Python dependencies
├── feedback.db        # SQLite database (auto-created)
├── static/
│   └── images/
│       └── background.png
└── templates/
    ├── index.html     # Public feedback submission page
    ├── login.html     # Admin login page
    └── dashboard.html # Admin feedback management dashboard
```

---

## ⚙️ Configuration

Before going to production, update the following in `main.py`:

```python
# Change these!
ADMIN_USERNAME = "your_admin_username"
ADMIN_PASSWORD = "your_secure_password"
app.add_middleware(SessionMiddleware, secret_key="a-long-random-secret")
```

For production, consider migrating from SQLite to PostgreSQL or MySQL by updating the `SQLALCHEMY_DATABASE_URL` in `database.py`.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
