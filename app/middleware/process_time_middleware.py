import time

from fastapi import Request


def calculate_process_time(start: float) -> float:
    """
    Utility function to calculate processing time
    """
    return round(time.perf_counter() - start, 3)


async def add_process_time_header(request: Request, call_next):
    """
    Middleware to measure and record the processing time for each HTTP request.

    - Records the start time before processing the request.
    - Calls the next handler in the middleware chain.
    - Calculates the elapsed time after the response is generated.
    - Adds the elapsed time as an "X-Process-Time" header to the response.

    Args:
        request (Request): The incoming FastAPI request object.
        call_next (Callable): The next middleware or route handler.

    Returns:
        Response: The HTTP response with the process time header included.
    """
    # Record start time of request processing
    start = time.perf_counter()

    # Proceed with request handling
    response = await call_next(request)

    # Add process time as header to the response
    process_time = calculate_process_time(start)
    response.headers["X-Process-Time"] = f"{process_time} s."

    return response
