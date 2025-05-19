from fastapi import FastAPI
from src.asset_manager.agencies import router as agencies_router
from src.asset_manager.assets import router as asset_router
from src.asset_manager.projects import router as projects_router

app = FastAPI()
app.include_router(agencies_router,
                   prefix = '/agency')
app.include_router(asset_router,
                   prefix = '/asset')

app.include_router(projects_router,
                   prefix = '/project')

@app.get('/')
async def root():
    return {'msg' : 'Initial endpoint'}