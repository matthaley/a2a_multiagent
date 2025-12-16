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

FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy project configuration
COPY pyproject.toml /app/

# Copy required modules (auth_lib)
COPY auth_lib /app/auth_lib

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy demo_agent_registry module after dependencies are installed
COPY demo_agent_registry /app/demo_agent_registry

# Create a non-root user for security and set ownership
RUN useradd -m -u 1000 agentregistry && \
    chown -R agentregistry:agentregistry /app

# Set default environment variables
ENV APP_URL=""
ENV HOST="0.0.0.0"
ENV PORT="5001"
ENV LOG_LEVEL="info"

# Expose the default port (Cloud Run will override PORT to 8080 when deployed)
EXPOSE 8080

# Switch to non-root user
USER agentregistry

# Entrypoint script
# Port is read from PORT environment variable (set by Cloud Run)
ENTRYPOINT ["python", "-m", "demo_agent_registry"]
CMD ["--host", "0.0.0.0", "--log-level", "info", "--registry-file", "/app/demo_agent_registry/agent_registry.json"]
