from observability.logger import setup_logger
import time
import random

logger = setup_logger()

def simulate_service():
    """
    For intentional ZeroDivisionError
    """
    logger.info("Service started")
    while True:
        val = 0
        try:
            div = 100/val
            logger.info(f"Processing value: {div}")
        except Exception as e:
            logger.error(e)
        time.sleep(2)

def login_user(request):
    try:
        user_data = request.get("user")  # This will fail if "user" is None
        user_email = user_data.get("email")  # Intentional bug: accessing 'get' on None
        print(f"Authenticating {user_email}")
    except Exception as e:
        logger.error(e)
    return True


if __name__ == "__main__":
    # Simulate a request missing the "user" key
    fake_request = {}
    login_user(fake_request)

# if __name__ == "__main__":
#     simulate_service()