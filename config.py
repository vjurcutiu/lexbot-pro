from openai import OpenAI

try:
    # Initialize the OpenAI client globally
    client = OpenAI()

    # Create and configure the assistant once
    assistant = client.beta.assistants.create(
        name="testbot",
        instructions="You are an expert legal analyst. Use your knowledge base to answer questions about legal cases.",
        model="gpt-4o-mini",
        tools=[{"type": "file_search"}],
    )

    # Update the assistant with tool resources
    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": ['vs_blMFhWfdfa27zronK3PbQDAR']}},
    )

except Exception as e:
    # Handle initialization errors gracefully
    print(f"Error during OpenAI client or assistant initialization: {e}")
    client = None
    assistant = None