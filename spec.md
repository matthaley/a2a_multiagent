# spec.md

(Sections 1 and 2 - No changes)

## 3. Security Model & Authentication Flow

End-to-end security is provided by OAuth 2.0, with session state managed by a persistent `DatabaseSessionService`. The asynchronous authentication flow is managed using the A2A Task Lifecycle.

### 3.1. Authentication Flow

1.  A user interacts with the `host_agent`'s Gradio UI.
2.  The `host_agent`'s LLM routes the request to the secure `horizon_agent`.
3.  The `send_message` tool checks the session state for an `access_token`.
4.  If no token is found, it initiates the OAuth 2.0 flow:
    a.  It creates a long-running A2A **Task** to represent the user's original request.
    b.  It returns a `redirect_url` to the user, pointing to the IDP.
5.  The user authenticates via the IDP and is redirected to the `host_agent`'s `/callback` endpoint.
6.  The `/callback` endpoint exchanges the authorization code for an `access_token` and writes it to the session state in the SQLite database.
7.  The user returns to the UI and sends a message (e.g., "done") to notify the agent that authentication is complete.
8.  The `host_agent` receives the new message and re-attempts the original task.
9.  The `send_message` tool, executing again, now finds the `access_token` in the session state.
10. It adds the token to an `Authorization` header and successfully calls the `horizon_agent`.

*   **Implementation Notes:**
    *   The implementation should use the `TaskUpdater.requires_auth()` method to signal that authentication is required.

### 3.2. A2A Task Lifecycle for Asynchronous Operations

The system uses a stateful, persistent task management flow to handle long-running asynchronous operations like user authentication.

-   A `PersistentTaskStore`, backed by a SQLite database, is used to save and retrieve the state of every user request (`Task`).
-   When a secure agent requires authentication, the original task is saved with a `submitted` status.
-   After the user completes the OAuth 2.0 flow, the `/callback` endpoint retrieves the original task, updates its status to `working`, and saves the user's access token to the persistent session.
-   This robust, stateful mechanism allows the agent to seamlessly resume the user's original request without losing context.

### 3.3. Asynchronous Task Delegation

To provide a responsive user experience, the system uses an asynchronous task delegation model. The `host_agent` does not wait for downstream agents to complete their work.

1.  **Local Task Creation**: The `host_agent` creates a `Task` in its own `PersistentTaskStore`.
2.  **Asynchronous Hand-off**: The `host_agent` sends a `message:send` request to the downstream agent. It does **not** wait for the task to be completed.
3.  **Immediate User Feedback**: The `host_agent` immediately responds to the user, confirming that the task has been started and providing the local `task_id`.
4.  **Remote Task Creation & Linking**: The downstream agent creates its own task and returns the `remote_task_id` to the `host_agent`, which then links the two tasks in its database.
5.  **Checking Status**: The user can ask for the status of a task at any time using the `task_id`. The `host_agent` will then query the downstream agent to get the latest status.
