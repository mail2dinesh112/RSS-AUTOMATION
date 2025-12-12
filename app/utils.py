import time

def retry(func, attempts=3, delay=2):
    for attempt in range(attempts):
        try:
            return func()
        except Exception as e:
            print(f"Retry {attempt + 1}/{attempts} failed:", e)
            time.sleep(delay)
    raise RuntimeError("Max retries exceeded")
