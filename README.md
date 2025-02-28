---

# 🚀 **Blog API** - Django REST Framework  

![Blog API](https://i.gifer.com/3AyY.gif)  

📢 A powerful and scalable **Blog API** built with Django and Django REST Framework (DRF).  
Manage **posts, categories, tags, and comments** effortlessly with a well-structured API.  

---

## 🌟 **Features**
✅ Create, read, update, and delete (CRUD) blog posts  
✅ Nested comments with replies  
✅ Categories and tags for better post organization  
✅ Pagination & filtering  
✅ Fully RESTful API with **JWT authentication**  

---

## 📂 **Project Structure**
```
📦 blog-api
├── 📁 apps
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   └── tests.py
├── 📁 config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── ...
├── 📁 static
│   ├── css/
│   ├── js/
│   ├── images/
├── manage.py
└── README.md
```

---

## 🚀 **Installation & Setup**
🔹 **Step 1**: Clone the repository  
```sh
git clone https://github.com/your-username/blog-api.git
cd blog-api
```
🔹 **Step 2**: Create and activate a virtual environment  
```sh
python -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate  # Windows
```
🔹 **Step 3**: Install dependencies  
```sh
pip install -r requirements.txt
```
🔹 **Step 4**: Apply migrations and start the server  
```sh
python manage.py migrate
python manage.py runserver
```

---

## 🎯 **API Endpoints**
### 📌 **Posts**
🔹 Get all posts:  
```sh
GET /api/posts/
```
🔹 Create a new post:  
```sh
POST /api/posts/
```

### 💬 **Comments**
🔹 Get comments for a post:  
```sh
GET /api/posts/{post_slug}/comments/
```
🔹 Add a comment:  
```sh
POST /api/posts/{post_slug}/comments/
```

### 🏷 **Categories & Tags**
🔹 List all categories:  
```sh
GET /api/categories/
```
🔹 List all tags:  
```sh
GET /api/tags/
```

📜 **[View Full API Documentation](https://your-docs-link.com)**

---

## 🔒 **Authentication**
This API uses **JWT Authentication**. To obtain an access token:
```sh
POST /api/token/
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```
Use the token in the **Authorization** header for protected routes:
```
Authorization: Bearer your_access_token
```

---

## 🛠 **Tech Stack**
🚀 **Backend**: Django, Django REST Framework  
🛢 **Database**: PostgreSQL / SQLite  
🛡 **Authentication**: JWT (JSON Web Token)  
📡 **Deployment**: Docker, Heroku, AWS  

---

## 🤝 **Contributing**
We welcome contributions!  
1. Fork this repo  
2. Create a new branch (`feature-xyz`)  
3. Commit changes (`git commit -m "Add feature xyz"`)  
4. Push to your branch (`git push origin feature-xyz`)  
5. Open a **Pull Request** 🎉  

---

## 💬 **Contact & Support**
👨‍💻 **Author**: [Your Name](https://github.com/rinkuo)  
📧 **Email**: your-email@example.com  
🔗 **GitHub**: [https://github.com/your-username](https://github.com/rinkuo)  

Give this repo a ⭐ if you like it! 🚀✨  

---
