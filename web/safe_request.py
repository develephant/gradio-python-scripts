
# Reusable HTTP Request Wrapper
# Python

import httpx

def safe_request(method: str, url: str, **kwargs) -> httpx.Response:
    """
    Makes an HTTP request with consistent error handling.
    
    Args:
        method (str): HTTP method ("GET", "POST", etc.)
        url (str): Target URL.
        **kwargs: Additional arguments for httpx.request (params, data, files, json, timeout, etc.)
    
    Returns:
        httpx.Response: The successful HTTP response object.
    
    Raises:
        httpx.RequestError: For network-related errors.
        httpx.HTTPStatusError: For non-2xx/3xx HTTP responses.
    """
    try:
        response = httpx.request(method, url, **kwargs)
        response.raise_for_status()  # Will raise HTTPStatusError if status >= 400
        return response

    except httpx.RequestError as e:
        print(f"❌ Network error while requesting {e.request.url!r}: {e}")
        raise  # Re-raise so caller can handle if needed

    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP error {e.response.status_code} for {e.request.url!r}")
        print(f"Response body: {e.response.text}")
        raise  # Re-raise so caller can handle if needed


# Example Usage
# Python

if __name__ == "__main__":
    try:
        # Example GET request
        resp = safe_request("GET", "https://httpbin.org/status/200")
        print("✅ Success:", resp.text[:100])

        # Example POST with JSON
        resp = safe_request(
            "POST",
            "https://httpbin.org/post",
            json={"name": "Alice"},
            timeout=5.0
        )
        print("✅ POST Success:", resp.json())

        # Example that triggers an error
        safe_request("GET", "https://httpbin.org/status/404")

    except Exception as e:
        print("⚠️ Request failed:", e)


# Benefits of This Pattern

# Centralized error handling — no need to repeat try/except everywhere.
# Consistent logging — all errors are reported in the same format.
# Flexible — works for GET, POST, PUT, DELETE, file uploads, etc.
# Re-raises exceptions so the caller can decide whether to stop or retry.


# If you want, I can extend this so it automatically retries failed requests with exponential backoff — which is very useful for unstable networks or flaky APIs.
# Do you want me to add that retry logic?
