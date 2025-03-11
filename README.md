# ProDev BE - Job Board Backend

## **Overview**
**Job Board Platform system** is designed to provide efficient job postings, secure authentication, role-based access control, and optimized job searches. Built with **Django REST Framework (DRF)**, the backend includes **Chapa payment integration, Celery for email alerts, and API documentation via Swagger and Redoc**.

The frontend implementation is developed using **React Vite** for a fast and modern user experience.

## **Key Features**

### **1. Job Posting Management**
- APIs for creating, updating, deleting, and retrieving job postings.
- Categorization of jobs by **industry, location, and type**.
- Integrated **Chapa payment** for job post submissions.

### **2. Role-Based Authentication**
- Uses **JWT authentication** for secure user management.
- Role-based access control for **admins, employers, and job seekers**.
- Employers can **manage job listings**, while job seekers can **apply for jobs**.

### **3. Optimized Job Search**
- **Indexing and optimized queries** for fast job retrieval.
- **Location-based and category-based filtering**.
- Advanced **search and filtering options** for job seekers.

### **4. Automated Email Alerts with Celery**
- **Daily/weekly job alerts** for job seekers.
- Asynchronous **email notifications using Celery** for high performance.

### **5. API Documentation**
- Comprehensive API documentation using **Swagger & Redoc**.
- Available at **`/api/docs/`** for easy frontend integration.

---

## **Tech Stack**
| Technology | Purpose |
|------------|---------|
| **Django** | High-level Python framework for rapid development |
| **Django REST Framework (DRF)** | API development and request handling |
| **PostgreSQL** | Database for storing job board data |
| **JWT** | Secure authentication and role-based access control |
| **Swagger & Redoc** | API documentation |
| **Celery & Redis** | Background task processing (email alerts) |
| **Chapa Payment API** | Payment processing for job posting submissions |
| **React Vite** | Frontend implementation for fast and modern UI |

---

## **Project Setup & Installation**

### **1. Clone the Repository**
```sh
$ git clone https://github.com/yourusername/prodev-be.git
$ cd prodev-be
```

### **2. Create a Virtual Environment**
```sh
$ python -m venv venv
$ source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3. Install Dependencies**
```sh
$ pip install -r requirements.txt
```

### **4. Configure Environment Variables**
Create a `.env` file and configure:
```sh
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://user:password@localhost:5432/jobboard
CHAPA_SECRET_KEY=your_chapa_key
REDIS_URL=redis://localhost:6379
```

### **5. Apply Migrations & Run Server**
```sh
$ python manage.py migrate
$ python manage.py runserver
```

### **6. Start Celery Worker (For Email Alerts)**
```sh
$ celery -A prodev worker --loglevel=info
```

### **7. Access API Documentation**
- Swagger UI: **http://127.0.0.1:8000/swagger/**
- Redoc Docs: **http://127.0.0.1:8000/api/docs/**

---

## **API Endpoints**
### **Authentication**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/api/token/` | Get JWT token |
| `POST` | `/api/token/refresh/` | Refresh JWT token |
| `GET` | `/auth/user/` | Get logged-in user info |

### **Job Management**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/jobposts/` | Retrieve all job posts |
| `POST` | `/jobposts/` | Create a new job post (requires authentication) |
| `GET` | `/jobposts/{id}/` | Retrieve a specific job post |
| `PUT/PATCH` | `/jobposts/{id}/` | Update a job post (admin/employer only) |
| `DELETE` | `/jobposts/{id}/` | Delete a job post (admin only) |

### **Categories & Job Types**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/categories/` | Retrieve all job categories |
| `GET` | `/jobtypes/` | Retrieve all job types |

### **Companies**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/companies/` | Retrieve all companies |
| `POST` | `/companies/` | Register a new company |

### **Payments (Chapa Integration)**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/payments/` | Initiate payment for job posting |
| `GET` | `/payments/{tx_ref}/` | Check payment status |

---

## **Security Features**
- **JWT-based authentication** for secure access control.
- **Role-based permissions** ensuring only authorized users can create/manage jobs.
- **CSRF & CORS Protection** with Django's security settings.

---

## **Contributing**
### **Guidelines**
1. Fork the repository and create a feature branch.
2. Write clear, maintainable, and well-documented code.
3. Run tests before submitting a pull request.
4. Follow Python's PEP 8 coding style.

### **Run Tests**
```sh
$ python manage.py test
```

---

## **License**
This project is licensed under the **MIT License**.

---

## **Contact & Support**
For questions, feature requests, or support, please contact:
- **Developer:** Meshack Mutune
- **Email:** meshack3197@gmail.com
- **GitHub:** [your-github-profile](https://github.com/yourusername)

---