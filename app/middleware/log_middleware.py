import html
import time

from fastapi import Request

MAX_REDIRECT_COUNT = 10
IGNORED_USER_AGENTS = ["GoogleStackdriverMonitoring-UptimeChecks(https://cloud.google.com/monitoring)"]


async def calculate_process_time(start: float) -> float:
    """
    Utility function to calculate processing time
    """
    return round(time.perf_counter() - start, 3)


async def get_request_url(request: Request) -> str:
    """
    Utility function to get the request URL
    """
    # Get the query params if any:
    query_params = f"?{request.query_params}" if request.query_params else ""

    # create the url:
    url = f"{request.url.path}{query_params}"

    # escape any html characters in the url:
    url = html.escape(url)

    return url


async def log_and_track_request_process_time(request: Request, call_next):
    """
    Asynchronous middleware function that:

    1. Calculates the process time for handling a request.
    2. Adds the process time as an "X-Process-Time" header to the response.
    3. Logs request details (excluding static files) as a background task.


    Args:
        request (Request): The incoming request object.
        call_next (Callable): The function to call to proceed with the request handling.

    Returns:
        Response: The response object with added process time header.
    """

    # Record start time of request processing
    start = time.perf_counter()

    # Check if the request is for a static file
    if request.url.path.startswith("/assets"):
        # Allow serving static files without blocking checks
        response = await call_next(request)

        # Add process time as header to the response
        response.headers["X-Process-Time"] = f"{str(await calculate_process_time(start=start))} s."
        return response

    # Proceed with request handling
    response = await call_next(request)

    # Add process time as header to the response
    response.headers["X-Process-Time"] = f"{str(await calculate_process_time(start=start))} s."

    return response
