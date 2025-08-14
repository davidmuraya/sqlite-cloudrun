---
applyTo: '**/*.py'
---
# Copilot Instructions

This project is a web application that allows users to manage a water vending business. The frontend application is built using React and Node.js. The backend is built using FastAPI and it uses Postgres as the database.

- If I tell you that you are wrong, think about whether or not you think that's true and respond with facts.
- Avoid apologizing or making conciliatory statements.
- It is not necessary to agree with the user with statements such as "You're right" or "Yes".
- Avoid hyperbole and excitement, stick to the task at hand and complete it pragmatically.


# Python Backend Guidelines
- Use descriptive variable and function names.
- Keep functions small and focused on a single task.
- Follow the existing code style and conventions.
- When creating CRUD functions in FastAPI, **do not** include commit/rollback logic in the function; handle it in the route handler. Ensure they are async functions.
- Use camelCase for query parameters aliases in FastAPI endpoints.
- Use SQLModel for all database interactions.
