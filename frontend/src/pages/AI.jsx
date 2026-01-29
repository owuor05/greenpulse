import { useEffect, useRef, useState } from "react";
import { aiService } from "../services/api";

function AIPage() {
  const [messages, setMessages] = useState([]); // {role:'user'|'assistant', content:string}
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const messagesEndRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    window.scrollTo(0, 0);
    
    // Load saved conversation from localStorage
    const savedMessages = localStorage.getItem('terraGuardChat');
    if (savedMessages) {
      try {
        const parsed = JSON.parse(savedMessages);
        setMessages(parsed);
      } catch (e) {
        console.error('Failed to load saved messages:', e);
      }
    }
  }, []);

  useEffect(() => {
    if (messages.length > 0 && containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
    
    // Save conversation to localStorage whenever messages change
    if (messages.length > 0) {
      localStorage.setItem('terraGuardChat', JSON.stringify(messages));
    }
  }, [messages, loading]);

  const send = async () => {
    const q = input.trim();
    if (!q || loading) return;
    
    // Validate minimum length (backend requires 3 characters)
    if (q.length < 3) {
      setError("Please enter at least 3 characters.");
      return;
    }
    
    // Validate maximum length (backend max is 500 characters)
    if (q.length > 500) {
      setError("Question is too long. Please keep it under 500 characters.");
      return;
    }
    
    setError("");
    setLoading(true);
    setMessages((prev) => [...prev, { role: "user", content: q }]);
    setInput("");

    try {
      // Get complete response from backend
      const data = await aiService.askQuestion(q);
      const fullAnswer = data.answer;
      
      // Add empty AI message that we'll "stream"
      const aiMessageId = Date.now();
      setMessages((prev) => [
        ...prev,
        { id: aiMessageId, role: "assistant", content: "" },
      ]);
      
      setLoading(false); // Stop showing "Thinking..."
      
      // Simulate streaming by revealing words gradually
      const words = fullAnswer.split(' ');
      
      for (let i = 0; i < words.length; i++) {
        // Wait 30ms between words (adjust for speed)
        await new Promise(resolve => setTimeout(resolve, 30));
        
        // Update message with words revealed so far
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === aiMessageId
              ? { ...msg, content: words.slice(0, i + 1).join(' ') }
              : msg
          )
        );
      }
      
    } catch (e) {
      // Handle different error formats
      let errorMessage = "Something went wrong. Please try again.";
      
      if (e.response?.data?.detail) {
        const detail = e.response.data.detail;
        // FastAPI validation errors return an array
        if (Array.isArray(detail)) {
          errorMessage = detail.map(err => err.msg).join(", ");
        } else if (typeof detail === 'string') {
          errorMessage = detail;
        } else {
          errorMessage = "Invalid request. Please check your input.";
        }
      } else if (e.message) {
        errorMessage = e.message;
      }
      
      setError(errorMessage);
      setLoading(false);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError("");
    // Clear from localStorage as well
    localStorage.removeItem('terraGuardChat');
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      {/* Header */}
      <div className="bg-gradient-to-r from-emerald-600 to-green-700 text-white py-20 px-4">
        <div className="max-w-5xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-3">TerraGuard AI Assistant</h1>
          <p className="text-lg md:text-xl text-green-100">
            Your guide to land conservation, soil health, and climate-smart farming across Kenya
          </p>
        </div>
      </div>

      {/* Chat Section */}
      <div className="max-w-6xl mx-auto py-12 px-4 md:px-6">
        {/* Tools */}
        <div className="flex items-center justify-end mb-4">
          <button
            onClick={clearChat}
            className="text-sm font-semibold text-green-700 hover:text-green-800"
          >
            Clear Chat
          </button>
        </div>

        {/* Conversation */}
        <div
          ref={containerRef}
          className="bg-white border border-gray-200 rounded-xl p-6 h-[65vh] overflow-y-auto"
        >
          {messages.length === 0 && !loading && !error && (
            <div className="text-gray-500 text-center mt-20">
              <p className="text-lg mb-2">Ask me about:</p>
              <p className="text-sm">Land conservation • Soil health • Tree planting • Erosion control</p>
              <p className="text-sm">Climate-smart farming • Drought mitigation • Sustainable agriculture</p>
            </div>
          )}

          <div className="space-y-6">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={`flex ${
                  m.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[75%] ${
                    m.role === "user" ? "text-right" : "text-left"
                  }`}
                >
                  {m.role === "assistant" && (
                    <div className="text-xs text-gray-500 mb-1 px-1">
                      TerraGuard AI
                    </div>
                  )}
                  <div
                    className={`inline-block whitespace-pre-wrap ${
                      m.role === "user" ? "text-gray-900" : "text-gray-900"
                    }`}
                  >
                    {m.content}
                  </div>
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="max-w-[75%]">
                  <div className="text-xs text-gray-500 mb-1 px-1">
                    TerraGuard AI
                  </div>
                  <div className="inline-block text-gray-600">Thinking...</div>
                </div>
              </div>
            )}

            {error && (
              <div className="flex justify-center">
                <div className="text-red-700 bg-red-50 border border-red-200 rounded-lg px-4 py-3 max-w-md">
                  {error}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Input */}
        <div className="mt-4">
          <div className="flex items-end gap-3">
            <div className="flex-1">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKey}
                placeholder="Ask about land conservation, soil erosion, tree planting, drought mitigation..."
                rows={2}
                maxLength={500}
                className="w-full resize-none px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-green-600"
              />
              <div className="text-xs text-gray-500 mt-1 px-1">
                {input.length}/500 characters {input.length < 3 && input.length > 0 && "(minimum 3)"}
              </div>
            </div>
            <button
              onClick={send}
              disabled={loading || input.trim().length < 3}
              className="bg-green-700 text-white px-8 py-3 rounded-xl font-semibold hover:bg-green-800 disabled:opacity-50 h-fit"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AIPage;
