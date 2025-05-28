
# Agentic System with MCP (Model Context Protocol)

## Overview

This project implements an intelligent agentic system that leverages the Model Context Protocol (MCP) to provide tool-calling capabilities to Large Language Models (LLMs). The system consists of an agent runner that communicates with a local LLM and an MCP server that exposes utility tools for weather information and currency conversion.

## Architecture

The system follows a modular architecture with three main components:

### 1. Agent Runner
The agent runner serves as the main orchestrator that manages conversations with the LLM and coordinates tool execution. It dynamically fetches tool schemas from the MCP server and handles the complete conversation flow including tool calling and response generation.

### 2. MCP Server
A FastAPI-based server that implements the Model Context Protocol, exposing tools through standardized REST endpoints.The server provides:
- Tool discovery endpoint for listing available tools
- Tool execution endpoint for calling specific tools
- Plugin manifest for AI integration

### 3. Tool Suite
Currently includes two utility tools:
- **Weather Tool**: Fetches current weather information for specified cities
- **Currency Converter**: Performs real-time currency conversion between different currencies

## Features

- **Dynamic Tool Discovery**: The agent automatically fetches available tools from the MCP server
- **Conversation History**: Maintains context across multiple interactions
- **Error Handling**: Robust error handling for API calls and tool execution  
- **Real-time Data**: Integration with external APIs for live weather and currency data
- **Extensible Architecture**: Easy to add new tools by extending the tools directory

## Configuration

### Environment Variables

The system requires several environment variables for proper operation:

- `LOCAL_LLM_API_KEY`: API key for the local LLM service 
- `WEATHER_API_KEY`: API key for WeatherAPI service 
- `EXCHANGE_API_KEY`: API key for ExchangeRate-API service

### System Configuration

- **LLM Endpoint**: Configured to use a local LLM service 
- **Model**: Uses Llama 3.3 model 
- **MCP Server**: Runs on localhost:8000

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
The agent runner provides an interactive command-line interface where users can ask questions and request tool usage. 

Example interactions:
- "What's the weather in London?"
- "Convert 100 USD to EUR"
- "How much is 50 GBP in Japanese Yen?"

### Tool Execution Flow

1. User input is processed by the agent runner
2. The LLM determines if tool usage is required
3. If tools are needed, the agent fetches available tools from MCP server
4. Tool is executed via the MCP server 
5. Results are integrated back into the conversation
6. Final response is generated and returned to the user

## API Reference

### MCP Server Endpoints

#### GET `/tools/list`
Returns the list of available tools with their schemas.

#### POST `/tools/call`
Executes a specific tool with provided arguments.  

#### GET `/.well-known/ai-plugin.json`
Provides plugin manifest for AI integration. 

### Available Tools

#### Weather Tool
- **Function**: `getWeather`
- **Parameters**: `city` (string)
- **Description**: Fetches current weather information 

#### Currency Converter
- **Function**: `convertCurrency`
- **Parameters**: `amount` (number), `from_currency` (string), `to_currency` (string)
- **Description**: Converts currency amounts between different currencies  

## External Dependencies

The system integrates with the following external services:

- **WeatherAPI**: For real-time weather data
- **ExchangeRate-API**: For currency conversion rates
- **Local LLM Service**: For natural language processing and reasoning

## Error Handling

The system includes comprehensive error handling:
- API key validation and missing parameter detection
- External API error handling 
- Tool execution error handling with detailed error messages

## Notes

This project demonstrates a practical implementation of the Model Context Protocol for building agentic AI systems. The modular architecture allows for easy extension with additional tools, and the MCP protocol ensures standardized communication between the agent and tool providers. The system is designed to be production-ready with proper error handling, logging, and API integration patterns.
