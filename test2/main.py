from fastapi import FastAPI
from middlewares import SearchValidationMiddleware
from routers import search_router, upload_router
# from moviepy.config import get_setting, change_settings
# import subprocess

app = FastAPI()

# print(get_setting("FFMPEG_BINARY"))
# change_settings({"FFMPEG_BINARY": "/opt/homebrew/bin/ffmpeg"})
# print(get_setting("FFMPEG_BINARY"))
# print(subprocess.run(["whereis", "ffmpeg"], capture_output=True).stdout.decode())

app.add_middleware(SearchValidationMiddleware)

app.include_router(upload_router.router)
app.include_router(search_router.router)

@app.get("/")
async def root():
    return {"Hello": "World"}
