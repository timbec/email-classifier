from fastapi import FastAPI
from app.routes.email_routes import email_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the email classifier API!"}

app.include_router(email_router, prefix="/emails", tags=["emails"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
