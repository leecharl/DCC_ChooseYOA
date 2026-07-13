# Local Setup

## 1. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Run migrations

```bash
python manage.py migrate
```

## 3. Seed the starter adventure ("Level 1: The Collapse")

```bash
python manage.py seed_db
```

This is idempotent — running it again will skip re-creating nodes if the adventure is already seeded.

## 4. Create an admin/superuser account

```bash
python manage.py createsuperuser
```

Follow the prompts for username/email/password. Log in at `/admin/` to manage Items, Adventures, Nodes, Options, and Runs.

## 5. Start the dev server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to register a player account and play, or `http://127.0.0.1:8000/admin/` to manage content.

## Notes

- `media/` (uploaded/seeded images) and `db.sqlite3` are gitignored — they're generated locally by the steps above.
- The seed command pulls its source images from `engine/seed_assets/`, which *is* committed to the repo.
