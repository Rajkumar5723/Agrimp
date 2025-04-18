# 🌿 Agrimp - Smart Agricultural Assistant

Agrimp is an intelligent web-based platform aimed at improving sustainable farming practices by analyzing soil fertility and recommending suitable crops and nutrient strategies. It is designed to help farmers and agricultural researchers make data-driven decisions for optimized yield.

## 🚀 Features

- 🌱 **Soil Fertility Prediction** – Predicts soil health using AI models.
- 🧪 **Crop Recommendation** – Suggests the best crops based on post-rice soil condition.
- 🧾 **Automated Reports** – Generates detailed analysis reports.
- 📊 **Admin Dashboard** – Manage user and model activities.
- 🧬 **MongoDB Integration** – Secure and scalable NoSQL backend.
- 💡 **Multi-page Design** – Includes login, signup, product showcase, and more.

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Python, Flask
- **Database**: MongoDB
- **Libraries**: scikit-learn, pandas, Flask-PyMongo

## 📁 Folder Structure

```
Agrimp/
│
├── app.py               # Flask application entry point
├── main.py              # Main routing logic
├── mongo_utils.py       # MongoDB helper functions
│
├── pages/               # Core feature logic (crop prediction, report generation)
│   ├── crop.py
│   └── report.py
│
├── templates/           # HTML pages
│   ├── index.html
│   ├── login.html
│   └── ...
│
├── static/              # Static assets
│   ├── css/
│   ├── js/
│   ├── images/
│   └── ...
│
└── README.md            # Project documentation
```

## 🧪 Setup & Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rajkumar5723/Agrimp.git
   cd Agrimp
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. Open your browser and navigate to: `http://127.0.0.1:5000/`

## 📌 To-Do

- Add support for real-time weather APIs
- Enhance model accuracy with more soil features
- Implement multilingual UI support for Indian farmers
