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
    """
    A module for interacting with https://seon.io
    """
    def __init__(self):
        self._cookies = _loadSessionFromConfig()
        self._refreshJWT()

    def _getRegisteredSocials(self, socials: dict) -> list[str]:
        """
        Returns a list of registered sites based on the input socials data
        """
        return [site for site, data in socials.items() if data.get("registered") == True]

    def _refreshJWT(self) -> str:
        """
        Refreshes the current JWT auth token
        """
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
    
    def _search(self, url: str, data: dict) -> list[str]:
        """
        Performs a SEON search on the input URL with the input data
        """
        try:
            response = requests.post(url, cookies=self._cookies, json=data)
            details = response.json()["socialDetails"]
            return self._getRegisteredSocials(details)
        except Exception as err:
            print(f"Search failed ({err}), retrying")
            self._refreshJWT()
            return self._search(url, data)

    def email(self, email: str) -> list[str]:
        """
        Performs a SEON email search with the input email address
        """
        print(f"Searching for email: {email}")
        url = "https://admin.seon.io/api/v2/manual/manual-input/email"
        data = {"email": email}
        return self._search(url, data)
    
    def phone(self, phone: str) -> list[str]:
        """
        Performs a SEON phone search with the input phone number
        """
        print(f"Searching for phone: {phone}")
        url = "https://admin.seon.io/api/v2/manual/manual-input/phone"
        data = {"phone_number": phone}
        return self._search(url, data)
