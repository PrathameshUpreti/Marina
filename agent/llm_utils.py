from config import Config
import openai
import tiktoken
import time

CFG = Config()

# Set up OpenAI client in the compatible way
openai.api_key = CFG.openai_api_key
#openai.api_base = CFG.openai_api_base

from typing import Optional

def count_tokens(text, model="gpt-3.5-turbo"):
    """Count the number of tokens in a text string."""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except:
        # Fallback: estimate tokens (1 token ~= 4 chars for English)
        return len(text) // 4

def check_token_limit(messages, model="gpt-3.5-turbo"):
    """Check if messages exceed token limit and truncate if necessary."""
    # Set limits based on model
    if "gpt-4" in model:
        limit = 6000  # Conservative limit for GPT-4 context window
    else:
        limit = 3000  # Conservative limit for GPT-3.5 context window
    
    # Count tokens in all messages
    total_tokens = 0
    for msg in messages:
        total_tokens += count_tokens(msg["content"])
    
    # Return true if within limit
    return total_tokens <= limit

def llm_response(model, 
             messages, 
             temperature: float = CFG.temperature,
             max_tokens: Optional[int] = None,
             retry_count: int = 3):
    
    # Check if current messages exceed token limit
    if not check_token_limit(messages, model):
        # If user message is too long, truncate it
        if len(messages) >= 2 and messages[-1]["role"] == "user":
            content = messages[-1]["content"]
            # Try to find a logical truncation point
            # Estimate safe length (3000 tokens ≈ 12000 chars)
            safe_length = 12000 
            if len(content) > safe_length:
                truncated = content[:safe_length]
                # Find last complete sentence
                last_period = max(truncated.rfind('.'), truncated.rfind('!'), truncated.rfind('?'))
                if last_period > 0:
                    messages[-1]["content"] = truncated[:last_period+1] + " [TRUNCATED FOR TOKEN LIMIT]"
                else:
                    messages[-1]["content"] = truncated + " [TRUNCATED FOR TOKEN LIMIT]"
                print(f"Input truncated from {len(content)} to {len(messages[-1]['content'])} characters")
    
    # Try to generate a response with retries
    for attempt in range(retry_count):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message["content"]
        except Exception as e:
            print(f"Error in LLM response: {str(e)}")
            if attempt < retry_count - 1:
                print(f"Retrying in {2 ** attempt} seconds...")
                time.sleep(2 ** attempt)
            else:
                return f"I encountered an error processing your request. Please try with a shorter or simpler query. Error: {str(e)}"


def llm_stream_response(model, 
                        messages, 
                        temperature: float = CFG.temperature, 
                        max_tokens: Optional[int] = None):
    response = ""
    
    # Ensure messages don't exceed token limit
    if not check_token_limit(messages, model):
        # Truncate user message if needed
        if len(messages) >= 2 and messages[-1]["role"] == "user":
            messages[-1]["content"] = messages[-1]["content"][:12000] + " [TRUNCATED]"
    
    try:
        for chunk in openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
        ):
            content = chunk["choices"][0]["delta"].get("content")
            if content is not None:
                response += content
                yield response
    except Exception as e:
        error_msg = f"\n\nI apologize, but I encountered an error: {str(e)}\nPlease try again with a shorter query."
        response += error_msg
        yield response


