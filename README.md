# Recipe Recommendation API

The **Recipe Recommendation API** is a backend application for discovering, managing, and recommending recipes. It offers personalized recommendations, ingredient-based filtering, and advanced search capabilities to simplify recipe discovery and enhance user engagement.

---

## Features

- **User Management**:
  - Secure user registration and login with token-based authentication.
  - Save and manage favorite recipes.

- **Recipe Management**:
  - Create, view, update, and delete recipes.
  - Filter recipes by ingredients.
  - Search recipes by titles or keywords.

- **Personalized Recommendations**:
  - Suggest recipes based on user-provided ingredients.
  - Match recipes using ingredient similarity scoring.

- **Feedback and Ratings**:
  - Collect and display user feedback for recipes.
  - Highlight top-rated recipes.

---

## Tech Stack

- **Backend**: Django REST Framework
- **Authentication**: Token-based authentication (DRF Tokens)
- **Similarity Scoring**: RapidFuzz
- **Database**: SQLite (can be switched to PostgreSQL or MySQL)


## API Endpoints

| **Endpoint**                    | **Method** | **Description**                              |
|----------------------------------|------------|----------------------------------------------|
| `/register/`                    | POST       | Register a new user                          |
| `/login/`                       | POST       | Login and receive an auth token              |
| `/recipes/`                     | GET        | List all recipes                             |
| `/recipes/`                     | POST       | Create a new recipe                          |
| `/recipes/<id>/`                | GET        | Retrieve a recipe by ID                      |
| `/recipes/<id>/`                | PUT        | Update a recipe by ID                        |
| `/recipes/<id>/`                | DELETE     | Delete a recipe by ID                        |
| `/recipes/search/?q=<query>`    | GET        | Search recipes by title                      |
| `/recipes/filter/`              | GET        | Filter recipes by ingredients                |
| `/recommend/`                   | POST       | Recommend recipes by ingredients             |
| `/recipes/top/`                 | GET        | Get top-rated recipes                        |
| `/recipes/<id>/feedback/`       | POST       | Add feedback to a recipe                     |
| `/user/saved-recipes/`          | GET        | List user-saved recipes                      |
| `/user/saved-recipes/`          | POST       | Save a recipe for the user                   |





