# Car Listing App

## Overview
This is a full-stack web application for listing and viewing cars for sale. Sellers can upload car details, including five images, and buyers can view listings with contact details. The application consists of a **Flask backend** and a **React frontend**.

## Features
- User authentication (Buyer, Seller, Admin)
- Sellers can add, update, and delete car listings
- Buyers can view car details, including images and seller contact
- Admins can manage listings
- Image slideshow with a full-screen view

---

## Backend (Flask) Setup

### Prerequisites
- Python 3.8+
- Pip

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/car-listing-app.git
   cd car-listing-app/backend
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```sh
   python -c "from app import db; db.create_all()"
   ```
5. Start the server:
   ```sh
   flask run
   ```
   The API will be available at `http://127.0.0.1:5000/`

---

## Frontend (React) Setup

### Prerequisites
- Node.js (16+ recommended)
- npm or yarn

### Installation
1. Navigate to the frontend folder:
   ```sh
   cd ../frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the development server:
   ```sh
   npm start
   ```
   The frontend will be available at `http://localhost:3000/`

---

## Deployment

### Deploy Backend (Flask)
- Use **Heroku, AWS, or DigitalOcean** to deploy Flask.
- Configure the database (PostgreSQL recommended for production).
- Set environment variables for JWT secret and database URL.

### Deploy Frontend (React)
- Use **Netlify or Vercel**.
- Update API URLs in React to point to the deployed backend.
- Run:
  ```sh
  npm run build
  ```
- Upload the `build/` folder to Netlify or Vercel.

---

## API Endpoints
| Method | Endpoint         | Description                |
|--------|-----------------|----------------------------|
| POST   | /register       | Register a new user       |
| POST   | /login          | Authenticate and get token |
| GET    | /cars           | Get all car listings      |
| POST   | /cars           | Add a new car (Sellers)   |
| DELETE | /cars/<id>      | Delete a car (Seller/Admin) |

---

## License
This project is open-source and free to use.


