# Retry requests.get() for timeout and other errors
import requests as req
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class ReqRetry:
    def __init__(
        self,
        retries: int = 3,
        backoff_factor: float = 0.3,
        status_forcelist: tuple = (500, 502, 504),
        session: None = None,
    ):

        self.retries = retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist
        self.session = session

    def retry_session(self):
        session = self.session or req.Session()
        retry = Retry(
            total=self.retries,
            read=self.retries,
            connect=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
