
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import requests
import os
import time
from dotenv import load_dotenv

from service.twitch_service import (
    get_streamer,
    get_twitch_stream,
    search_streamers,
    get_streamer_videos
)

from service.user_service import (
    get_users, get_user, create_user, update_user, delete_user,
    add_rating, get_ratings, delete_rating,
    create_playlist, get_playlists, add_video, delete_playlist
)


load_dotenv()

twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
twitch_client_secret = os.getenv("TWITCH_CLIENT_SECRET")

access_token = None
token_expiration = 0

app = FastAPI()


class UserCreate(BaseModel):
    username: str
    age: int = Field(..., ge=0, le=120)


class RatingCreate(BaseModel):
    streamer_id: str
    rating: str


class PlaylistCreate(BaseModel):
    name: str


class VideoCreate(BaseModel):
    video_id: str

#TOKEN

def get_twitch_token():

    global access_token, token_expiration

    if access_token and time.time() < token_expiration:
        return access_token

    url = "https://id.twitch.tv/oauth2/token"

    response = requests.post(
        url,
        data={
            "client_id": twitch_client_id,
            "client_secret": twitch_client_secret,
            "grant_type": "client_credentials",
        },
    )

    response.raise_for_status()

    token_data = response.json()

    access_token = token_data["access_token"]
    token_expiration = time.time() + token_data["expires_in"] - 60

    return access_token


# TWITCH

@app.get("/streamers/{login}")
def get_streamer_info(login: str):
    token = get_twitch_token()
    return get_streamer(login, twitch_client_id, token)


@app.get("/streams/{username}")
def get_stream_info(username: str):
    token = get_twitch_token()
    return get_twitch_stream(username, twitch_client_id, token)


@app.get("/streamers/search/{query}")
def search_streamers_info(query: str):
    token = get_twitch_token()
    return search_streamers(query, twitch_client_id, token)


@app.get("/videos/{user_id}")
def get_videos_info(user_id: str):
    token = get_twitch_token()
    return get_streamer_videos(user_id, twitch_client_id, token)


# USER MANAGEMENT

@app.get("/users")
def list_users():
    return get_users()


@app.get("/users/{user_id}")
def get_user_info(user_id: int):
    data = get_user(user_id)

    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    return data


@app.post("/users")
def post_user(user: UserCreate):
    new_user = create_user(user.username, user.age)

    return JSONResponse(
        content=new_user,
        status_code=201
    )


@app.put("/users/{user_id}")
def put_user(user_id: int, user: UserCreate):
    data = update_user(user_id, user.username, user.age)

    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    return JSONResponse(
        content=data,
        status_code=200
    )


@app.delete("/users/{user_id}")
def remove_user(user_id: int):
    data = delete_user(user_id)

    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    return JSONResponse(
        content=data,
        status_code=200
    )



# Preferencias de Usuario

@app.post("/users/{user_id}/ratings")
def post_rating(user_id: int, rating: RatingCreate):

    data = add_rating(user_id, rating.streamer_id, rating.rating)

    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"])

    return JSONResponse(content=data, status_code=201)


@app.get("/users/{user_id}/ratings")
def get_user_ratings(user_id: int):

    data = get_ratings(user_id)

    if isinstance(data, dict) and "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    return JSONResponse(content=data, status_code=200)


@app.delete("/users/{user_id}/ratings/{streamer_id}")
def remove_rating(user_id: int, streamer_id: str):

    data = delete_rating(user_id, streamer_id)

    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    return JSONResponse(content=data, status_code=200)




# Listas de reproducción

@app.post("/users/{user_id}/playlists")
def post_playlist(user_id: int, playlist: PlaylistCreate):
    data = create_playlist(user_id, playlist.name)

    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    return JSONResponse(content=data, status_code=201)


@app.get("/users/{user_id}/playlists")
def get_user_playlists(user_id: int):
    data = get_playlists(user_id)

    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    return JSONResponse(content=data, status_code=200)


@app.post("/users/{user_id}/playlists/{playlist_id}/videos")
def post_playlist_video(user_id: int, playlist_id: int, video: VideoCreate):
    data = add_video(user_id, playlist_id, video.video_id)

    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"])

    return JSONResponse(content=data, status_code=201)


@app.delete("/users/{user_id}/playlists/{playlist_id}")
def remove_playlist(user_id: int, playlist_id: int):
    data = delete_playlist(user_id, playlist_id)

    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    return JSONResponse(content=data, status_code=200)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
