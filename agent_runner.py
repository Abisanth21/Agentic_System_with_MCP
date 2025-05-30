import requests
import json
import os

# === CONFIGURATION ===
API_URL        = "http://dvt-aiml.wv.mentorg.com:4000/v1/chat/completions"
API_KEY        = os.getenv("LOCAL_LLM_API_KEY", "sk-XP1Dz8AqV23hFzzibzxYkQ")
MODEL_NAME     = "llama3.3"
MCP_SERVER_URL = "http://localhost:8000"

conversation_history = [
    {
        "role": "system",
        "content": (
            "You are a utility assistant. Use getWeather(city) to fetch current weather "
            "and convertCurrency(amount, from_currency, to_currency) to convert currency."
        )
    }
]

def fetch_tools_from_mcp():
    """Fetch tool schemas dynamically from MCP server."""
    res = requests.get(f"{MCP_SERVER_URL}/tools/list")
    res.raise_for_status()
    return res.json()

def call_tool(tool_name, arguments):
    """Call the MCP server tool with arguments."""
    res = requests.post(
        f"{MCP_SERVER_URL}/tools/call",
        json={"name": tool_name, "arguments": arguments}
    )
    res.raise_for_status()
    return res.json()

def run_agent(user_input):
    conversation_history.append({"role": "user", "content": user_input})

    tools = fetch_tools_from_mcp()

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

    if raw_calls:
        call = raw_calls[0]

        if "name" in call:
            tool_name = call["name"]
            raw_args = call.get("arguments", "{}")
        else:
            fn = call.get("function", {})
            tool_name = fn.get("name")
            raw_args = fn.get("arguments", "{}")

        tool_args = json.loads(raw_args)
        print(f"🔧 Calling tool {tool_name} with args {tool_args}")

        result = call_tool(tool_name, tool_args)
        print("🧾 Tool result:", result)

        conversation_history.append(response_message)
        conversation_history.append({
            "role": "tool",
            "name": tool_name,
            "content": json.dumps(result)
        })

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

    return response_message.get("content", "[no content]")

if __name__ == "__main__":
    while True:
        user_in = input("Ask me anything: ")
        print("🤖", run_agent(user_in))
