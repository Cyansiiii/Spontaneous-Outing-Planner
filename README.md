# Here are your Instructions
Spontaneous Outing Planner
Overview
The Spontaneous Outing Planner is a web application designed to transform abstract "vibes" into concrete, actionable two-stop outing plans. By leveraging AI and real-world venue data, the app generates creative itineraries with detailed narratives, tailored to user inputs for vibe and location. The result is a seamless, engaging, and personalized outing experience with a modern, polished interface.
Features

Beautiful UI: Modern, geometric design with clean typography and responsive layouts, matching provided mockups.
AI-Powered Itinerary Generation: Integrates Google Gemini API (gemini-1.5-flash) to interpret vibes and generate creative two-stop plans.
Real Venue Discovery: Uses Foursquare Places API for popularity-weighted venue selection, ensuring relevant and high-quality recommendations.
Real-Time Thought Process: Displays the AI's reasoning steps with animated updates during itinerary creation.
Two-Stop Plans: Intelligently pairs activities (e.g., Museum + Cafe, River Cruise + Bistro) based on vibe input.
Creative Narratives: Generates detailed, atmospheric itineraries with timing and storytelling elements.
User-Friendly Input: Intuitive form for entering vibe and location preferences.
One-Click Generation: Produces complete itineraries with venue details (ratings, addresses) in a single click.

Website Link -https://spontaneous-outing-planner.netlify.app/

Technical Stack

Frontend: React with modern CSS and a clean component architecture.
Backend: FastAPI with MongoDB for efficient data persistence.
APIs:
Google Gemini AI (gemini-1.5-flash) for vibe interpretation and itinerary creation.
Foursquare Places API for real-time venue discovery.


Processing: Real-time async processing with robust error handling.

How It Works

Input Vibe and Location: Users provide a desired vibe (e.g., "cozy cultural afternoon" or "romantic evening out") and a location.
AI Reasoning: The app processes the input using Google Gemini AI, displaying real-time reasoning steps in an animated "My Thought Process" section.
Venue Selection: The Foursquare API fetches relevant venues, weighted by popularity, to create a two-stop plan (e.g., a museum followed by a cozy cafe).
Itinerary Generation: The app generates a detailed narrative with timing, atmosphere, and venue details (ratings, addresses) for a complete outing plan.
Output: Users receive two venue cards and a creative itinerary, ready to inspire their next adventure.

Testing and Validation
The app has been thoroughly tested with the following results:

Successfully handled multiple vibe inputs (e.g., "cozy cultural afternoon", "romantic evening out").
Confirmed proper integration with Google Gemini and Foursquare APIs.
Verified end-to-end flow from vibe input to final itinerary.
Demonstrated intelligent venue pairing (e.g., Museum + Cafe, River Cruise + Bistro).
Validated creative narrative generation with accurate timing and atmosphere details.

Getting Started
Prerequisites

Node.js (for React frontend)
Python 3.8+ (for FastAPI backend)
MongoDB (for data persistence)
API keys for:
Google Gemini API
Foursquare Places API



Installation

Clone the Repository:
git clone https://github.com/Cyansiiii/Spontaneous-Outing-Planner.git
cd Spontaneous-Outing-Planner


Frontend Setup:
cd frontend
npm install
npm start


Backend Setup:
cd backend
pip install -r requirements.txt
uvicorn main:app --reload


Environment Variables:Create a .env file in the backend directory with the following:
GEMINI_API_KEY=your_gemini_api_key
FOURSQUARE_API_KEY=your_foursquare_api_key
MONGODB_URI=your_mongodb_connection_string


Run the App:

Start the backend server (uvicorn main:app --reload).
Launch the frontend (npm start).
Access the app at http://localhost:3000.



Usage

Open the app in your browser.
Enter a vibe (e.g., "cozy cultural afternoon") and a location (e.g., "New York, NY").
Click "Generate Itinerary" to see the AI's thought process and receive a two-stop plan with venue details and a narrative.
Explore the venue cards and itinerary to plan your outing!

Contributing
Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes. Ensure your code follows the project's style guidelines and includes appropriate tests.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or feedback, reach out via GitHub Issues or contact the maintainer at [anantanandam8340@gmail.com].
