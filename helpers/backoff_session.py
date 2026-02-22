import requests
import time


# Retry logic, to handle error 429 - Too Many Requests
class BackoffSession(requests.Session):
    def request(self, method, url, *args, max_retries=5, initial_delay=1, **kwargs):
        delay = initial_delay
        for _ in range(max_retries):
            response = super().request(method, url, *args, **kwargs)
            if response.status_code != 429:
                return response
            retry_after = int(response.headers.get("Retry-After", delay))
            time.sleep(retry_after)
            delay *= 2
        raise Exception(f"Too many 429 errors after {max_retries} retries.")
