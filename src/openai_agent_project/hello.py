import chainlit as cl
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from agents import Agent,Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel

gemini_api_key = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent1 = Agent(
    name = "Assistant",
    instructions= "you are a helpful assistant yau can answer the question of the user"
)

# print(result.final_output)


@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content = "Hello, how can I help you today?").send()


@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})
    result = await Runner.run(
      input = history,
      run_config=config,
      starting_agent= agent1,
    )

    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
    await cl.Message(content= result.final_output).send()


