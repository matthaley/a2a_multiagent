# Welcome to the Multi-Agent Trip Planner!

This project is a friendly and powerful trip-planning assistant that demonstrates how multiple AI agents can work together to help you plan your next vacation. Think of it as a team of specialists, each with a unique skill, all coordinated by a central "host" agent to make your life easier.

Whether you're a developer curious about multi-agent systems or just someone who wants to see how AI can simplify trip planning, you're in the right place!

## What Can It Do?

Our trip planner is made up of a team of specialized agents:

*   **The Host Agent (Your Personal Concierge):** This is the agent you'll talk to directly. It understands your requests and knows exactly which specialist agent to ask for help.
*   **The Airbnb Agent:** Helps you find the perfect place to stay.
*   **The Calendar Agent:** Checks your Google Calendar to see if you're available for your trip.
*   **The Weather Agent:** Gives you the weather forecast for your destination.
*   **The Horizon Agent (for Order Status):** A special agent that can check the status of an order. This agent is secure and requires you to log in.

## How It Works: A Look Under the Hood

This project is more than just a trip planner; it's a demonstration of a secure and scalable multi-agent system. Here are some of the key concepts:

*   **Teamwork:** The Host Agent acts as a team lead, delegating tasks to the right specialist agent. This is a common pattern in modern AI applications.
*   **Security First:** We use industry-standard OAuth 2.0 to keep your information safe. When you need to access a secure agent (like the Horizon Agent), you'll be asked to log in through a mock "Identity Provider," just like you would with a real application.
*   **Remembering Your Conversation:** The Host Agent saves the state of your conversation in a local database file (`host_agent.db`). This means that even if you need to step away to log in, the agent will remember what you were doing and can pick up right where you left off.

## Getting Started: Let's Get It Running!

Ready to try it out? Here’s how to get the multi-agent trip planner running on your local machine.

### Step 1: Install the Necessary Tools

First, you'll need to install all the project's dependencies. It's a good idea to do this in a virtual environment. Open your terminal and run this command from the project's root directory:

```bash
pip install -e .
```

### Step 2: Set Up the "Identity Provider"

To simulate a real login experience, we need to set up a mock "Identity Provider." This requires generating a set of secure keys.

1.  **Generate a Private Key:**
    ```bash
    ssh-keygen -t rsa -b 2048 -m PEM -f idp/idp_rsa -N ""
    ```

2.  **Create a Public Key:**
    ```bash
    openssl rsa -in idp/idp_rsa -pubout -out idp/pubkey.pub
    ```

3.  **Generate the Final Key File:**
    ```bash
    (cd idp && python3 generate_jwks.py)
    ```

### Step 3: Start All the Services

Now, it's time to bring our team of agents to life! You'll need to open **7 separate terminal windows**. In each one, you'll run one of the following commands from the project's root directory.

*   **Terminal 1: Start the Identity Provider**
    ```bash
    python -m idp.app
    ```

*   **Terminal 2: Start the Agent Registry**
    ```bash
    python -m demo_agent_registry.app
    ```

*   **Terminal 3: Start the Weather Agent**
    ```bash
    python -m weather_agent
    ```

*   **Terminal 4: Start the Calendar Agent**
    ```bash
    python -m calendar_agent
    ```

*   **Terminal 5: Start the Horizon Agent**
    ```bash
    python -m horizon_agent --port 10008 --tenant-id tenant-abc
    ```

*   **Terminal 6: Start the Airbnb Agent**
    ```bash
    python -m airbnb_agent
    ```

*   **Terminal 7: Start the Host Agent (Your Concierge!)**
    ```bash
    python -m host_agent --port 8083 --tenant-id tenant-abc
    ```

### Step 4: Chat with Your Agent!

Once all the services are running, you can start chatting with your personal trip-planning concierge.

1.  Open your web browser and go to: **http://localhost:8083**
2.  You'll see a chat window. Try asking it a question! For example, to test the secure agent, you could ask:
    `what is the status of order 123`
3.  The agent will give you a link to log in. Click the link and use the following credentials:
    *   **Username:** `john.doe`
    *   **Password:** `password123`
4.  After you grant consent, you'll be redirected back to the chat. Just type "done" to let the agent know you're finished, and it will complete your request!

We hope you enjoy exploring the world of multi-agent AI!
