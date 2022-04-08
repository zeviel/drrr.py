import requests


class DrrrClient:
    def __init__(self, language: str = "en-US"):
        self.api = "https://drrr.com"
        self.auth_token = None
        self.client_token = None
        self.language = language
        self.tokens = self.get_tokens()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-N975F Build/N2G48H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.120 Mobile Safari/537.36",
            "cookie": f"drrr-session-1={self.client_token}"}

    def login(
            self,
            nickname: str,
            icon: str = "kuromu-2x",
            language: str = "en-US"):
        data = {
            "name": nickname,
            "icon": icon,
            "token": self.auth_token,
            "login": "ENTER",
            "language": self.language
        }
        return requests.post(
            f"{self.api}?api=json",
            data=data,
            headers=self.headers).json()

    def create_room(
            self,
            name: str,
            description: str,
            users_limit: int = 5,
            music: bool = False,
            adult: bool = False,
            conceal: bool = False):
        data = {
            "name": name,
            "description": description,
            "limit": users_limit,
            "language": self.language,
            "submit": "Create Room"
        }
        if music:
            data["music"] = music
        elif adult:
            data["adult"] = adult
        elif conceal:
            data["conceal"] = conceal
        return requests.post(
            f"{self.api}/create_room?api=json",
            data=data,
            headers=self.headers).json()

    def join_room(self, room_id: str):
        return requests.get(
            f"{self.api}/room?id={room_id}&api=json",
            headers=self.headers).json()

    def leave_room(self, room_id: str):
        data = {"leave": "leave"}
        return requests.post(
            f"{self.api}/room?ajax=1&api=json",
            data=data,
            headers=self.headers).json()

    def transfer_host(self, user_id: str):
        data = {"new_host": user_id}
        return requests.post(
            f"{self.api}/room?ajax=1&api=json",
            data=data,
            headers=self.headers).json()

    def ban_user(self, user_id: str):
        data = {"ban": user_id}
        return requests.post(
            f"{self.api}/room?ajax=1&api=json",
            data=data,
            headers=self.headers).json()

    def kick_user(self, user_id: str):
        data = {"kick": user_id}
        return requests.post(
            f"{self.api}/room?ajax=1&api=json",
            data=data,
            headers=self.headers).json()

    def send_message(self, message: str, url: str = "", to: str = ""):
        data = {
            "message": message,
            "url": url,
            "to": to
        }
        return requests.post(
            f"{self.api}/room?ajax=1&api=json",
            data=data,
            headers=self.headers).json()

    def edit_room(self, title: str = None, description: str = None):
        data = {}
        if title:
            data["room_name"] = title
        elif description:
            data["room_description"] = description
        return requests.post(
            f"{self.api}/room?ajax=1&api=json",
            data=data,
            headers=self.headers).json()

    def play_music_in_room(self, name: str, url: str):
        data = {
            "music": "music",
            "name": name,
            "url": url
        }
        return requests.post(
            f"{self.api}/room?ajax=1&api=json",
            data=data,
            headers=self.headers).json()

    def get_room_info(self):
        return requests.get(
            f"{self.api}/json.php?fast=1",
            headers=self.headers).json()

    def get_current_session(self):
        return requests.get(
            f"{self.api}/profile?api=json",
            headers=self.headers).json()

    def get_lounge(self):
        return requests.get(
            f"{self.api}/lounge?api=json",
            headers=self.headers).json()

    def get_tokens(self):
        response = requests.get(f"{self.api}?api=json").json()
        self.client_token = response["Authorization"]
        self.auth_token = response["token"]
        return self.client_token, self.auth_token
