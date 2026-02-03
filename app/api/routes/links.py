from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from uuid import uuid4

from app.core.security import get_current_user
from app.db.session import get_db
from app.models import ShortLink, User
from app.schemas import LinkCreate, LinkOut

router = APIRouter()


@router.post("/shorten", response_model=LinkOut)
def shorten(
    link: LinkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rand_token = str(uuid4())
    new_link = ShortLink(
        key=rand_token,
        target_url=str(link.url),
        owner_id=current_user.id,
    )
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link


@router.get("/link")
def ref(key: str, db: Session = Depends(get_db)):
    link = db.query(ShortLink).filter(ShortLink.key == key).first()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found :(")
    return RedirectResponse(link.target_url)
