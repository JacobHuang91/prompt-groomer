# Packer Examples

These examples demonstrate how to use MessagesPacker and TextPacker with real LLM APIs.

## Setup

1. **Install dependencies:**
   ```bash
   pip install llm-prompt-refiner[token] openai python-dotenv
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

   The examples use `python-dotenv` to automatically load variables from the `.env` file.

## Running Examples

### MessagesPacker (Chat Completion APIs)
```bash
python messages_packer.py
```

Demonstrates:
- Priority-based message packing
- RAG document integration
- Conversation history management
- Real OpenAI Chat Completions API call

### TextPacker (Text Completion APIs)
```bash
python text_packer.py
```

Demonstrates:
- MARKDOWN format for base models
- Priority-based content selection
- Real OpenAI Completions API call
- Structured prompt generation

## Get Your API Key

Visit [OpenAI Platform](https://platform.openai.com/api-keys) to create an API key.
