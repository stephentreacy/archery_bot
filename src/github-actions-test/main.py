import datetime
import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Test script ran successfully at {current_time}")

    # Demonstrate environment variables
    github_env = os.environ.get("GITHUB_ENV", "Not running in GitHub Actions")
    logger.info(f"GitHub environment: {github_env}")

    os.makedirs("data", exist_ok=True)
    with open("data/last_run.txt", "w") as f:
        f.write(f"Last run: {current_time}")

    logger.info("Test complete!")


if __name__ == "__main__":
    main()
