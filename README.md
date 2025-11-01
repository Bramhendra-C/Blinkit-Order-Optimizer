# ⚡ Blinkit Order Optimizer 🛵

A proof-of-concept system for instant-delivery services combining **geospatial calculations** and **graph algorithms** to find the fastest delivery route.

🖼️ Screenshots & Visuals
Frontend UI Preview


### 📍 Optimized Route Results  
![System UI](./Demo/Demo-2.jpg)
### 📊 Delivery Summary Card
![System UI](./Demo/Demo-1.jpg)
---

## 🚀 Live Demo  
Check out the live frontend here:  
[https://bramhendra-c.github.io/Blinkit-Order-Optimizer/](https://bramhendra-c.github.io/Blinkit-Order-Optimizer/)

---

## 🧩 Key Features

- **FastAPI Backend:**  
  High-performance API endpoint (`/optimize_route`) for handling delivery route calculations.

- **Geospatial Modeling:**  
  Uses the **Haversine formula** to compute distances between any two geographic points on Earth.

- **Routing Optimization Algorithm:**  
  Implements a **Nearest Neighbor heuristic** to approximate the Traveling Salesman Problem (TSP) — fast and scalable for dense delivery zones.

- **Real-time ETA & Distance:**  
  Computes total Estimated Time of Arrival (ETA) and distance based on an average delivery speed (default: 30 km/h).

- **Responsive Frontend UI:**  
  Built with **HTML5 + Tailwind CSS**, allowing users to input coordinates and view a step-by-step optimized route.

- **Resilient Networking:**  
  Frontend includes an **Exponential Backoff** retry mechanism for robust API communication.

---

## 🛠 Tech Stack

| Component       | Technology                     | Role                                                |
|-----------------|--------------------------------|-----------------------------------------------------|
| Backend         | Python 3.x, FastAPI     | API server for optimization logic                   |
| Logic Core      | Python (math library)          | Haversine distance & Nearest Neighbor optimization  |
| API Server      | Uvicorn (ASGI)         | Runs the FastAPI application                        |
| Frontend        | HTML, Tailwind CSS             | User interface and visualization                     |
| Integration     | JavaScript (Fetch API, CORS)   | Connects frontend to backend, handles retry logic   |

---

## 📐 How It Works

The system addresses a version of the Traveling Salesman Problem (TSP): **visit all customer points once, starting from a store, and return (optional)** with minimal time/distance.

### Steps:

1. **Distance Calculation:**  
   The `haversine` function uses the Haversine formula to compute great-circle distances (in km) between two lat-lon points.

2. **Time Estimation:**  
   Travel time is derived by converting distance into time using a fixed average speed (default = 30 km/h).

3. **Routing Strategy:**  
   The `nearest_neighbor_optimization` function:  
   - Starts at the store location.  
   - Repeatedly selects the nearest unvisited customer location.  
   - Continues until all drop-offs are done.  
   - Returns a sequence of segments, total distance, total time, and the visitation order.

### Trade-Offs  
- The Nearest Neighbor heuristic is **fast and scalable**, making it suitable for many stops.  
- However, it **does not guarantee** the absolute shortest route (i.e., *optimal*) — more advanced algorithms (Simulated Annealing, Branch & Bound, etc.) would be required for that.

---

## 📁 Repo Structure

Blinkit-Order-Optimizer/
│
├── optimizer_api.py ← FastAPI backend code
├── optimizer_frontend.html ← Frontend UI (HTML + Tailwind)
├── requirements.txt ← Python dependencies
├── render.yaml ← (optional) Render.com deployment spec
├── README.md ← This file
└── assets/ ← Screenshots, banner images etc.
├── banner.png
├── screenshot1.png
└── screenshot2.png


---

## 🔧 Getting Started (Locally)

### Prerequisites  
- Python 3.8+ installed on your machine.

### Backend Setup

1. Install dependencies:

   ```bash
   pip install fastapi uvicorn pydantic python-multipart starlette-cors
2.Run the API server:
  uvicorn optimizer_api:app --reload
The server will be available at http://127.0.0.1:8000.

3.Verify the root endpoint:
    GET http://127.0.0.1:8000/
You should receive:

{
  "message": "Blinkit Order Optimizer API is running. Use the /optimize_route endpoint."
}
Frontend Setup

1.Open optimizer_frontend.html in your browser (double-click the file or use Live Server).

2.Ensure the API_URL in the script matches your running backend.
  const API_URL = 'https://blinkit-order-optimizer-1.onrender.com/optimize_route';
3.Load demo data and click "Calculate Fastest Route" to test.
🌐 Deployment
Backend (Render.com)

Add requirements.txt and (optionally) render.yaml.

On Render.com: create a new Web Service, connect your GitHub repo, set build command to pip install -r requirements.txt, and start command to:
uvicorn optimizer_api:app --host 0.0.0.0 --port $PORT
After deployment, the service will provide a public URL (e.g., https://blinkit-order-optimizer-1.onrender.com).

Update API_URL in the frontend to point to this live backend.

Frontend (GitHub Pages, Static Site)

Host the optimizer_frontend.html in your repository or another dedicated repo.

Enable GitHub Pages or another static site hosting platform.

Live demo link: https://bramhendra-c.github.io/Blinkit-Order-Optimizer/

Ensure the API_URL in your HTML matches the live backend endpoint.

### 🧭 Usage Guide

Go to the Live Demo link above.

In the “Input Locations” panel:

Enter the store location (latitude, longitude).

Enter one or more customer drop-off points (each lat, lon pair on a new line).

Click “Use Demo Data” to auto-fill example locations.

Click Calculate Fastest Route.

View the “Optimization Result” — sequence of drop-offs, distance/time per leg, total distance, total time.

Inspect the “Delivery Summary” card for overall metrics.

### 🚧 Future Enhancements

VRPTW (Vehicle Routing Problem with Time Windows): Allow each customer to specify a delivery time window (e.g., 9 AM–10 AM).

Capacity Constraints: Model vehicle capacity (number of orders, weight/volume) and generate multiple routes/trips if capacity is exceeded.

Live Traffic & Road Networks: Replace static Haversine distances with real road network distances and traffic data (via Google Maps API, OpenRouteService, OSRM).

Multiple Vehicles & Depots: Optimize across multiple delivery vehicles and depots, enabling real-world fleet planning.

### 📄 License

This project is released under the MIT License — feel free to use, modify, and distribute it accordingly.

### 🧑‍💻 Author

Bramhendra C
🔗 GitHub Profile

Thanks for checking out this project! Feel free to ⭐ the repo and provide feedback or contributions.

---











