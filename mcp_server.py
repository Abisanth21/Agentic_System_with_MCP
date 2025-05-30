# mcp_server.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from tools.get_weather import get_weather
from tools.convert_currency import convert_currency

app = FastAPI()

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    return {
        "schema_version": "v1",
        "name_for_human": "Utility Agent MCP Server",
        "name_for_model": "utility_agent",
        "description_for_human": "Provides weather and currency conversion tools",
        "description_for_model": "Use this to access weather and currency conversion tools",
        "api": {"type": "openapi", "url": "/openapi.json"},
        "auth": {"type": "none"},
    }

@app.get("/tools/list")
async def list_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "getWeather",
                "description": "Get current weather for a city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"}
                    },
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

@app.post("/tools/call")
async def call_tool(request: Request):
    try:
        body = await request.json()
        name = body["name"]
        args = body["arguments"]
        
        print(f"🔧 Tool called: {name}")
        print(f"📋 Arguments received: {args}")

        if name == "getWeather":
            if "city" not in args:
                return JSONResponse(status_code=400, content={"error": "Missing required parameter: city"})
            return get_weather(args["city"])
            
        elif name == "convertCurrency":
            required_params = ["amount", "from_currency", "to_currency"]
            missing_params = [param for param in required_params if param not in args]
            
            if missing_params:
                return JSONResponse(
                    status_code=400, 
                    content={"error": f"Missing required parameters: {', '.join(missing_params)}"}
                )
            
            return convert_currency(args["amount"], args["from_currency"], args["to_currency"])
            
        else:
            return JSONResponse(status_code=400, content={"error": f"Tool '{name}' not found"})
            
    except Exception as e:
        print(f"❌ Error in call_tool: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
