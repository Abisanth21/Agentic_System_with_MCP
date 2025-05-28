



# Agentic System with MCP (Model Context Protocol)

## Overview

This project implements an intelligent agentic system that leverages the Model Context Protocol (MCP) to provide tool-calling capabilities to Large Language Models (LLMs). The system consists of an agent runner that communicates with a local LLM and an MCP server that exposes utility tools for weather information and currency conversion.

## Architecture

The system follows a modular architecture with three main components:

### 1. Agent Runner
The agent runner serves as the main orchestrator that manages conversations with the LLM and coordinates tool execution. [1](#0-0)  It dynamically fetches tool schemas from the MCP server and handles the complete conversation flow including tool calling and response generation.

### 2. MCP Server
A FastAPI-based server that implements the Model Context Protocol, exposing tools through standardized REST endpoints. [2](#0-1)  The server provides:
- Tool discovery endpoint for listing available tools
- Tool execution endpoint for calling specific tools
- Plugin manifest for AI integration

### 3. Tool Suite
Currently includes two utility tools:
- **Weather Tool**: Fetches current weather information for specified cities
- **Currency Converter**: Performs real-time currency conversion between different currencies

## Features

- **Dynamic Tool Discovery**: The agent automatically fetches available tools from the MCP server [3](#0-2) 
- **Conversation History**: Maintains context across multiple interactions [4](#0-3) 
- **Error Handling**: Robust error handling for API calls and tool execution [5](#0-4) 
- **Real-time Data**: Integration with external APIs for live weather and currency data
- **Extensible Architecture**: Easy to add new tools by extending the tools directory

## Configuration

### Environment Variables

The system requires several environment variables for proper operation:

- `LOCAL_LLM_API_KEY`: API key for the local LLM service [6](#0-5) 
- `WEATHER_API_KEY`: API key for WeatherAPI service [7](#0-6) 
- `EXCHANGE_API_KEY`: API key for ExchangeRate-API service [8](#0-7) 

### System Configuration

- **LLM Endpoint**: Configured to use a local LLM service [9](#0-8) 
- **Model**: Uses Llama 3.3 model [10](#0-9) 
- **MCP Server**: Runs on localhost:8000 [11](#0-10) 

## Installation & Setup

### Prerequisites
- Python 3.7+
- FastAPI
- Requests library
- API keys for WeatherAPI and ExchangeRate-API

### Running the System

1. **Start the MCP Server**:
   ```bash
   uvicorn mcp_server:app --host 0.0.0.0 --port 8000
   ```

2. **Run the Agent**:
   ```bash
   python agent_runner.py
   ```

## Usage

### Interactive Mode
The agent runner provides an interactive command-line interface where users can ask questions and request tool usage. [12](#0-11) 

Example interactions:
- "What's the weather in London?"
- "Convert 100 USD to EUR"
- "How much is 50 GBP in Japanese Yen?"

### Tool Execution Flow

1. User input is processed by the agent runner
2. The LLM determines if tool usage is required
3. If tools are needed, the agent fetches available tools from MCP server [13](#0-12) 
4. Tool is executed via the MCP server [14](#0-13) 
5. Results are integrated back into the conversation
6. Final response is generated and returned to the user

## API Reference

### MCP Server Endpoints

#### GET `/tools/list`
Returns the list of available tools with their schemas. [15](#0-14) 

#### POST `/tools/call`
Executes a specific tool with provided arguments. [16](#0-15) 

#### GET `/.well-known/ai-plugin.json`
Provides plugin manifest for AI integration. [17](#0-16) 

### Available Tools

#### Weather Tool
- **Function**: `getWeather`
- **Parameters**: `city` (string)
- **Description**: Fetches current weather information [18](#0-17) 

#### Currency Converter
- **Function**: `convertCurrency`
- **Parameters**: `amount` (number), `from_currency` (string), `to_currency` (string)
- **Description**: Converts currency amounts between different currencies [19](#0-18) 

## File Structure

```
Abisanth21/Agentic_System_with_MCP/
├── agent_runner.py          # Main agent orchestrator
├── mcp_server.py            # FastAPI MCP server
└── tools/
    ├── get_weather.py       # Weather fetching tool
    └── convert_currency.py  # Currency conversion tool
```

## External Dependencies

The system integrates with the following external services:

- **WeatherAPI**: For real-time weather data [20](#0-19) 
- **ExchangeRate-API**: For currency conversion rates [21](#0-20) 
- **Local LLM Service**: For natural language processing and reasoning

## Error Handling

The system includes comprehensive error handling:
- API key validation and missing parameter detection [22](#0-21) 
- External API error handling [23](#0-22) 
- Tool execution error handling with detailed error messages

## Notes

This project demonstrates a practical implementation of the Model Context Protocol for building agentic AI systems. The modular architecture allows for easy extension with additional tools, and the MCP protocol ensures standardized communication between the agent and tool providers. The system is designed to be production-ready with proper error handling, logging, and API integration patterns.
