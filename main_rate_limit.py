from rate_limit_decorators import rate_limit
from rate_limit_decorators import time


@rate_limit(max_per_second=2.0)
def fetch_api_data(url: str) -> None:
    print(time.strftime("%H:%M:%S"), f"-> Fetching data from {url}")

# Let's simulate hammering the function rapidly
urls = ["url1", "url2", "url3", "url4"]
for url in urls:
    fetch_api_data(url)