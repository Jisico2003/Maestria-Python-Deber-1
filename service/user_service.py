import json

USERS_JSON = "users.json"


def get_users():
    with open(USERS_JSON, "r") as file:
        users = json.load(file)
    return users


def get_user(user_id: int):
    users = get_users()
    for user in users:
        if user["id"] == user_id:
            return user
    return {"error": "Usuario no encontrado"}


def create_user(username: str, age: int):
    users = get_users()
    new_id = 1
    if users:
        new_id = max(user["id"] for user in users) + 1
    new_user = {
        "id": new_id,
        "username": username,
        "age": age,
        "favorites": []
    }
    users.append(new_user)
    with open(USERS_JSON, "w") as file:
        json.dump(users, file, indent=4)

    return new_user


def update_user(user_id: int, username: str, age: int):
    users = get_users()
    for user in users:
        if user["id"] == user_id:
            user["username"] = username
            user["age"] = age
            with open(USERS_JSON, "w") as file:
                json.dump(users, file, indent=4)
            return user
    return {"error": "Usuario no encontrado"}


def delete_user(user_id: int):
    users = get_users()
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            with open(USERS_JSON, "w") as file:
                json.dump(users, file, indent=4)
            return {"message": "Usuario eliminado"}
    return {"error": "Usuario no encontrado"}



# Preferencias de Usuario

def add_rating(user_id: int, streamer_id: str, rating: str):
    users = get_users()
    if rating not in ["like", "dislike"]:
        return {"error": "Debes dar like o dislike"}
    for user in users:
        if user["id"] == user_id:
            if "ratings" not in user:
                user["ratings"] = []
            for streamer in user["ratings"]:
                if streamer["streamer_id"] == streamer_id:
                    streamer["rating"] = rating

                    with open(USERS_JSON, "w") as file:
                        json.dump(users, file, indent=4)
                    return {"message": "Valoración guardada correctamente"}

            user["ratings"].append({
                "streamer_id": streamer_id,
                "rating": rating
            })

            with open(USERS_JSON, "w") as file:
                json.dump(users, file, indent=4)
            return {"message": "Valoración guardada correctamente"}

    return {"error": "Usuario no encontrado"}


def get_ratings(user_id: int):
    users = get_users()
    for user in users:
        if user["id"] == user_id:
            return user.get("ratings", [])
    return {"error": "Usuario no encontrado"}


def delete_rating(user_id: int, streamer_id: str):
    users = get_users()
    for user in users:
        if user["id"] == user_id:
            for streamer in user.get("ratings", []):
                if streamer["streamer_id"] == streamer_id:
                    user["ratings"].remove(streamer)
                    with open(USERS_JSON, "w") as file:
                        json.dump(users, file, indent=4)
                    return {"message": "Valoración eliminada correctamente"}

            return {"error": "No tienes una valoración para este streamer"}

    return {"error": "Usuario no encontrado"}



# Listas de reproducción


def create_playlist(user_id: int, name: str):
    users = get_users()
    for user in users:
        if user["id"] == user_id:
            if "playlists" not in user:
                user["playlists"] = []
            playlist_id = 1
            if user["playlists"]:
                playlist_id = max(playlist["id"] for playlist in user["playlists"]) + 1
            new_playlist = {
                "id": playlist_id,
                "name": name,
                "videos": []
            }
            user["playlists"].append(new_playlist)
            with open(USERS_JSON, "w") as file:
                json.dump(users, file, indent=4)
            return new_playlist

    return {"error": "Usuario no encontrado"}



def get_playlists(user_id: int):
    users = get_users()
    for user in users:
        if user["id"] == user_id:
            result = {
                "user_id": user["id"],
                "playlists": user.get("playlists", [])
            }
            return result
    return {"error": "Usuario no encontrado"}


def add_video(user_id: int, playlist_id: int, video_id: str):
    users = get_users()
    for user in users:
        if user["id"] == user_id:
            for playlist in user.get("playlists", []):
                if playlist["id"] == playlist_id:
                    if video_id in playlist["videos"]:
                        return {"error": "El video ya está en la lista"}
                    playlist["videos"].append(video_id)
                    with open(USERS_JSON, "w") as file:
                        json.dump(users, file, indent=4)
                    return {"message": "Video agregado correctamente"}

            return {"error": "Lista de reproducción no encontrada"}

    return {"error": "Usuario no encontrado"}


def delete_playlist(user_id: int, playlist_id: int):
    users = get_users()
    for user in users:
        if user["id"] == user_id:
            for playlist in user.get("playlists", []):
                if playlist["id"] == playlist_id:
                    user["playlists"].remove(playlist)
                    with open(USERS_JSON, "w") as file:
                        json.dump(users, file, indent=4)
                    return {"message": "Lista de reproducción eliminada"}

            return {"error": "Lista de reproducción no encontrada"}

    return {"error": "Usuario no encontrado"}
