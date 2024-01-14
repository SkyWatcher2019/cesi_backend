import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel
from starlette.middleware.cors import CORSMiddleware

from db.db import engine
from routes.products import router as products_router
from routes.reports import router as reports_router
from routes.sections import router as sections_router
from routes.sells import router as sells_router

app = FastAPI(title='Продмаг')

app.include_router(products_router, tags=['Продукты'])
app.include_router(sections_router, tags=['Отделы'])
app.include_router(sells_router, tags=['Продажи'])
app.include_router(reports_router, tags=['Отчеты'])

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )

if __name__ == '__main__':
    SQLModel.metadata.create_all(engine)
    uvicorn.run(app, host='0.0.0.0', port=8000)
