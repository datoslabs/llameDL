import requests

from llamedl.tagsproviders.basetags import BaseTags


class LastFmTags(BaseTags):
    def __init__(self):
        self.api_key = "a7b8b15b54a347be1736dd0f77c7d048"

    def get_tags(self, artist_name: str) -> list:
        data = self._retrieve_data(artist_name)
        if not data:
            return []
        tags = data.get("artist").get("tags").get("tag", [])
        return [tag.get("name").title() for tag in tags]

    def _retrieve_data(self, artist_name: str) -> dict:
        artist = artist_name.replace(" ", "%20")
        url = (
            f"http://ws.audioscrobbler.com/2.0/?method=artist.getInfo"
            f"&artist={artist}"
            f"&user=RJ"
            f"&api_key={self.api_key}"
            f"&format=json"
        )
        response = requests.get(url)
        if response.json().get("error"):
            return {}
        return response.json()
