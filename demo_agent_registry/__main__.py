import argparse
import logging
import os
from demo_agent_registry.app import create_app

if __name__ == "__main__":
    # Get the directory of the current script for default paths
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Agent Registry Application")
    parser.add_argument(
        "--registry-file",
        type=str,
        default=os.path.join(script_dir, 'agent_registry.json'),
        help="Path to the agent registry JSON file",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind the Flask application to",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5001,
        help="Port to bind the Flask application to",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        help="Logging level (e.g., debug, info, warning, error)",
    )

    args = parser.parse_args()

    # Set logging level
    logging.basicConfig(level=getattr(logging, args.log_level.upper()))

    # Create the Flask app using the factory pattern
    app = create_app(registry_file=args.registry_file)

    # Run the app
    app.run(host=args.host, port=args.port, debug=True)
