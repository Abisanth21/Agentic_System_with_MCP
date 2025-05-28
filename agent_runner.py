import requests
import json
import os

# === CONFIGURATION ===
API_URL        = "http://dvt-aiml.wv.mentorg.com:4000/v1/chat/completions"
API_KEY        = os.getenv("LOCAL_LLM_API_KEY", "sk-XP1Dz8AqV23hFzzibzxYkQ")
MODEL_NAME     = "llama3.3"
MCP_SERVER_URL = "http://localhost:8000"

# conversation_history = []
conversation_history = [
    {
      "role": "system",
      "content": (
        "You are a utility assistant. Use getWeather(city) to retrieve current weather, "
        "and convertCurrency(amount, from_currency, to_currency) for exchange rates. "
        "Only call a function when the user explicitly asks for weather or currency conversion."
      )
    }
]
# === Define tools for the LLM ===
tools = [
    {
        "type": "function",
        "function": {
            "name": "getWeather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convertCurrency",
            "description": "Convert currency from one to another",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number"},
                    "from_currency": {"type": "string"},
                    "to_currency": {"type": "string"}
                },
                "required": ["amount", "from_currency", "to_currency"]
            }
        }
    }
]

def call_tool(tool_name, arguments):
    res = requests.post(
        f"{MCP_SERVER_URL}/tools/call",
        json={"name": tool_name, "arguments": arguments}
    )
    res.raise_for_status()
    return res.json()

def run_agent(user_input):
    # 1) Append user message
    conversation_history.append({"role": "user", "content": user_input})

    # 2) Ask the LLM
    payload = {
        "model": MODEL_NAME,
        "messages": conversation_history,
        "tools": tools,
        "tool_choice": "auto",
        "max_tokens": 500,
        "temperature": 0.5
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    choice = data["choices"][0]
    response_message = choice.get("message", {})
    raw_calls = response_message.get("tool_calls", [])

    print("🧠 LLM response_message:", response_message)
    print("🛠️ raw tool_calls:", raw_calls)

    # 3) If the LLM decided to call a tool...
    if raw_calls:
        call = raw_calls[0]

        # Extract name & arguments robustly
        if "name" in call:
            tool_name = call["name"]
            raw_args = call.get("arguments", "{}")
        else:
            fn = call.get("function", {})
            tool_name = fn.get("name")
            raw_args = fn.get("arguments", "{}")

        tool_args = json.loads(raw_args)
        print(f"🔧 Calling tool {tool_name} with args {tool_args}")

        # 4) Execute the tool on the MCP server
        result = call_tool(tool_name, tool_args)
        print("🧾 Tool result:", result)

        # 5) Append the function call & its result to history
        conversation_history.append(response_message)
        conversation_history.append({
            "role": "tool",
            "name": tool_name,
            "content": json.dumps(result)
        })

        # 6) Ask the LLM for a final answer
        followup_payload = {
            "model": MODEL_NAME,
            "messages": conversation_history,
            "max_tokens": 500,
            "temperature": 0.5
        }
        followup = requests.post(API_URL, headers=headers, json=followup_payload)
        followup.raise_for_status()
        final = followup.json()
        final_msg = final["choices"][0]["message"]["content"]
        print("🔁 Final LLM response:", final_msg)
        return final_msg

    # 7) Otherwise, just return what the LLM said
    return response_message.get("content", "[no content]")

if __name__ == "__main__":
    while True:
        user_in = input("Ask me anything: ")
        print("🤖", run_agent(user_in))
