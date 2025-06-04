# # 🔄 Alembic Migration Guide

This project uses **Alembic** for managing database schema migrations. Please follow the steps below to ensure smooth collaboration and database consistency.

---

## 📁 1. Environment Setup

Make sure your `.env` file includes the model folder path:

```env
MODELS_FOLDER=adapters/wrap_orm_adapters/models
```

## 🚀 2. Running Migrations After Pulling Code
Whenever you pull changes from the remote repository, run existing migrations to update your local database schema:

If using Poetry:

```Bash
poetry run alembic upgrade head
```

If using Docker:

```Bash
docker compose down && docker compose up --build -d
```
This ensures your database schema is in sync with the latest code.

## ✍️ 3. Creating a New Migration
If you've made changes to the SQLAlchemy model files (e.g., added/removed fields or tables):

Generate a new migration file:

```Bash
poetry run alembic revision --autogenerate -m "describe your change"
```
Review the generated migration script in migrations/versions/ to make sure it looks correct.

Test the migration locally or in your docker terminal:

```Bash
poetry run alembic upgrade head
```

**Make sure the migration applies successfully before pushing your code.**

## 🧠 Summary

| Action | Command | 
| -------- | -------- | 
| Run latest migrations (Poetry) | poetry run alembic upgrade head | 
| Run latest migrations (Docker | docker compose down && docker compose up --build -d | 
| Generate a new migration | poetry run alembic revision --autogenerate -m "your message" | 


## 🛑 Important Notes
* Always test migrations locally before pushing.
* Never generate migrations in production.
* Commit migration files with your PR when models change.