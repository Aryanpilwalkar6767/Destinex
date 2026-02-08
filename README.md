# 🌍 DESTINEX - AI Powered Travel Discovery

Destinex is an intelligent travel companion that helps you discover the best attractions, hotels, and restaurants in any city. It leverages AI-driven insights to provide personalized travel recommendations and price estimations.

## ✨ Features

- **Smart Search**: Find top-rated places in any city worldwide.
- **AI Insights**: Get unique, AI-generated descriptions for every location, explaining why it's worth visiting.
- **Price Estimation**: Automatic price range estimation (₹, ₹₹, ₹₹₹) based on place type and amenities.
- **Categorized Results**: Easily browse through Attractions, Hotels, and Restaurants.
- **Interactive Map**: Visualize locations on an interactive map (powered by Leaflet).
- **Responsive Design**: Beautiful, mobile-friendly interface.

## 🛠️ Tech Stack

**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)
- Leaflet.js (Maps)

**Backend:**
- Python 3.x
- Flask (Web Framework)
- Geoapify API (Location Data)
- MongoDB (Caching & Data Storage)

## 🚀 Getting Started

### Prerequisites

1. **Python 3.8+** installed.
2. **MongoDB** installed and running locally.
3. **Geoapify API Key** (Get one for free at [geoapify.com](https://www.geoapify.com/)).

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Aryanpilwalkar6767/Destinex.git
   cd Destinex
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   
   # Create a virtual environment (optional but recommended)
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Mac/Linux: source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Environment Configuration:**
   - Create a `.env` file in the `backend` directory.
   - Use `.env.example` as a reference:
   ```env
   GEOAPIFY_API_KEY=your_actual_api_key_here
   MONGO_URI=mongodb://localhost:27017/destinex_db
   ```

4. **Run the Backend:**
   ```bash
   python app.py
   ```
   The server will start at `http://127.0.0.1:5000`.

5. **Run the Frontend:**
   - Open `frontend/index.html` in your browser.
   - Or use a simple HTTP server:
     ```bash
     cd ../frontend
     python -m http.server 5500
     ```
   - Access at `http://localhost:5500`.

## 📂 Project Structure

```
Destinex/
├── backend/
│   ├── app.py                 # Main Flask Application
│   ├── requirements.txt       # Python Dependencies
│   ├── .env                   # Environment Variables (Not committed)
│   ├── .env.example           # Example Environment Variables
│   └── services/
│       ├── ai_service.py      # AI Logic for insights & pricing
│       ├── place_service.py   # Geoapify API integration
│       └── db_service.py      # MongoDB operations
├── frontend/
│   ├── index.html             # Main User Interface
│   ├── styles.css             # Styling
│   └── script.js              # Frontend Logic
└── README.md                  # Project Documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
