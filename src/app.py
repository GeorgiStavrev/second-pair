import os

from app_bootstrap import app
from logger_factory import get_logger

from config import ENV

logger = get_logger(__name__)
logger.info(f"Running on {ENV} environment.")

if __name__ == "__main__":
    # When running locally, disable OAuthlib"s HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    if ENV.lower() == "local":
        app.run("localhost", 4000, debug=True)
    else:
        app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
