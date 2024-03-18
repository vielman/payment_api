from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.pay import pay

app = FastAPI()

app.include_router(pay)

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

