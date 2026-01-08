
# src/agent_app.py
import os, asyncio
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from src.tools.sql_tool import run_sql

INSTRUCTIONS = """You are a BI Analyst Agent.
When the user asks for insights, decide if SQL is needed.
If SQL is needed, construct a safe SELECT query for SQLite schema: sales(order_id, date, region, product, qty, amount).
Return concise tabular results and a short narrative insight.
"""

async def main():
    # These are provided via Codespaces secrets
    endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
    deployment_name = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME")

    if not endpoint or not deployment_name:
        raise RuntimeError("Missing environment variables for Foundry: "
                           "AZURE_AI_PROJECT_ENDPOINT or AZURE_AI_MODEL_DEPLOYMENT_NAME")

    # Authenticate using Azure CLI (attendees will run `az login --use-device-code`)
    async with AzureCliCredential() as cred:
        async with AzureAIAgentClient(
            project_endpoint=endpoint,
            model_deployment_name=deployment_name,
            async_credential=cred,
            agent_name="BI-Agent"
        ).create_agent(instructions=INSTRUCTIONS, tools={"run_sql": run_sql}) as agent:

            # Example prompt BI developers will try first:
            user_prompt = "Top regions by revenue last quarter?"
            result = await agent.run(user_prompt)
            print("\n=== Agent Response ===")
            print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
