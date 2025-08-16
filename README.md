# TravelAgent CrewAI

A multi-agent system built using **CrewAI** for simulating the role of a smart travel assistant.  
The project combines autonomous agents to plan, organize, and provide personalized travel recommendations.

---

## Project Overview
The aim of this project is to demonstrate the use of **agent-based AI systems** in a real-world scenario.  
Here, agents collaborate to assist a user in:
- Searching and suggesting destinations
- Estimating budgets
- Managing travel bookings
- Providing itineraries and travel advice

This system shows how **autonomous collaboration between agents** can achieve a practical outcome without relying on a single monolithic model.

---

## Project Structure
TravelAgent/
│── agents/           # Different agents (planner, budget, booking, etc.)
│── utils/            # Utility functions/helpers
│── main.py           # Entry point to run the system
│── requirements.txt  # Dependencies
│── README.md         # Documentation

- **agents/** → Contains all CrewAI agent definitions (Planner, Budget Analyst, Booking Manager, etc.)  
- **utils/** → Helper methods for logging, prompts, or formatting.  
- **main.py** → Runs the complete multi-agent pipeline.  
- **requirements.txt** → Python dependencies for environment setup.  

---

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/varun-beep/TravelAgent-CrewAI-.git
   cd TravelAgent-CrewAI-

python -m venv venv
source venv/bin/activate     # For Mac/Linux

pip install -r requirements.txt

python main.py




 Features:
	•	Travel Planner Agent – Suggests destinations based on preferences.
	•	Budget Analyst Agent – Provides cost estimates and travel feasibility.
	•	Booking Agent – Handles accommodation, flights, and itinerary creation.
	•	Collaboration – Agents communicate to deliver final travel plans.


Use Cases:
	•	Personalized travel recommendations
	•	Budget-based planning for individuals/groups
	•	Simulated booking experience for research/academic purposes
	•	Demonstration of CrewAI for multi-agent coordination

Future Improvements:
	•	Integration with real-world APIs (Skyscanner, Booking.com, etc.)
	•	A user-facing web interface for interactive travel planning
	•	Smarter decision-making with memory persistence



	•	Varun Araballi (@varun-beep)
MSc in AI & ML | Passionate about AI, ML, and real-world applications.



