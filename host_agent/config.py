# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Configuration module for the host agent.

This module loads configuration from a JSON file and provides centralized
access to URLs and other settings. Values can be overridden via environment
variables.
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Get the directory where this config.py file is located
_CONFIG_DIR = Path(__file__).parent
_CONFIG_FILE = _CONFIG_DIR / "config.json"


def _load_config():
    """Load configuration from JSON file."""
    try:
        with open(_CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file not found: {_CONFIG_FILE}. "
            "Please ensure config.json exists in the host_agent directory."
        )
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")


_config = _load_config()

# Agent Registry Configuration
AGENT_REGISTRY_BASE_URL = os.getenv(
    "AGENT_REGISTRY_BASE_URL", _config["agent_registry"]["base_url"]
)
AGENT_REGISTRY_URL = os.getenv(
    "AGENT_REGISTRY_URL", _config["agent_registry"]["url"]
)

# Identity Provider (IDP) Configuration
IDP_BASE_URL = os.getenv("IDP_BASE_URL", _config["idp"]["base_url"])
IDP_TOKEN_URL = os.getenv("IDP_TOKEN_URL", _config["idp"]["token_url"])
IDP_AUTHORIZE_URL = os.getenv("IDP_AUTHORIZE_URL", _config["idp"]["authorize_url"])

# Host Agent Configuration
REDIRECT_URI = os.getenv("REDIRECT_URI", _config["host_agent"]["redirect_uri"])
