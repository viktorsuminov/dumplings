# main.py
from fastapi import FastAPI
from routers import shops_router, dumplings_router, prices_router

app = FastAPI(
    title="Пельменный сайт",
    description="Сравнение цен на пельмени в разных магазинах",
    version="1.0.0"
)

app.include_router(shops_router)
app.include_router(dumplings_router)
app.include_router(prices_router)

@app.get("/")
async def root():
    return {"message": "Добро пожаловать на Пельменный сайт! 🥟"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}