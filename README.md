# 🌾 Smart Crop Recommendation System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![Machine Learning](https://img.shields.io/badge/Model-Random%20Forest-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📌 Overview
The **Smart Crop Recommendation System** is an intelligent web application designed to assist farmers and agricultural enthusiasts in making informed decisions. By leveraging **Machine Learning (Random Forest)**, the system analyzes soil nutrients (Nitrogen, Phosphorus, Potassium) and environmental factors (Temperature, Humidity, pH, Rainfall) to predict the most suitable crop for cultivation.

This project aims to bridge the gap between technology and agriculture, promoting precision farming to maximize yield and profitability.

## 🚀 Features

### 👤 User Features
* **Secure Authentication:** User signup, login, and secure profile management.
* **AI Predictions:** Real-time crop recommendations based on 7 distinct agricultural parameters.
* **Prediction History:** Users can save, view, and delete their past prediction results.
* **Profile Management:** Update personal details and manage account security.

### 🛠 Admin Dashboard
* **Data Analytics:** Visual insights into user registrations and prediction trends using charts.
* **User Management:** View and manage registered users.
* **Prediction Monitoring:** Filter and analyze all predictions made on the platform by date or crop type.

## 🛠️ Tech Stack

* **Backend:** Django 5 (Python Framework)
* **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
* **Machine Learning:** Scikit-Learn (Random Forest Classifier), Pandas, NumPy
* **Database:** SQLite (Default) / PostgreSQL (Production ready)
* **Visualization:** Chart.js (for Admin Dashboard)

## 📂 Project Structure

crop-recommender/ │ ├── crop_site/ # Main Django Project Configuration ├── recommender/ # Main App Logic │ ├── ml/ # Machine Learning Model & Loader │ ├── templates/ # HTML Templates │ ├── static/ # CSS, Images, JS │ ├── models.py # Database Models │ └── views.py # Application Logic ├── manage.py # Django Command Line Utility ├── requirements.txt # Project Dependencies └── README.md # Project Documentation


## ⚙️ Installation & Setup

Follow these steps to run the project locally on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/crop-recommender.git](https://github.com/YourUsername/crop-recommender.git)
cd crop-recommender
2. Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

Bash

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash

pip install -r requirements.txt
(Note: If requirements.txt is missing, install manually: pip install django scikit-learn pandas numpy)

4. Apply Migrations
Set up the database tables.

Bash

python manage.py makemigrations
python manage.py migrate
5. Create a Superuser (Admin)
To access the Admin Dashboard.

Bash

python manage.py createsuperuser
6. Run the Server
Bash

python manage.py runserver
7. Access the Application
Open your browser and navigate to: http://127.0.0.1:8000/
