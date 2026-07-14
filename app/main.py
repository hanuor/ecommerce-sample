from fastapi import FastAPI

app = FastAPI(
    title="Ecommerce Store",
    version="1.0.0"
)

@app.get("/")
def health():
    return {"status": "healthy"}