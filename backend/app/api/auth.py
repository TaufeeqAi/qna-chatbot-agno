from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from httpx_oauth.google import GoogleOAuth2
from ..db import crud, schemas
from ..core.secuirty import create_access_token
from ..db.session import SessionLocal
from app.core.secuirty import create_access_token, verify_access_token, oauth2_scheme
from app.core.config import get_settings


settings = get_settings()

google_oauth_client = GoogleOAuth2(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
)

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.user.get_user_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = crud.user.create_user(db, email=user_in.email, password=user_in.password)
    return user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.user.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def read_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    user_id: int = int(payload.get("sub")) # Make sure sub is an int
    user = crud.user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/google")
async def google_auth(request: Request):
    redirect_uri = request.url_for("google_auth_callback")
    return await google_oauth_client.get_authorization_url(
        redirect_uri,
        scope=["email", "profile"],
        extras_params={"access_type": "offline"},
    )

@router.get("/google/callback")
async def google_auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await google_oauth_client.get_access_token(
            request.query_params["code"],
            redirect_uri=str(request.url_for("google_auth_callback")),
        )
        user_data = await google_oauth_client.get_id_email(token["access_token"])
        email = user_data["email"]
        
        user = crud.user.get_user_by_email(db, email=email)
        if not user:
            user = crud.user.create_user(db, email=email, oauth_provider="google", oauth_account_id=user_data.get("id"))
        elif not user.oauth_provider: # User exists but not linked to OAuth
            user = crud.user.update_user_oauth(db, user_id=user.id, oauth_provider="google", oauth_account_id=user_data.get("id"))

        access_token = create_access_token({"sub": str(user.id)})
        # Redirect to frontend with token (example)
        # This needs to be configured to your frontend's callback handling URL
        frontend_url = f"http://localhost:8501/callback?token={access_token}" 
        return RedirectResponse(url=frontend_url)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during Google OAuth callback: {e}",
        )