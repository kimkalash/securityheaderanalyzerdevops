from sqlalchemy.orm import Session
from app.models import User, Scan, HeaderResult


def create_user(db: Session, username: str, email: str, password_hash: str) -> User:
    """Create a new user in the database."""
    new_user = User(username=username, email=email, password_hash=password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Fetch a user by their ID."""
    return db.query(User).filter(User.id == user_id).first()


def create_scan(db: Session, user_id: int, scan_url: str) -> Scan:
    """Create a new scan entry for a user."""
    new_scan = Scan(user_id=user_id, scan_url=scan_url)
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)
    return new_scan


def get_user_scans(db: Session, user_id: int) -> list[Scan]:
    """Get all scans for a specific user."""
    return db.query(Scan).filter(Scan.user_id == user_id).all()


def create_header_result(db: Session, scan_id: int, header_name: str, header_value: str) -> HeaderResult:
    """Add a header result to a specific scan."""
    new_header_result = HeaderResult(
        scan_id=scan_id, header_name=header_name, header_value=header_value
    )
    db.add(new_header_result)
    db.commit()
    db.refresh(new_header_result)
    return new_header_result
