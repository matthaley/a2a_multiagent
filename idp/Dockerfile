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

# Copy required modules (idp and auth_lib)
COPY idp /app/idp
COPY auth_lib /app/auth_lib

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create a non-root user for security and set ownership
RUN useradd -m -u 1000 idp && \
    chown -R idp:idp /app

# Set default environment variables
ENV APP_URL=""
ENV IDP_URL="http://localhost:5000"
ENV HOST="0.0.0.0"
ENV PORT=5000
ENV LOG_LEVEL="info"

# Expose the default port
EXPOSE 5000

# Switch to non-root user
USER idp

# Entrypoint script
ENTRYPOINT ["python", "-m", "idp"]
CMD ["--host", "0.0.0.0", "--port", "5000", "--log-level", "info"]
