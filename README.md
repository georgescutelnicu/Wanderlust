# Wanderlust

Travel inspiration platform that includes a user-friendly website for exploring travel destinations and a RESTful API for accessing travel data programmatically.

<img src="extras/banner_repo.png" alt="Wanderlust Banner" width="750">

## About

Wanderlust is a comprehensive Travel Destination Platform that combines a user-friendly website and a powerful RESTful API. The website offers an interactive user-friendly interface where you can discover travel destinations, view detailed city information, check real-time weather updates, and book flight tickets. Simultaneously, the RESTful API empowers developers to programmatically access data, enabling them to retrieve, create, update, and delete destinations.

## Demo

[Explore Wanderlust Website](https://wanderlust-v4k4.onrender.com/) <br>
[Explore Wanderlust API Docs](https://wanderlust-v4k4.onrender.com/api/docs/) <br><br>
**<ins>QUICK NOTES:</ins> <br>Even tho the passwords are hashed and salted i recommend you to avoid using your personal informations when you sign up.<br>It may take up to one minute for the demo to start.**

## Features

### Wanderlust Website

- **Random Destination Discovery:** Experience the thrill of spontaneity by exploring random travel destinations.
- **In-Depth City Insights:** Discover cities with comprehensive pages showcasing popular attractions, ratings, and valuable insights.
- **Tailored Travel Planning:** Explore the world's most visited destinations or narrow down your choices by continent for focused travel planning.
- **Real-Time Weather Forecast:** Stay prepared with 7-day weather forecasting for each city on your itinerary.
- **Flight Ticket Booking:** Book your flight tickets with our integrated booking widget.
- **Intuitive User Interface:** Enjoy a user-friendly and elegant interface for effortless navigation and travel inspiration.
- **User Account Features:** Sign up and log in to save places to your "visited" or "plan to visit" lists, making your travel planning more accessible.
- **Interactive Map:** Visualize your travel journey with an interactive map, giving you a geographical overview of your adventures.
- **Achievements Tracker:** Track your travel achievements and earn badges.

### Wanderlust API

- **Effortless Data Retrieval:** Retrieve destination data, including ratings, descriptions, and more.
- **Advanced Search and Filtering:** Advanced search and filtering capabilities to find destinations that match specific criteria.
- **Dynamic Data Updates:** Add new destinations to expand the travel content or update existing details to keep the information fresh.
- **Secure Data Deletion:** Maintain data integrity by securely deleting destinations as needed.
- **Clear Documentation:** Simplify development with clear and comprehensive API documentation using Swagger UI.
- **Error Handling and Validation:** Ensure data integrity and reliability with robust error handling and input validation.
- **API Key Integration:** Sign up to generate a secure and unique API key, allowing you to access the Wanderlust API.

## Technologies

- **Front-End Development:** HTML, CSS, JS, Bootstrap.
- **Back-End Development:** Flask (flask_sqlalchemy, flask_login, flask_swagger_ui, flask_paginate, werkzeug.security, etc.), PostgreSQL + SQLAlchemy.
- **Visualization:** Plotly for interactive choropleth maps.
- **API Integration:** VisualCrossing API for weather forecasting, Tequila by Kiwi.com for flight ticket booking.
- **API Docs:** Swagger UI.

---
## API Structure

### 1. Get a Random Destination

- **Endpoint:** `/api/random`
- **Method:** `GET`
- **Parameters:**
  - `api_key` (required)
 
### 2. Get All Destinations

- **Endpoint:** `/api/all`
- **Method:** `GET`
- **Parameters:**
  - `api_key` (required)

### 3. Get Recent Destinations

- **Endpoint:** `/api/recent`
- **Method:** `GET`
- **Parameters:**
  - `api_key` (required)

### 4. Search for Destinations

- **Endpoint:** `/api/search`
- **Method:** `GET`
- **Parameters:**
  - `api_key` (required)
  - Additional filters:
    - `continent`
    - `country`
    - `city`
    - `description`
    - `budget`
    - `eating_out`
    - `sightseeing`
    - `activities`
    - `shopping`
    - `nightlife`
    - `museums`
    - `kid_friendly`
    - `beaches`
    - `skiing`
    - `diving`
    - `camping`
    - `hiking`
    - `cycling`
    - `sailing`
    - `romantic`
    - `photography`
    - `popular_attractions`
    - `picture`

### 5. Add a New Destination

- **Endpoint:** `/api/add_destination`
- **Method:** `POST`
- **Parameters:**
  - `api_key` (required)
  - `continent` (required)
  - `country` (required)
  - `city` (required)
  - `description` (required)
  - `popular_attractions` (required)
  - Additional parameters:
    - `budget`
    - `eating_out` 
    - `sightseeing` 
    - `activities`
    - `shopping` 
    - `nightlife`
    - `museums` 
    - `kid_friendly`
    - `beaches`
    - `skiing` 
    - `diving`
    - `camping`
    - `hiking`
    - `cycling` 
    - `sailing`
    - `romantic` 
    - `photography` 
    - `picture`

### 6. Update a Destination

- **Endpoint:** `/api/update_destination/{destination_id}`
- **Method:** `PATCH`
- **Parameters:**
  - `api_key` (required)
  - `destination_id` (required)
  - Additional parameters:
    - `continent`
    - `country`
    - `city` 
    - `description` 
    - `popular_attractions` 
    - `budget` 
    - `eating_out` 
    - `sightseeing`
    - `activities` 
    - `shopping` 
    - `nightlife`
    - `museums` 
    - `kid_friendly` 
    - `beaches` 
    - `skiing` 
    - `diving` 
    - `camping`
    - `hiking` 
    - `cycling` 
    - `sailing` 
    - `romantic`
    - `photography` 
    - `picture`

### 7. Delete a Destination

- **Endpoint:** `/api/delete_destination/{destination_id}`
- **Method:** `DELETE`
- **Parameters:**
  - `api_key` (required)
  - `destination_id` (required)

### 8. Get Weather for a Destination

- **Endpoint:** `/api/get_weather`
- **Method:** `GET`
- **Parameters:**
  - `api_key` (required)
  - `city` (required)

---
## Credits

- **Data:** Most of the data was gathered from earthroulette.com, a valuable resource for travel information.
- **Theme:** Created by templatemo and modified by me to fit this project.
<br>

*This project is open-source, and contributions are welcome. Feel free to fork the repository and submit your pull requests.*

---
