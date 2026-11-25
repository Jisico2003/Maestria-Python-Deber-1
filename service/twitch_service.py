
import requests

BASE_URL = "https://api.twitch.tv/helix"


def twitch_credentials(client_id: str, access_token: str):
    credentials = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}"
    }
    return credentials


def get_streamer(login: str, client_id: str, access_token: str):
    url = f"{BASE_URL}/users?login={login}"
    credentials = twitch_credentials(client_id, access_token)

    try:
        response = requests.get(url, headers=credentials, timeout=10)
        if response.status_code != 200:
            return {"error": "Error al obtener el streamer"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    streamer_data = response.json()
    return streamer_data


def get_twitch_stream(username: str, client_id: str, access_token: str):
    url = f"{BASE_URL}/streams?user_login={username}"
    credentials = twitch_credentials(client_id, access_token)

    try:
        response = requests.get(url, headers=credentials, timeout=10)
        if response.status_code != 200:
            return {"error": "Error al obtener la transmision"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    stream_data = response.json()
    return stream_data


def search_streamers(query: str, client_id: str, access_token: str):
    url = f"{BASE_URL}/search/channels?query={query}"
    credentials = twitch_credentials(client_id, access_token)

    try:
        response = requests.get(url, headers=credentials, timeout=10)
        if response.status_code != 200:
            return {"error": "Error al buscar streamers"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    search_data = response.json()
    return search_data


def get_streamer_videos(user_id: str, client_id: str, access_token: str):
    url = f"{BASE_URL}/videos?user_id={user_id}"
    credentials = twitch_credentials(client_id, access_token)

    try:
        response = requests.get(url, headers=credentials, timeout=10)
        if response.status_code != 200:
            return {"error": "Error al obtener videos"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    videos_data = response.json()
    return videos_data
