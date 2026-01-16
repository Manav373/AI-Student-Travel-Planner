<div align="center">

# ✈️ AI-Powered Student Travel Planner

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Groq AI](https://img.shields.io/badge/Powered%20By-Groq%20Llama%203-orange?style=for-the-badge)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

*An intelligent, AI-driven travel planning application designed to create personalized itineraries, manage budgets, and visualize routes.*

[Features](#-key-features) • [Tech Stack](#-%EF%B8%8F-tech-stack) • [Getting Started](#-getting-started) • [Contribution](#-contribution)

</div>

---

## ✨ Key Features

### 🧠 **Intelligent Itinerary Generation**
> Experience travel planning like never before with our advanced AI engine.
-   **Hyper-Personalized**: Tailored day-by-day plans based on your interests (Culture, Food, Adventure, etc.).
-   **Smart Scheduling**: optimization of Morning, Afternoon, and Evening slots.
-   **Hidden Gems**: Discover local secrets alongside main attractions.

### 💰 **Smart Budget Management**
> Maximize every dollar with Zero-Based Budgeting.
-   **Auto-Splitter**: Automatically allocates funds for Accommodation, Food, Transport, and Activities.
-   **Real-time FX**: Live currency conversion for accurate international planning.
-   **Viability Guard**: AI warnings if your budget is too tight for the destination.

### 🌍 **Interactive Visualization**
> See your trip come to life.
-   **Dynamic Mapping**: Interactive Folium maps with route plotting.
-   **Glassmorphism UI**: A stunning, modern interface designed for students.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white) | Interactive web interface |
| **AI Engine** | ![Llama-3](https://img.shields.io/badge/-Llama--3%2070B-blue?style=flat) | Powered by **Groq** for instant inference |
| **Mapping** | ![Folium](https://img.shields.io/badge/-Folium-77DD77?style=flat) | OpenStreetMap based interactive maps |
| **Data** | ![Pandas](https://img.shields.io/badge/-Pandas-150458?style=flat&logo=pandas&logoColor=white) | Data manipulation & budget algorithms |

---

## 🚀 Getting Started

Follow these simple steps to launch your planner.

### Prerequisites
-   **Python 3.8+**
-   **Groq API Key** (Free at [console.groq.com](https://console.groq.com/))

### 📥 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Manav373/ai-student-travel-planner.git
    cd ai-student-travel-planner
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key**
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=gsk_your_api_key_here
    ```

4.  **Launch App**
    ```bash
    streamlit run app.py
    ```

---

## 📂 Project Structure

```text
ai-student-travel-planner/
├── src/
│   ├── ai.py              # 🧠 AI Logic & Prompts
│   ├── budget.py          # 💰 Budget Algorithms
│   ├── maps.py            # 🗺️ Map Generation
│   └── styles.css         # 🎨 Custom UI Styling
├── app.py                 # 🚀 Main Application
├── requirements.txt       # 📦 Dependencies
└── README.md              # 📄 Documentation
```

---

<div align="center">

Made with ❤️ by [Manav373](https://github.com/Manav373)

</div>