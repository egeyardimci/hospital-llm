from backend.ai.llm.sgk_agent.agent import sgk_agent
from backend.web.dtos import ChatRequest, ChatResponse

class ChatService:
    @staticmethod
    def process_chat_request(request: ChatRequest) -> ChatResponse:
        """
        Process a chat request using the SGK agent.
        
        Args:
            request: ChatRequest containing llm, query, and options
            
        Returns:
            ChatResponse with the assistant's response
            
        Raises:
            Exception: If there's an error processing the chat request
        """
        result = sgk_agent(request.llm, request.query, request.options)
        return ChatResponse(role="assistant", content=result.content)