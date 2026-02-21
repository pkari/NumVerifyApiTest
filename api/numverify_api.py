from helpers.backoff_session import BackoffSession


class NumVerifyAPI:
    BASE_URL = "https://apilayer.net/api"

    VALIDATE_URL = "/validate"

    def __init__(self, api_key):
        self.api_key = api_key
        self.session = BackoffSession()

    def get_number_validation(self, number, country_code="", j_format=1):
        params = {
            "access_key": self.api_key,
            "number": number,
            "country_code": country_code,
            "format": j_format
        }
        response = self.session.get(f"{self.BASE_URL}{self.VALIDATE_URL}", params=params)
        return response

