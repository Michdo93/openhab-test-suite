import requests
import json

class OpenHABConnector:
    def __init__(self, url:str, username:str = None, password:str = None):
        self.url = url
        self.username = username
        self.password = password
        self.isCloud = False
        self.isLoggedIn = False

        self.session = requests.Session()

        if self.username is not None and self.password is not None:
            self.auth = (self.username, self.password)
            self.session.auth = self.auth
        else:
            self.auth = None
            self.session.auth = None

        self.__login()

    def __login(self):
        if self.url == "https://myopenhab.org" or self.url == "https://myopenhab.org/":
            self.url = "https://myopenhab.org"
            self.isCloud = True
            url = self.url
        else:
            if self.url[-1] == "/":
                self.url = self.url[:-1]
            self.isCloud = False
            url = self.url + "/rest"

        try:
            login_response = self.session.get(url, auth=self.auth, timeout=8)
            login_response.raise_for_status()

            if login_response.ok or login_response.status_code == 200:
                self.isLoggedIn = True
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def __executeRequest(self, header:dict = None, resource_path:str = None, method:str = None, data = None):
        if resource_path is not None and method is not None:
            method = method.lower()

            if not "/rest" in resource_path:
                resource_path = "/rest" + resource_path
            self.session.headers.update(header)
            try:
                if method == "get":
                    response = self.session.get(self.url + resource_path, auth=self.auth, timeout=5)
                    response.raise_for_status()

                    if response.ok or response.status_code == 200:
                        if "/state" in resource_path or resource_path.find("/state") != -1:
                            return response.text
                        return json.loads(response.text)
                elif method == "put":
                    response = self.session.put(self.url + resource_path, auth=self.auth, data=data, timeout=5)
                    response.raise_for_status()

                    return None
                elif method == "post":
                    response = self.session.post(self.url + resource_path, auth=self.auth, data=data, timeout=5)
                    response.raise_for_status()

                    return None
                elif method == "delete":
                    response = self.session.delete(self.url + resource_path, auth=self.auth, timeout=5)
                    response.raise_for_status()

                    return None
                else:
                    raise ValueError('The entered http method is not valid for accessing the rest api!')
            except requests.exceptions.HTTPError as errh:
                print(errh)
            except requests.exceptions.ConnectionError as errc:
                print(errc)
            except requests.exceptions.Timeout as errt:
                print(errt)
            except requests.exceptions.RequestException as err:
                print(err)
        else:
            raise ValueError('You have to enter a valid resource path for accessing the rest api!')

    def get(self, endpoint: str, headers=None):
        """GET-Anfrage an den OpenHAB-Server"""
        return self.__executeRequest(headers, endpoint, "get")

    def post(self, endpoint: str, headers=None, data=None):
        """POST-Anfrage an den OpenHAB-Server"""
        return self.__executeRequest(headers, endpoint, "post")

    def put(self, endpoint: str, headers=None, data=None):
        """PUT-Anfrage an den OpenHAB-Server"""
        return self.__executeRequest(headers, endpoint, "put")

    def delete(self, endpoint: str, headers=None, data=None):
        return self.__executeRequest(headers, endpoint, "delete")
