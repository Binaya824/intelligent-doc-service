from openai import OpenAI
from app.core.config import settings
class AssistantAgent:
    def __init__(self):
        self.openai = OpenAI(
                            api_key=settings.API_KEY,
                            base_url=settings.BASE_URL,
                        )
        self.model = settings.CHAT_MODEL

    def send_message(self, chunks , message: str):
        print("send_message called --------------------------",message)
        system_instruction = (
             "You are a highly specialized AI assistant for document understanding and search.\n\n"

                "Context:\n"
                "- You will receive a user query along with relevant parts (chunks) of a document.\n"
                "- You will use only these chunks to answer the user's questions.\n\n"

                "Greeting Handling:\n"
                "- If the user's first message is a greeting (e.g., 'Hi', 'Hello', 'Hey'), reply politely (e.g., 'Hello! How can I help you today?'). Do not use document chunks for this.\n\n"

                "Identity Handling:\n"
                "- If the user asks about your identity, respond exactly: 'I am an AI assistant that helps you understand and search within your documents.'\n\n"

                "General Answering Rules:\n"
                "- Use only the content from the provided document chunks.\n"
                "- Never use any external knowledge.\n"
                "- If the answer is not present in the chunks, reply: 'The answer is not available in the provided document excerpts.'\n\n"

                "Behavior When Asked to Summarize or Explain:\n"
                "- If the user asks to summarize, explain, or give an overview, generate the summary ONLY from the document chunks.\n"
                "- Do not mention which chunks were used.\n"
                "- Do not say: 'From the chunks', 'Based on the provided excerpts', 'In Chunk 2', or similar phrases.\n"
                "- Just provide the clean summary or explanation directly, as if you are speaking from full document knowledge.\n"
        )






        messages_histories = [
            {"role": "system", "content": system_instruction}
        ]
        

        context = "\n\n".join([f"Chunk {i+1}:\n{chunk}" for i, chunk in enumerate(chunks)])
        user_prompt = (
                f"User Query:\n{message}\n\n"
                f"Document Chunks:\n{context}"
            )
        messages_histories.append(
            {"role": "user", "content": user_prompt}
        )

        response = self.openai.chat.completions.create(
            model=self.model,
            messages=messages_histories
        )

        assistant_message = response.choices[0].message.content
        print("assistant_message: ****************************************************************", assistant_message)
        return assistant_message
