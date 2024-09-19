import json
import requests

def _readFile(fileName: str) -> str:
    """
    Reads the input fileName's data
    """
    with open(fileName, "r") as file:
        return file.read()

def _writeFile(fileName: str, data: str | dict | list, format=True):
    """
    Writes the input data to the input fileName
    - If the data is a dict or a list, it will deserialize it automatically
    """
    with open(fileName, "w") as file:
        if type(data) in (dict, list):
            if format:
                data = json.dumps(data, indent=4)
            else:
                data = json.dumps(data)
        file.write(data)
    
def _readFileLines(fileName: str, strip=True) -> list[str]:
    """
    Reads the input fileName's lines
    """
    with open(fileName, "r") as file:
        return [line.strip() if strip else line for line in file.readlines()]

def _loadSessionFromConfig() -> dict:
    """
    Loads session cookies from the config.json file
    """
    config = json.loads(_readFile("config.json"))
    if config.get("session") in ("", None):
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
        phone = phone.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
        if not phone.startswith("+"):
            phone = "+1" + phone

        print(f"Searching for phone: {phone}")

        url = "https://admin.seon.io/api/v2/manual/manual-input/phone"
        data = {"phone_number": phone}
        return self._search(url, data)
    
    def phoneFile(self, fileName: str) -> list[str]:
        """
        Performs a SEON phone search with the input file name
        """
        results = {}
        phones = _readFileLines(fileName)
        for phone in phones:            
            if results.get(phone):
                continue
            result = self.phone(phone)
            results[phone] = result
        _writeFile("search.json", results)
        return results

    def emailFile(self, fileName: str) -> list[str]:
        """
        Performs a SEON email search with the input file name
        """ 
        results = {}
        emails = _readFileLines(fileName)
        for email in emails:
            if results.get(email):
                continue
            result = self.email(email)
            results[email] = result
        _writeFile("search.json", results)
        return results
