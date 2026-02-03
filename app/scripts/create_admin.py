import argparse

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models import User


def main() -> None:
    parser = argparse.ArgumentParser(description="Create admin user")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == args.email).first()
        if existing:
            raise SystemExit("User already exists")
        user = User(
            email=args.email,
            hashed_password=get_password_hash(args.password),
            role="admin",
        )
        db.add(user)
        db.commit()
        print("Admin user created")
    finally:
        db.close()


if __name__ == "__main__":
    main()
