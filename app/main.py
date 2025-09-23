from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import secrets
from datetime import timedelta
from contextlib import asynccontextmanager

from app import models, schemas, security
from app.config import settings
from app.database import engine, get_db, Base


# --- Lifespan Event Handler ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to handle startup and shutdown events.
    Creates database tables on application startup.
    """
    print("Application startup: Creating database tables...")
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # in production use Alembic migrations
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("Application shutdown.")

app = FastAPI(
    title="Chote",
    description="A modern, high-performance URL shortener API.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url=settings.DOMAIN_URL+"docs")

@app.post("/register", response_model=schemas.UserInfo, status_code=status.HTTP_201_CREATED, tags=['Authentication'])
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user. Hashes the password and saves the user to the database.
    """
    q = select(models.User).where(models.User.email==user.email)
    res = await db.execute(q)
    db_user = res.scalar_one_or_none()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashedpassword = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, password=hashedpassword, is_active=True)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.post("/token", response_model=schemas.Token, tags=["Authentication"]) # to authorize from /docs page
@app.post("/login", response_model=schemas.Token, tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    Logs in a user by verifying their credentials and returns a JWT access token.
    """
    q = select(models.User).where(models.User.email==form_data.username)
    res = await db.execute(q)
    db_user = res.scalar_one_or_none()

    if not db_user or not security.verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username or Password")
    
    access_token = security.create_access_token({'sub': db_user.email})
    return {"access_token":access_token, "token_type":"bearer"}

@app.post('/shorten', response_model=schemas.URLInfo, status_code=status.HTTP_201_CREATED, tags=["URL Shortener"])
async def get_short_url(url: schemas.URLCreate, db: AsyncSession = Depends(get_db), user: models.User = Depends(security.get_current_user)):
    """
    Create a new short URL. This is a protected endpoint that requires authentication.
    """
    while True:
        short_code = secrets.token_urlsafe(7)
        q = select(models.URL).where(models.URL.short_code==short_code)
        res = await db.execute(q)
        if not res.scalar_one_or_none():
            break
    
    db_url = models.URL(
        long_url = url.long_url,
        short_code = short_code,
        owner_id=user.id
    )
    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)
    return {"long_url": url.long_url,"short_code": short_code, "short_url": settings.DOMAIN_URL+short_code, "owner_id": user.id}
    # return db_url

@app.get('/{short_code}', tags=["URL Shortener"])
@app.get('/{short_code}/', tags=["URL Shortener"])
async def redirect_to_url(short_code: str, db: AsyncSession = Depends(get_db)):
    """
    Redirects a short URL to its original long URL. This is a public endpoint.
    (Note: Caching can be added for better performance)
    """
    q = select(models.URL).where(models.URL.short_code==short_code)
    res = await db.execute(q)
    db_url = res.scalar_one_or_none()
    if not db_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    return RedirectResponse(url=db_url.long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
