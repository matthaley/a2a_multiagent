import argparse
import logging
import os
from idp.app import app

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Identity Provider Service")
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind the Flask application to",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", "5000")),
        help="Port to bind the Flask application to",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        help="Logging level (e.g., debug, info, warning, error)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable Flask debug mode",
    )

    args = parser.parse_args()

    # Set logging level
    logging.basicConfig(level=getattr(logging, args.log_level.upper()))

    # Run the app
    app.run(host=args.host, port=args.port, debug=args.debug)
