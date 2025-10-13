import os
from openai import OpenAI
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("MODEL"),
    temperature=0,
    openai_api_key=os.getenv("API_KEY"),
    openai_api_base=os.getenv("API_BASE_URL")
)
memory = ConversationSummaryMemory(llm=llm)

def ConnectChatBot(data: str):
    try:
        print(data["Question"])
        if not isinstance(data["Question"], str):
            return {
                "Error": "Question must be a string",
                "statusCode": 400
            }
        
        chat_history = memory.load_memory_variables({})
        history_text = chat_history.get("history", "")
        client = OpenAI(
            base_url=os.getenv("API_BASE_URL"),
            api_key=os.getenv("API_KEY"),
        )        
        system_content = "You are a helpful assistant."
        if history_text:
            system_content += f"\n\nConversation summary so far:\n{history_text}"
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_content,
                },
                {
                    "role": "user",
                    "content": data['Question'], 
                }
            ],
            model=os.getenv("MODEL"),
            temperature=1,
            max_tokens=4096,
            top_p=1
        )
        output = response.choices[0].message.content
        memory.save_context(
            {"input": data['Question']},
            {"output": output}
        )
        return output
    except Exception as e:
        return {
            "Error": str(e),
            "statusCode": 400
        }