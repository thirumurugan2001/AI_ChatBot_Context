import os
from openai import OpenAI
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

# Initialize memory (do this once, outside the function, to persist across calls)
# Create LangChain LLM wrapper for the summary generation
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    openai_api_key=os.environ.get("GITHUB_TOKEN"),
    openai_api_base="https://models.inference.ai.azure.com"
)

# Initialize conversation summary memory
memory = ConversationSummaryMemory(llm=llm)


def openai_with_memory(question: str):
    """
    Execute OpenAI chat with conversation summary memory
    
    Args:
        question: User's input question
    
    Returns:
        str or dict: AI response or error details
    """
    try:
        # Load conversation history from memory
        chat_history = memory.load_memory_variables({})
        history_text = chat_history.get("history", "")
        
        # Initialize OpenAI client
        client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.environ.get("GITHUB_TOKEN"),
        )
        
        # Prepare system message with conversation history
        system_content = "You are a helpful assistant."
        if history_text:
            system_content += f"\n\nConversation summary so far:\n{history_text}"
        
        # Create chat completion
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_content,
                },
                {
                    "role": "user",
                    "content": question,
                }
            ],
            model="gpt-4o",
            temperature=1,
            max_tokens=4096,
            top_p=1
        )
        
        output = response.choices[0].message.content
        
        # Save the conversation to memory
        memory.save_context(
            {"input": question},
            {"output": output}
        )
        
        return output
        
    except Exception as e:
        return {
            "Error": str(e),
            "statusCode": 400
        }


# Alternative: Using ConversationBufferMemory for full chat history
def openai_with_buffer_memory(question: str):
    """
    Alternative implementation using ConversationBufferMemory
    This stores the full conversation history instead of a summary
    """
    from langchain.memory import ConversationBufferMemory
    
    # Initialize buffer memory (store full history)
    if not hasattr(openai_with_buffer_memory, 'buffer_memory'):
        openai_with_buffer_memory.buffer_memory = ConversationBufferMemory()
    
    try:
        # Load conversation history
        chat_history = openai_with_buffer_memory.buffer_memory.load_memory_variables({})
        history_text = chat_history.get("history", "")
        
        client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.environ.get("GITHUB_TOKEN"),
        )
        
        system_content = "You are a helpful assistant."
        if history_text:
            system_content += f"\n\nPrevious conversation:\n{history_text}"
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_content,
                },
                {
                    "role": "user",
                    "content": question,
                }
            ],
            model="gpt-4o",
            temperature=1,
            max_tokens=4096,
            top_p=1
        )
        
        output = response.choices[0].message.content
        
        # Save to memory
        openai_with_buffer_memory.buffer_memory.save_context(
            {"input": question},
            {"output": output}
        )
        
        return output
        
    except Exception as e:
        return {
            "Error": str(e),
            "statusCode": 400
        }


# Usage examples:
if __name__ == "__main__":
    # Example 1: Using ConversationSummaryMemory
    print("=== Using ConversationSummaryMemory ===")
    response1 = openai_with_memory("My name is Alice and I love Python programming.")
    print(f"Response 1: {response1}\n")
    
    response2 = openai_with_memory("What's my name?")
    print(f"Response 2: {response2}\n")
    
    # View the summary
    print(f"Memory Summary: {memory.buffer}\n")
    
    # Example 2: Using ConversationBufferMemory
    print("=== Using ConversationBufferMemory ===")
    response3 = openai_with_buffer_memory("Tell me about machine learning.")
    print(f"Response 3: {response3}\n")
    
    response4 = openai_with_buffer_memory("Can you elaborate on that?")
    print(f"Response 4: {response4}\n")