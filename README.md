# Wanderlust

Travel inspiration platform that includes a user-friendly website for exploring travel destinations and a RESTful API for accessing travel data programmatically.

<img src="extras/banner_repo.png" alt="Wanderlust Banner" width="800">

## About

Wanderlust is a comprehensive Travel Destination Platform that combines a user-friendly website and a powerful RESTful API. The website offers an interactive user-friendly interface where you can discover travel destinations, view detailed city information, check real-time weather updates, and book flight tickets. Simultaneously, the RESTful API empowers developers to programmatically access data, enabling them to retrieve, create, update, and delete destinations.

## Demo

[Explore Wanderlust Website](https://wanderlust-v4k4.onrender.com/) <br>
[Explore Wanderlust API Docs](https://wanderlust-v4k4.onrender.com/api/docs/) <br><br>
**<ins>QUICK NOTES:</ins> <br>Even tho the passwords are hashed and salted i recommend you to avoid using your personal informations when you sign up.<br>It may take up to one minute for the demo to start.**

*Hosted by [Render](https://render.com/)*

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
- **API Integration:** VisualCrossing API for weather forecasting, Dev.me API for countries FAQ and Flags, Tequila by Kiwi.com for flight ticket booking.
- **API Docs:** Swagger UI.

---
# Wanderlust API

## Authorization

All API requests require the use of a generated API key. You can find your API key, or generate a new one, in your profile tab after registering to Wanderlust.
To authenticate an API request, you should provide your API key in the `Authorization` header.

| Headers | Parameter | Description |
| :--- | :--- | :--- |
| `Authorization` | `api_key` | **Required**. Your Wanderlust API key |


## Request methods

| Method   | Description                                                              |
| -------- | ------------------------------------------------------------------------ |
| `GET`    | Used to retrieve a single item or a collection of items.                 |
| `POST`   | Used when creating new items e.g. a new user, post, comment etc.         |
| `PATCH`  | Used to update one or more fields on an item e.g. update e-mail of user. |
| `DELETE` | Used to delete an item.                                                  |

## Endpoints

| Method   | URL                                        | Description                                |  Parameters Required/Additional                     | 
| -------- | ------------------------------------------ | ------------------------------------------ |  ------------------------------------------ |
| `GET`    | `/api/random`                              | Retrieve a random destination.             |  - / -                                                               |
| `Get`    | `/api/all`                                 | Retrieve all destination.                  |  - / -                                                           |
| `GET`    | `/api/recent`                              | Retrieve recent added destinations.        |  - / -                                                           |
| `Get`    | `/api/search`                              | Retrieve searched destinations.            |  - /  `country`, `city`, `description`, `budget`, `eating_out`, `sightseeing`, `activities`, `shopping`, `nightlife`, `museums`, `kid_friendly`, `beaches`, `skiing`, `diving`, `camping`, `hiking`, `cycling`, `sailing`, `romantic`, `photography`, `popular_attractions`, `picture`|
| `POST`   | `/api/add_destination`                     | Add new destination.                       |  `continent` `country` `city` `description` `popular_attractions` / `budget`, `eating_out`, `sightseeing`, `activities`, `shopping`, `nightlife`, `museums`, `kid_friendly`, `beaches`, `skiing`, `diving`, `camping`, `hiking`, `cycling`, `sailing`, `romantic`, `photography`, `picture`|
| `PATCH`  | `/api/update_destination/{destination_id}` | Update destination at #destination_id.     |  `destination_id` / `continent`, `country`, `city`, `description`, `popular_attractions`, `budget`, `eating_out`, `sightseeing`, `activities`, `shopping`, `nightlife`, `museums`, `kid_friendly`, `beaches`, `skiing`, `diving`, `camping`, `hiking`, `cycling`, `sailing`, `romantic`, `photography`, `picture`|
| `DELETE` | `/api/delete_destination/{destination_id}` | Delete destination #destination_id.        |  `destination_id` / -                                               |
| `GET`    | `/api/get_weather`                         | Retrieve 7-day forecast for a destination. |  `city` / -                                            |


## HTTP Response Status Codes

| Code  | Title                     | Description                              |
| ----- | ------------------------- | ---------------------------------------- |
| `200` | `OK`                      | Successful request. |
| `201` | `Created`                 | Successfully created a new resource. |
| `204` | `No Content`              | Successfully processed request with no content to return. |
| `400` | `Bad Request`             | Invalid request or request parameters. |
| `401` | `Unauthorized`            | Unauthorized access. |
| `404` | `Not Found`               | Resource not found. |
| `500` | `Internal Server Error`   | Internal server error. |

---
## Credits

- **Data:** The ratings for each city were gathered from earthroulette.com, a valuable resource for travel information.
- **Theme:** Created by templatemo and modified by me to fit this project.
<br>

*This project is open-source, and contributions are welcome. Feel free to fork the repository and submit your pull requests.*

---
