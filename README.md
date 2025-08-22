Spontaneous Outing Planner ✨
An intelligent agent that transforms a simple "vibe" into a creative, two-stop itinerary using the Gemini and Foursquare APIs.

(Website Link- )

📍 About The Project
The Spontaneous Outing Planner was designed to eliminate the friction and indecision inherent in planning everyday outings. Many of us face the "what should we do?" dilemma, which often leads to wasted time and missed opportunities. This intelligent agent tackles that problem head-on by transforming a simple, conversational input—a "vibe"—into a concrete, creative, and actionable two-stop plan.

The goal is to provide users with a delightful, frictionless way to discover new places and enjoy their free time, whether in their hometown or a new city.

Key Features:
Vibe Interpretation: Simply describe the mood of your desired outing (e.g., "a relaxing afternoon," "an exciting date night"), and the AI will suggest two fitting activities.

Intelligent Location Search: Using the Foursquare API, the agent finds the best real-world venues for your plan. It uses a "popularity-weighted" algorithm to recommend places that are not just highly-rated but also well-loved, and resiliently expands its search radius to ensure it always finds a great spot.

Creative Itinerary Generation: Go beyond a simple list of addresses. The app uses the Gemini API to generate a full, engaging narrative for your outing, complete with suggestions for what to do at each location.

Interactive 3D UI: A visually stunning and intuitive interface featuring an animated 3D globe built with Three.js.

🚀 How It Works
The application is a single-page web app built on a modern, agentic architecture that intelligently combines multiple APIs to deliver a seamless user experience.

Vibe Interpretation (Gemini API): When a user enters a "vibe" and a location, the app first calls Google's Gemini API. The AI model interprets the abstract concept and translates it into two concrete, searchable activity categories (e.g., "Bookstore, Cafe").

Location Search (Foursquare API): Armed with these categories, the agent queries the Foursquare Places API to find real-world venues. It employs a sophisticated algorithm to find popular and highly-rated locations.

Creative Itinerary Generation (Gemini API): Once the two locations are finalized, a second call to the Gemini API crafts a compelling narrative for the outing, adding a layer of creative flair that a simple data lookup could never achieve.

Built With:
Frontend: HTML, Tailwind CSS, Three.js

Core Logic: Vanilla JavaScript

APIs: Google Gemini API, Foursquare Places API

🔮 Future Development
This project serves as a robust foundation for a much larger platform. Future plans include:

Full Foursquare API Integration: Replace the current mock API data with live, real-time calls.

User Accounts & Personalization: Introduce user accounts to save plans and tailor suggestions.

Multi-Stop & Group Planning: Evolve the agent to handle more complex requests.

Booking & Reservation Integration: Partner with booking platforms to allow users to make reservations or buy tickets directly.

Native Mobile App: Develop dedicated iOS and Android applications.

🏁 Getting Started
This is a self-contained, single-file application. To run it locally:

Clone the repository:

git clone https://github.com/your-username/spontaneous-outing-planner.git

Open the index.html file in your favorite web browser.

📄 License
Distributed under the MIT License. See LICENSE for more information.
