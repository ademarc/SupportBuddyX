from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from config import get_openai_key, setup_logging
from memory import get_user_memory, save_user_memory
from langchain.callbacks import get_openai_callback
from embed_process import load_documents

# Set up environment variables
OPENAI_API_KEY = get_openai_key()

# Set up logging
logger = setup_logging()

# Initialize LLM
chat0 = ChatOpenAI(temperature=0)

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.memory = None

    def ask_question(self, question):
        try:
            with get_openai_callback() as cb:
                retriever = load_documents()
                self.memory = get_user_memory(self.user_id)
                chain = ConversationalRetrievalChain.from_llm(llm=chat0, retriever=retriever, return_source_documents=True, memory=self.memory, verbose=True)
                result = chain({"question": question}, return_only_outputs=True)
                save_user_memory(self.user_id, self.memory)
                logger.info(f'Generated response for user {self.user_id} with {cb.total_tokens} tokens')
                
                # Extract answer and source links from the result
                response = {
                    "answer": result.get("answer"),
                    "sources": list(set(doc.metadata['source'] for doc in result.get("source_documents", []) if 'source' in doc.metadata))
                }

            return response
        except Exception as e:
            logger.error(f"Failed to process question '{question}' for user {self.user_id}. Error: {str(e)}")
            return None
