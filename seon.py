import json
import requests

def _loadSessionFromConfig() -> dict:
    with open("config.json", "r") as file:
        config = json.loads(file.read())
        if config.get("session") == "" or config.get("session") == None:
            print("You did not finish the setup (session is null)")
            exit()
        return {
            "seon-refresh": config["session"]
        }

class SEON:
    def __init__(self):
        self._cookies = _loadSessionFromConfig()
        self._refreshJWT()

    def _getRegisteredSocials(self, socials: dict) -> list[str]:
        return [site for site, data in socials.items() if data.get("registered") == True]

    def _refreshJWT(self):
        try:
            url = "https://login.seon.io/api/auth/renew"
            data = {}
            response = requests.post(url, cookies=self._cookies, json=data)
            result = response.json()

            jwt = result["jwt"]
            self._cookies["seon-jwt"] = jwt

            return jwt
        except:
            print("Invalid session was passed")
            exit()
    
    def _search(self, url: str, data: dict):
        try:
            response = requests.post(url, cookies=self._cookies, json=data)
            details = response.json()["socialDetails"]
            return self._getRegisteredSocials(details)
        except Exception as err:
            print(f"Search failed ({err}), retrying")
            self._refreshJWT()
            return self._search(url, data)

    def email(self, email: str):
        print(f"Searching for email: {email}")
        url = "https://admin.seon.io/api/v2/manual/manual-input/email"
        data = {"email": email}
        return self._search(url, data)
    
    def phone(self, phone: str) -> list[str]:
        print(f"Searching for phone: {phone}")
        url = "https://admin.seon.io/api/v2/manual/manual-input/phone"
        data = {"phone_number": phone}
        return self._search(url, data)
