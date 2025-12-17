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

from google.adk import Agent


def create_root_agent(tenant_id: str) -> Agent:
    """Creates the horizon agent with tenant-specific context.
    
    Args:
        tenant_id: The tenant ID for this agent instance.
        
    Returns:
        An Agent configured for the specified tenant.
    """
    
    async def get_order_status(order_id: str) -> str:
        """Gets the status of a specific order.

        Args:
            order_id: The ID of the order to check.

        Returns:
            A string indicating the order status.
        """
        # In a real application, this would query a database or an order management system
        # filtered by tenant_id. For this example, we'll return a mock status.
        return f"The status of order {order_id} is: Shipped"

    return Agent(
        model='gemini-2.5-flash',
        name='horizon_agent',
        description=f'Agent that can check order status for tenant {tenant_id}.',
        instruction=(
            f"Always structure your response in this format: '[{tenant_id}] [status message]' "
            "to clearly indicate which tenant the information is for."
        ),
        tools=[
            get_order_status,
        ],
    )
