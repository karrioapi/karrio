from google.adk.agents import Agent

root_agent = Agent(
    name="karrio_agent",
    model="gemini-1.5-flash",
    description=(
        "Agent to assist with Karrio shipping carrier integrations."
    ),
    instruction=(
        "You are a helpful agent who can assist developers to build shipping integrations under the Karrio umbrella."
    ),
    tools=[],
)
