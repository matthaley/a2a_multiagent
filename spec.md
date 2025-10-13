# spec.md

(Sections 1 and 2 - No changes)

## 2. System Components

The system is composed of a central orchestrator and several independent services and agents.

*   **`host_agent`**: The central orchestrator and single entry point for users. It uses an LLM to understand user prompts and route them to the appropriate downstream agent. It also manages the security flow and persists session and task state.
*   **Downstream Agents**:
    *   **`airbnb_agent`**: A tool-using agent that can search for accommodations.
    *   **`calendar_agent`**: A secure, tool-using agent that can check a user's Google Calendar after an interactive OAuth flow.
    *   **`weather_agent`**: A simple agent that provides weather forecasts.
    *   **`horizon_agent`**: A secure, tenant-specific agent for retrieving order status, requiring a JWT for access.
*   **`auth_lib`**: A shared library responsible for JWT validation, used by all secure downstream agents to protect their endpoints.
*   **`idp`**: A mock OAuth 2.0 Identity Provider that issues JWTs for the authentication flow.
*   **`demo_agent_registry`**: A service discovery mechanism that provides the `host_agent` with the necessary endpoint information for all downstream agents.

## 3. Multi-Tenancy

The system is designed for multi-tenancy, where each tenant is isolated.

*   The `host_agent` is started with a specific `tenant-id`.
*   It uses this `tenant-id` to query the `demo_agent_registry` to discover the correct downstream agents configured for that specific tenant.
*   For secure, tenant-specific agents like the `horizon_agent`, the JWT issued by the IDP contains a `tenant_id` claim. The agent's token validation logic ensures that the `tenant_id` in the token matches the `tenant_id` the agent was configured with, preventing cross-tenant data access.

## 4. Testing Strategy

To ensure the robustness of the security model and prevent regressions, the project includes a suite of unit tests.

*   **Coverage**: Unit tests are provided for all downstream agent executors (`weather`, `horizon`, `airbnb`, `calendar`).
*   **Focus**: The tests specifically validate the authentication logic by mocking the `is_token_valid` function and simulating requests with valid, invalid, and missing bearer tokens.
*   **Execution**: Tests are run from the project root using the `unittest discover` command to ensure correct module resolution within Python's packaging system.

## 5. Security Model & Authentication Flow

End-to-end security is provided by OAuth 2.0, with session state managed by a persistent `DatabaseSessionService`. The asynchronous authentication flow is managed using the A2A Task Lifecycle.

### 5.1. Authentication Flow

1.  A user interacts with the `host_agent`'s Gradio UI.
2.  The `host_agent`'s LLM routes the request to the secure `horizon_agent`.
3.  The `send_message` tool checks the session state for an `access_token`.
4.  If no token is found, it initiates the OAuth 2.0 flow:
    a.  It creates a long-running A2A **Task** to represent the user's original request.
    b.  It returns a `redirect_url` to the user, pointing to the IDP.
5.  The user authenticates via the IDP and is redirected to the `host_agent`'s `/callback` endpoint.
6.  The `/callback` endpoint exchanges the authorization code for an `access_token` and a `refresh_token`, and writes them to the session state in the SQLite database.
7.  The user returns to the UI and sends a message (e.g., "done") to notify the agent that authentication is complete.
8.  The `host_agent` receives the new message and re-attempts the original task.
9.  The `send_message` tool, executing again, now finds the `access_token` in the session state.
10. It adds the token to an `Authorization` header and successfully calls the `horizon_agent`.

### 5.1.1. Token Refresh Flow

If the `access_token` has expired, the `host_agent` automatically attempts to refresh it.

1.  The `host_agent` sends a request to a downstream agent with an expired `access_token`.
2.  The downstream agent rejects the request with a "token has expired" error.
3.  The `host_agent` catches this specific error and checks the session for a `refresh_token`.
4.  If a `refresh_token` exists, the `host_agent` calls the IDP's `/generate-token` endpoint with the `refresh_token`.
5.  The IDP validates the `refresh_token` and issues a new `access_token`.
6.  The `host_agent` updates the session state with the new `access_token`.
7.  The `host_agent` automatically retries the original request to the downstream agent with the new `access_token`.

### 5.2. A2A Task Lifecycle for Asynchronous Operations

The system uses a stateful, persistent task management flow to handle long-running asynchronous operations like user authentication.

-   A `PersistentTaskStore`, backed by a SQLite database, is used to save and retrieve the state of every user request (`Task`).
-   When a secure agent requires authentication, the original task is saved with a `submitted` status.
-   After the user completes the OAuth 2.0 flow, the `/callback` endpoint retrieves the original task, updates its status to `working`, and saves the user's access token to the persistent session.
-   This robust, stateful mechanism allows the agent to seamlessly resume the user's original request without losing context.

### 5.3. Task Delegation and Linking

When the `host_agent` delegates a task to a downstream agent, it follows the A2A specification for task creation to ensure a robust, distributed system.

1.  **Local Task Creation**: The `host_agent` first creates a `Task` in its own `PersistentTaskStore`. This task represents the user's original request to the host.
2.  **Message without Task ID**: The `host_agent` sends a `message:send` request to the downstream agent. Crucially, this message **does not** contain a `taskId`.
3.  **Remote Task Creation**: The downstream agent receives this request and, per the A2A specification, creates a *new* task in its own task store.
4.  **Response with Task Object**: The downstream agent's immediate response to the `message:send` request is a `Task` object containing the `id` of the newly created remote task.
5.  **Linking**: The `host_agent` receives this response, extracts the `remote_task_id`, and updates its original, local `Task` record with this new ID. This creates a durable link between the parent task in the host and the child task in the downstream agent.

### Testing Secrets Management

To maintain security and prevent the accidental commitment of sensitive information, private keys and other secrets required for running the unit test suite must be handled as follows:

1.  **Configuration File**: Secrets for the `auth_lib` tests, such as the private key for signing test JWTs, must be stored in a file named `auth_lib/test_config.py`.

2.  **Git Ignore**: The file `auth_lib/test_config.py` is explicitly listed in the project's root `.gitignore` file and must never be committed to version control.

3.  **Example Template**: A template file, `auth_lib/test_config.example.py`, is provided in the repository. To set up a local test environment, copy this file to `auth_lib/test_config.py` and populate it with the necessary secret values.

4.  **Usage**: The test suite will import secrets from `auth_lib.test_config`.