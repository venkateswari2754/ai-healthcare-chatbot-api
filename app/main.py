from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta

from app.database import get_db, Base, engine
from app import models
from app.auth import (
    create_user,
    verify_password, 
    create_access_token, 
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.schemas import (
    UserRegister, 
    UserLogin, 
    Token, 
    UserResponse,
    ChatMessage,
    ChatResponse,
    ChatHistoryResponse,
    ChatLogItem,
)
from app.intent import classify_intent, Intents
from app.handlers import (
    handle_order_status,
    handle_payment_invoice,
    handle_warranty_amc,
    handle_scheduling,
    handle_complaint,
    handle_default,
)

# Create tables if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="HealthcareSense Support Chatbot API")

# ADD CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",   # Default Angular port
        "http://localhost:61957",  # Current Angular port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/db-health")
def db_health_check(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1"))
        rows = list(result)
        return {"status": "ok", "db_result": [tuple(r) for r in rows]}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.post("/register", response_model=Token)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    user = create_user(db=db, user_data=user_data)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/login", response_model=Token)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get user's primary client info
    user_client = db.query(models.UserClient).filter(
        models.UserClient.user_id == current_user.id,
        models.UserClient.is_primary == 1
    ).first()
    
    client_name = None
    client_code = None
    if user_client:
        client = db.query(models.Client).filter(models.Client.id == user_client.client_id).first()
        if client:
            client_name = client.name
            client_code = client.client_code
    
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at,
        client_name=client_name,
        client_code=client_code
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(
    message: ChatMessage,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get user's primary client
    user_client = db.query(models.UserClient).filter(
        models.UserClient.user_id == current_user.id,
        models.UserClient.is_primary == 1
    ).first()

    if not user_client:
        raise HTTPException(status_code=400, detail="User not linked to any client")

    # Classify intent
    intent = await classify_intent(message.message)

    # Route to handler
    try:
        if intent == Intents.ORDER_STATUS:
            ai_response, source = handle_order_status(db, user_client.client_id, message.message)
        elif intent == Intents.PAYMENT_INVOICE:
            ai_response, source = handle_payment_invoice(db, user_client.client_id, message.message)
        elif intent == Intents.WARRANTY_AMC:
            ai_response, source = handle_warranty_amc(db, user_client.client_id, message.message)
        elif intent == Intents.SCHEDULING:
            ai_response, source = handle_scheduling(db, user_client.client_id, message.message)
        elif intent == Intents.COMPLAINT:
            ai_response, source = handle_complaint(db, current_user.id, user_client.client_id, message.message)
        else:
            ai_response, source = handle_default(db, user_client.client_id, message.message)
    except Exception as e:
        ai_response, source = ("Sorry, I hit an error while fetching data.", "none")

    # Log the conversation
    chat_log = models.ChatLog(
        user_id=current_user.id,
        client_id=user_client.client_id,
        user_message=message.message,
        ai_response=ai_response,
        intent=intent.value,
        data_source=source,
    )
    db.add(chat_log)
    db.commit()

    return ChatResponse(
        response=ai_response,
        intent=intent.value,
        data_source=source,
    )


@app.get("/chat/history", response_model=ChatHistoryResponse)
def chat_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_client = db.query(models.UserClient).filter(
        models.UserClient.user_id == current_user.id,
        models.UserClient.is_primary == 1
    ).first()

    if not user_client:
        raise HTTPException(status_code=400, detail="User not linked to any client")

    logs = (
        db.query(models.ChatLog)
        .filter(models.ChatLog.user_id == current_user.id, models.ChatLog.client_id == user_client.client_id)
        .order_by(models.ChatLog.timestamp.desc())
        .limit(50)
        .all()
    )

    items = [
        ChatLogItem(
            id=l.id,
            timestamp=l.timestamp,
            user_message=l.user_message,
            ai_response=l.ai_response,
            intent=l.intent,
            data_source=l.data_source,
        )
        for l in logs
    ]
    return {"items": items}