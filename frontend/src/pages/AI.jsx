import { useEffect, useRef, useState } from "react";
import { aiService } from "../services/api";
import ReactMarkdown from "react-markdown";

function AIPage() {
  const [messages, setMessages] = useState([]); // {role:'user'|'assistant', content:string}
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileError, setFileError] = useState("");
  const [processingFile, setProcessingFile] = useState(false);
  const messagesEndRef = useRef(null);
  const containerRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    window.scrollTo(0, 0);

    // Load saved conversation from localStorage
    const savedMessages = localStorage.getItem("greenPulseChat");
    if (savedMessages) {
      try {
        const parsed = JSON.parse(savedMessages);
        setMessages(parsed);
      } catch (e) {
        console.error("Failed to load saved messages:", e);
      }
    }
  }, []);

  useEffect(() => {
    if (messages.length > 0 && containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }

    // Save conversation to localStorage whenever messages change
    if (messages.length > 0) {
      localStorage.setItem("greenPulseChat", JSON.stringify(messages));
    }
  }, [messages, loading]);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    setFileError("");

    if (!file) {
      setSelectedFile(null);
      return;
    }

    // Validate file type (PDF only)
    if (file.type !== "application/pdf") {
      setFileError("Only PDF files are allowed");
      setSelectedFile(null);
      e.target.value = "";
      return;
    }

    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      setFileError("File size must be less than 10MB");
      setSelectedFile(null);
      e.target.value = "";
      return;
    }

    setSelectedFile(file);
  };

  const removeFile = () => {
    setSelectedFile(null);
    setFileError("");
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const send = async () => {
    const q = input.trim();
    if (!q || loading) return;

    if (q.length < 3) {
      setError("Please enter at least 3 characters.");
      return;
    }

    if (q.length > 500) {
      setError("Question is too long. Please keep it under 500 characters.");
      return;
    }

    console.log(
      "🤖 Sending to AI:",
      q,
      selectedFile ? `with file: ${selectedFile.name}` : "text only",
    );
    setError("");
    setFileError("");
    setLoading(true);

    // Create user message with file info if attached
    const userMessage = selectedFile
      ? `${q}\n\n📎 Analyzing document: ${selectedFile.name}`
      : q;

    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setInput("");

    // Show file processing status
    if (selectedFile) {
      setProcessingFile(true);
    }

    try {
      // Send question with optional file to AI
      console.log("📤 Calling aiService.askQuestion...");
      const data = await aiService.askQuestion(q, selectedFile);

      console.log("📥 AI response received:", data);
      setProcessingFile(false);

      // Backend returns: { success: true, answer: "...", mode: "...", ... }
      if (!data.success) {
        throw new Error(
          data.error || "AI service returned unsuccessful response",
        );
      }

      // Get the answer from response
      let fullAnswer =
        data.answer ||
        "I received your request but couldn't generate a response.";

      // If document was analyzed, add file info
      if (selectedFile && data.file_analyzed) {
        const fileInfo = data.file_analyzed;
        fullAnswer = `**📄 Document Analysis: ${fileInfo.filename}** (${fileInfo.size_mb} MB, ${fileInfo.chars_extracted} characters extracted)\n\n---\n\n${fullAnswer}`;
      }

      console.log("✅ Answer extracted, length:", fullAnswer.length);

      // Clear file after successful send
      removeFile();

      // Add empty AI message that we'll "stream"
      const aiMessageId = Date.now();
      setMessages((prev) => [
        ...prev,
        { id: aiMessageId, role: "assistant", content: "" },
      ]);

      setLoading(false);

      // Simulate streaming by revealing words gradually
      const words = fullAnswer.split(" ");

      for (let i = 0; i < words.length; i++) {
        await new Promise((resolve) => setTimeout(resolve, 25));
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === aiMessageId
              ? { ...msg, content: words.slice(0, i + 1).join(" ") }
              : msg,
          ),
        );
      }
    } catch (e) {
      console.error("❌ AI error:", e);
      setProcessingFile(false);

      let errorMessage = "Something went wrong. Please try again.";

      if (e.response?.data?.detail) {
        const detail = e.response.data.detail;
        if (Array.isArray(detail)) {
          errorMessage = detail
            .map((err) => err.msg || err.message || JSON.stringify(err))
            .join(", ");
        } else if (typeof detail === "string") {
          errorMessage = detail;
        } else {
          errorMessage = JSON.stringify(detail);
        }
      } else if (e.message) {
        errorMessage = e.message;
      }

      console.error("💬 Error message shown to user:", errorMessage);
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
    localStorage.removeItem("greenPulseChat");
  };

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  // Close fullscreen on Escape key
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === "Escape" && isFullscreen) {
        setIsFullscreen(false);
      }
    };
    window.addEventListener("keydown", handleEscape);
    return () => window.removeEventListener("keydown", handleEscape);
  }, [isFullscreen]);

  return (
    <div className="min-h-screen font-sans">
      {/* Fullscreen Overlay for Conversation */}
      {isFullscreen && (
        <div className="fixed inset-0 z-50 bg-gray-900/95 backdrop-blur-sm flex flex-col">
          {/* Fullscreen Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-700">
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-white font-semibold">
                GreenPulse AI Assistant
              </span>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-gray-400 text-sm">Press ESC to exit</span>
              <button
                onClick={clearChat}
                className="text-sm font-semibold text-gray-400 hover:text-white transition"
              >
                Clear Chat
              </button>
              <button
                onClick={toggleFullscreen}
                className="p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition"
                title="Exit fullscreen"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          </div>

          {/* Fullscreen Conversation */}
          <div className="flex-1 overflow-y-auto p-6">
            <div className="max-w-4xl mx-auto space-y-6">
              {messages.length === 0 && !loading && !error && (
                <div className="text-gray-400 text-center mt-20">
                  <p className="text-lg mb-2 font-semibold font-weight-bold">
                    Ask me about:
                  </p>
                  <p className="text-sm">
                    Land conservation • Soil health • Tree planting • Erosion
                    control
                  </p>
                  <p className="text-sm">
                    Climate-smart farming • Drought mitigation • Sustainable
                    agriculture
                  </p>
                </div>
              )}

              {messages.map((m, idx) => (
                <div
                  key={idx}
                  className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] ${m.role === "user" ? "text-right" : "text-left"}`}
                  >
                    {m.role === "assistant" && (
                      <div className="text-xs text-green-400 mb-1 px-1">
                        GreenPulse AI
                      </div>
                    )}
                    <div
                      className={`inline-block rounded-xl px-4 py-3 ${
                        m.role === "user"
                          ? "bg-green-600 text-white"
                          : "bg-gray-800 text-gray-100"
                      }`}
                    >
                      {m.role === "assistant" ? (
                        <div className="prose prose-invert prose-sm max-w-none">
                          <ReactMarkdown
                            components={{
                              h1: ({ node, ...props }) => (
                                <h1
                                  className="text-xl font-bold text-white mt-3 mb-2"
                                  {...props}
                                />
                              ),
                              h2: ({ node, ...props }) => (
                                <h2
                                  className="text-lg font-bold text-white mt-3 mb-2"
                                  {...props}
                                />
                              ),
                              h3: ({ node, ...props }) => (
                                <h3
                                  className="text-base font-semibold text-gray-200 mt-2 mb-1"
                                  {...props}
                                />
                              ),
                              p: ({ node, ...props }) => (
                                <p
                                  className="mb-2 text-gray-200 leading-relaxed"
                                  {...props}
                                />
                              ),
                              ul: ({ node, ...props }) => (
                                <ul
                                  className="list-disc list-inside mb-2 space-y-1 ml-2"
                                  {...props}
                                />
                              ),
                              ol: ({ node, ...props }) => (
                                <ol
                                  className="list-decimal list-inside mb-2 space-y-1 ml-2"
                                  {...props}
                                />
                              ),
                              li: ({ node, ...props }) => (
                                <li className="text-gray-200" {...props} />
                              ),
                              strong: ({ node, ...props }) => (
                                <strong
                                  className="font-semibold text-white"
                                  {...props}
                                />
                              ),
                              em: ({ node, ...props }) => (
                                <em className="italic" {...props} />
                              ),
                              blockquote: ({ node, ...props }) => (
                                <blockquote
                                  className="border-l-4 border-green-500 pl-3 italic text-gray-400 my-2"
                                  {...props}
                                />
                              ),
                              code: ({ node, ...props }) => (
                                <code
                                  className="bg-gray-700 px-1 py-0.5 rounded text-sm"
                                  {...props}
                                />
                              ),
                            }}
                          >
                            {m.content}
                          </ReactMarkdown>
                        </div>
                      ) : (
                        <span className="whitespace-pre-wrap">{m.content}</span>
                      )}
                    </div>
                  </div>
                </div>
              ))}

              {loading && (
                <div className="flex justify-start">
                  <div className="max-w-[80%]">
                    <div className="text-xs text-green-400 mb-1 px-1">
                      GreenPulse AI
                    </div>
                    <div className="inline-block bg-gray-800 text-gray-300 rounded-xl px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-bounce"></div>
                        <div
                          className="w-2 h-2 bg-green-500 rounded-full animate-bounce"
                          style={{ animationDelay: "0.1s" }}
                        ></div>
                        <div
                          className="w-2 h-2 bg-green-500 rounded-full animate-bounce"
                          style={{ animationDelay: "0.2s" }}
                        ></div>
                        <span className="ml-2">Thinking...</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {error && (
                <div className="flex justify-center">
                  <div className="text-red-400 bg-red-900/50 border border-red-700 rounded-lg px-4 py-3 max-w-md">
                    {error}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Fullscreen Input with File Upload */}
          <div className="border-t border-gray-700 px-6 py-4">
            <div className="max-w-4xl mx-auto">
              {/* File processing indicator */}
              {processingFile && (
                <div className="mb-3 flex items-center gap-2 p-3 bg-blue-900/50 border border-blue-700 rounded-lg">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-400"></div>
                  <span className="text-sm text-blue-300">
                    Processing document... This may take a moment.
                  </span>
                </div>
              )}

              {/* File selection feedback in fullscreen */}
              {selectedFile && !processingFile && (
                <div className="mb-3 flex items-center gap-2 p-2 bg-green-900/50 border border-green-700 rounded-lg">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-5 w-5 text-green-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  <span className="text-sm text-green-300 flex-1 truncate">
                    {selectedFile.name}
                  </span>
                  <span className="text-xs text-green-400">
                    ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                  </span>
                  <button
                    onClick={removeFile}
                    className="text-red-400 hover:text-red-300 p-1"
                    title="Remove file"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-4 w-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>
              )}
              {fileError && (
                <p className="mb-2 text-sm text-red-400">{fileError}</p>
              )}

              <div className="flex items-end gap-3">
                <div className="flex-1 relative">
                  <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKey}
                    placeholder={
                      selectedFile
                        ? "Ask a question about the attached document..."
                        : "Ask about land conservation, soil erosion, tree planting, drought mitigation..."
                    }
                    rows={2}
                    maxLength={500}
                    className="w-full resize-none px-4 py-3 pr-12 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-green-600"
                    disabled={processingFile}
                  />
                  {/* PDF Upload Button - Bottom Right of Input */}
                  <button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    className={`absolute right-3 bottom-3 p-2 rounded-lg transition ${
                      selectedFile
                        ? "text-green-600 bg-green-50"
                        : "text-gray-500 hover:text-green-600 hover:bg-green-50"
                    }`}
                    title={
                      selectedFile
                        ? "Change document"
                        : "Attach PDF document for AI analysis"
                    }
                    disabled={processingFile}
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                      />
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 9h1m4 0h1m-6 4h6m-6 4h4"
                      />
                    </svg>
                  </button>
                </div>
                <button
                  onClick={send}
                  disabled={
                    loading || processingFile || input.trim().length < 3
                  }
                  className="bg-green-700 text-white px-8 py-3 rounded-xl font-semibold hover:bg-green-800 disabled:opacity-50 h-fit"
                >
                  {processingFile
                    ? "Processing..."
                    : loading
                      ? "Sending..."
                      : "Send"}
                </button>
              </div>
              <div className="text-xs text-green-200 mt-1 px-1">
                {input.length}/500 characters{" "}
                {input.length < 3 && input.length > 0 && "(minimum 3)"}
                {selectedFile
                  ? " • Document attached - AI will analyze its content"
                  : " • Attach a PDF for AI document analysis"}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Header - White to Green radial */}
      <section className="relative py-20 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(ellipse 120% 80% at 0% 0%, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0.95) 20%, rgba(255, 255, 255, 0.7) 40%, rgba(34, 197, 94, 0.75) 55%, rgba(5, 150, 105, 0.9) 70%, rgb(4, 120, 87) 100%)",
          }}
        ></div>
        <div className="relative max-w-5xl mx-auto text-center z-10">
          <h1 className="text-5xl md:text-6xl font-bold mb-3 text-black drop-shadow-lg">
            GreenPulse AI Assistant
          </h1>
          <p className="text-lg md:text-xl text-green-100 drop-shadow">
            Accepts industry reports and operational data. Answers “what if”
            questions about planned actions. Predicts environmental impact.
            Ensures regulatory compliance. Suggests mitigation strategies and
            alternative energy options. Helps businesses understand future
            environmental conditions of an area.
          </p>
        </div>
      </section>

      {/* Chat Section - Original dimensions preserved */}
      <section className="relative py-12 px-4 md:px-6 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(135deg, rgb(4, 120, 87) 0%, rgb(2, 80, 60) 25%, rgb(1, 50, 40) 50%, rgb(10, 30, 25) 75%, rgb(5, 15, 12) 100%)",
          }}
        ></div>
        <div className="relative max-w-6xl mx-auto z-10">
          {/* Tools */}
          <div className="flex items-center justify-end mb-4 gap-4">
            <button
              onClick={clearChat}
              className="text-sm font-semibold text-green-200 hover:text-white"
            >
              Clear Chat
            </button>
          </div>

          {/* Conversation Container */}
          <div className="relative">
            {/* Fullscreen Toggle Button - positioned on the top-left of conversation box */}
            <button
              onClick={toggleFullscreen}
              className="absolute top-3 left-3 z-10 p-2 text-gray-500 hover:text-green-600 hover:bg-green-50 rounded-lg transition"
              title="Expand to fullscreen"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3.75 3.75v4.5m0-4.5h4.5m-4.5 0L9 9M3.75 20.25v-4.5m0 4.5h4.5m-4.5 0L9 15M20.25 3.75h-4.5m4.5 0v4.5m0-4.5L15 9m5.25 11.25h-4.5m4.5 0v-4.5m0 4.5L15 15"
                />
              </svg>
            </button>

            {/* Conversation */}
            <div
              ref={containerRef}
              className="bg-white/95 backdrop-blur-sm border border-gray-200 rounded-xl p-6 pl-12 h-[65vh] overflow-y-auto"
            >
              {messages.length === 0 && !loading && !error && (
                <div className="text-gray-500 text-center mt-20">
                  <p className="text-lg mb-2">Ask me about:</p>
                  <p className="text-sm">
                    Land conservation • Soil health • Tree planting • Erosion
                    control
                  </p>
                  <p className="text-sm">
                    Climate-smart farming • Drought mitigation • Sustainable
                    agriculture
                  </p>
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
                          Greenpulse AI
                        </div>
                      )}
                      <div
                        className={`inline-block ${
                          m.role === "user" ? "text-gray-900" : "text-gray-900"
                        }`}
                      >
                        {m.role === "assistant" ? (
                          <div className="prose prose-sm max-w-none">
                            <ReactMarkdown
                              components={{
                                h1: ({ node, ...props }) => (
                                  <h1
                                    className="text-xl font-bold text-gray-900 mt-3 mb-2"
                                    {...props}
                                  />
                                ),
                                h2: ({ node, ...props }) => (
                                  <h2
                                    className="text-lg font-bold text-gray-900 mt-3 mb-2"
                                    {...props}
                                  />
                                ),
                                h3: ({ node, ...props }) => (
                                  <h3
                                    className="text-base font-semibold text-gray-800 mt-2 mb-1"
                                    {...props}
                                  />
                                ),
                                p: ({ node, ...props }) => (
                                  <p
                                    className="mb-2 text-gray-700 leading-relaxed"
                                    {...props}
                                  />
                                ),
                                ul: ({ node, ...props }) => (
                                  <ul
                                    className="list-disc list-inside mb-2 space-y-1 ml-2"
                                    {...props}
                                  />
                                ),
                                ol: ({ node, ...props }) => (
                                  <ol
                                    className="list-decimal list-inside mb-2 space-y-1 ml-2"
                                    {...props}
                                  />
                                ),
                                li: ({ node, ...props }) => (
                                  <li className="text-gray-700" {...props} />
                                ),
                                strong: ({ node, ...props }) => (
                                  <strong
                                    className="font-semibold text-gray-900"
                                    {...props}
                                  />
                                ),
                                em: ({ node, ...props }) => (
                                  <em className="italic" {...props} />
                                ),
                                blockquote: ({ node, ...props }) => (
                                  <blockquote
                                    className="border-l-4 border-green-500 pl-3 italic text-gray-600 my-2"
                                    {...props}
                                  />
                                ),
                                code: ({ node, ...props }) => (
                                  <code
                                    className="bg-gray-100 px-1 py-0.5 rounded text-sm"
                                    {...props}
                                  />
                                ),
                              }}
                            >
                              {m.content}
                            </ReactMarkdown>
                          </div>
                        ) : (
                          <span className="whitespace-pre-wrap">
                            {m.content}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}

                {loading && (
                  <div className="flex justify-start">
                    <div className="max-w-[75%]">
                      <div className="text-xs text-gray-500 mb-1 px-1">
                        GreenPulse
                      </div>
                      <div className="inline-block text-gray-600">
                        Thinking...
                      </div>
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
          </div>

          {/* Input with File Upload */}
          <div className="mt-4">
            {/* File processing indicator */}
            {processingFile && (
              <div className="mb-3 flex items-center gap-2 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                <span className="text-sm text-blue-700">
                  📄 Analyzing your document... The AI is reading and processing
                  the content. This may take a moment.
                </span>
              </div>
            )}

            {/* File selection feedback */}
            {selectedFile && !processingFile && (
              <div className="mb-3 flex items-center gap-2 p-2 bg-green-50 border border-green-200 rounded-lg">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5 text-green-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
                <span className="text-sm text-green-700 flex-1 truncate">
                  📎 {selectedFile.name} - Ready to analyze
                </span>
                <span className="text-xs text-green-600">
                  ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                </span>
                <button
                  type="button"
                  onClick={removeFile}
                  className="text-red-500 hover:text-red-700 p-1"
                  title="Remove file"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
            )}

            {/* File error message */}
            {fileError && (
              <p className="mb-2 text-sm text-red-400">{fileError}</p>
            )}

            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,application/pdf"
              onChange={handleFileSelect}
              className="hidden"
            />

            <div className="flex items-end gap-3">
              <div className="flex-1 relative">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKey}
                  placeholder={
                    selectedFile
                      ? "Ask a question about the attached document..."
                      : "Ask about land conservation, soil erosion, tree planting, drought mitigation..."
                  }
                  rows={2}
                  maxLength={500}
                  className="w-full resize-none px-4 py-3 pr-12 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-green-600"
                  disabled={processingFile}
                />
                {/* PDF Upload Button - Bottom Right of Input */}
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className={`absolute right-3 bottom-3 p-2 rounded-lg transition ${
                    selectedFile
                      ? "text-green-600 bg-green-50"
                      : "text-gray-500 hover:text-green-600 hover:bg-green-50"
                  }`}
                  title={
                    selectedFile
                      ? "Change document"
                      : "Attach PDF document for AI analysis"
                  }
                  disabled={processingFile}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 9h1m4 0h1m-6 4h6m-6 4h4"
                    />
                  </svg>
                </button>
              </div>
              <button
                onClick={send}
                disabled={loading || processingFile || input.trim().length < 3}
                className="bg-green-700 text-white px-8 py-3 rounded-xl font-semibold hover:bg-green-800 disabled:opacity-50 h-fit"
              >
                {processingFile
                  ? "Processing..."
                  : loading
                    ? "Sending..."
                    : "Send"}
              </button>
            </div>
            <div className="text-xs text-green-200 mt-1 px-1">
              {input.length}/500 characters{" "}
              {input.length < 3 && input.length > 0 && "(minimum 3)"}
              {selectedFile
                ? " • Document attached - AI will analyze its content"
                : " • Attach a PDF for AI document analysis"}
            </div>
          </div>
        </div>
      </section>

      {/* Info Section - Dark to Green radial */}
      <section className="relative py-16 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(ellipse 120% 120% at 100% 100%, rgb(4, 120, 87) 0%, rgba(5, 150, 105, 0.9) 20%, rgba(22, 163, 74, 0.8) 35%, rgb(10, 30, 25) 55%, rgb(5, 15, 12) 70%, rgb(0, 0, 0) 100%)",
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto text-center z-10">
          <h2 className="text-3xl font-bold mb-4 text-white">
            AI-Powered Conservation Guidance
          </h2>
          <p className="text-xl text-gray-200 mb-8">
            Get instant answers to your land conservation questions from our
            advanced AI assistant
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-4xl font-bold text-green-400 mb-2">24/7</div>
              <p className="text-green-100">Always Available</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-400 mb-2">Free</div>
              <p className="text-green-100">No Cost Ever</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-400 mb-2">
                Expert
              </div>
              <p className="text-green-100">Knowledge Base</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA - Green to White radial */}
      <section className="relative py-16 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(ellipse 120% 120% at 100% 100%, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0.9) 15%, rgba(255, 255, 255, 0.6) 30%, rgba(34, 197, 94, 0.7) 45%, rgba(5, 150, 105, 0.85) 60%, rgb(4, 120, 87) 80%, rgb(2, 80, 60) 100%)",
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto text-center z-10">
          <h2 className="text-3xl font-bold mb-4 text-white drop-shadow-lg">
            Prefer Messaging Apps?
          </h2>
          <p className="text-xl mb-8 text-green-100 drop-shadow">
            Chat with our AI assistant on Telegram or WhatsApp
          </p>
          <a
            href="https://t.me/TerraGuard_Bot"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-white text-green-700 px-10 py-4 rounded-lg font-bold text-lg hover:bg-green-50 transition shadow-lg"
          >
            Open Telegram Bot
          </a>
        </div>
      </section>
    </div>
  );
}

export default AIPage;
