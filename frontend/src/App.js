import React, { useState, useRef, useEffect } from 'react';
import { Send, FileText, Loader2, Upload, CheckCircle, AlertCircle, Sparkles, Bot, User } from 'lucide-react';

export default function RAGChatUI() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    console.log('Selected file:', file.name, 'Size:', file.size, 'Type:', file.type);

    if (!file.name.endsWith('.pdf')) {
      setUploadStatus({ type: 'error', message: 'Please upload a PDF file' });
      return;
    }

    setIsUploading(true);
    setUploadStatus({ type: 'loading', message: `Uploading ${file.name}...` });

    try {
      const formData = new FormData();
      formData.append('file', file);

      console.log('Sending request to: http://127.0.0.1:8000/uploadfile');
      console.log('FormData entries:', Array.from(formData.entries()));

      const response = await fetch('http://127.0.0.1:8000/uploadfile', {
        method: 'POST',
        body: formData,
      });

      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error response body:', errorText);
        throw new Error(`Upload failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log('Success response:', data);
      
      setUploadStatus({ 
        type: 'success', 
        message: `${data.filename} uploaded successfully! You can now chat about it.` 
      });

      setTimeout(() => setUploadStatus(null), 5000);
    } catch (error) {
      console.error('Full error object:', error);
      console.error('Error message:', error.message);
      console.error('Error stack:', error.stack);
      
      setUploadStatus({ 
        type: 'error', 
        message: `Failed: ${error.message}` 
      });
    } finally {
      setIsUploading(false);
      e.target.value = '';
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          session_id: sessionId,
          message: input
        }),
      });

      if (!response.ok) throw new Error('Failed to get response');

      const data = await response.json();
      
      const assistantMessage = { 
        role: 'assistant', 
        content: data.response || 'No response received'
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please make sure the backend server is running on http://127.0.0.1:8000',
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        <div className="absolute top-40 right-20 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse delay-700"></div>
        <div className="absolute bottom-20 left-1/2 w-72 h-72 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse delay-1000"></div>
      </div>

      {/* Header */}
      <div className="relative backdrop-blur-xl bg-white/10 border-b border-white/20 px-6 py-5 shadow-2xl">
        <div className="max-w-5xl mx-auto">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-gradient-to-br from-purple-500 to-blue-600 rounded-2xl shadow-lg">
                <Sparkles className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white bg-gradient-to-r from-purple-200 to-blue-200 bg-clip-text text-transparent">
                  DocInsight
                </h1>
                <p className="text-sm text-purple-200/80">Powered by AI • Ask anything about your documents</p>
              </div>
            </div>
            
            {/* Upload Button */}
            <div>
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                onChange={handleFileUpload}
                className="hidden"
              />
              <button
                onClick={() => fileInputRef.current?.click()}
                disabled={isUploading}
                className="group relative flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-600 text-white rounded-xl hover:from-purple-600 hover:to-blue-700 disabled:from-gray-500 disabled:to-gray-600 disabled:cursor-not-allowed transition-all duration-300 shadow-lg hover:shadow-purple-500/50 hover:scale-105"
              >
                <Upload className="w-5 h-5 group-hover:rotate-12 transition-transform" />
                <span className="font-semibold">{isUploading ? 'Uploading...' : 'Upload PDF'}</span>
              </button>
            </div>
          </div>

          {/* Upload Status */}
          {uploadStatus && (
            <div className={`mt-4 px-5 py-3 rounded-xl flex items-center gap-3 backdrop-blur-lg transition-all duration-300 ${
              uploadStatus.type === 'success' ? 'bg-green-500/20 text-green-100 border border-green-400/30' :
              uploadStatus.type === 'error' ? 'bg-red-500/20 text-red-100 border border-red-400/30' :
              'bg-blue-500/20 text-blue-100 border border-blue-400/30'
            }`}>
              {uploadStatus.type === 'success' && <CheckCircle className="w-5 h-5 flex-shrink-0" />}
              {uploadStatus.type === 'error' && <AlertCircle className="w-5 h-5 flex-shrink-0" />}
              {uploadStatus.type === 'loading' && <Loader2 className="w-5 h-5 animate-spin flex-shrink-0" />}
              <span className="text-sm font-medium">{uploadStatus.message}</span>
            </div>
          )}
        </div>
      </div>

      {/* Messages Container */}
      <div className="relative flex-1 overflow-y-auto px-4 py-8">
        <div className="max-w-4xl mx-auto space-y-6">
          {messages.length === 0 && (
            <div className="text-center text-purple-100/60 mt-32 space-y-6">
              <div className="relative inline-block">
                <div className="absolute inset-0 bg-purple-500 rounded-full blur-2xl opacity-30 animate-pulse"></div>
                <FileText className="relative w-20 h-20 mx-auto text-purple-300" />
              </div>
              <div>
                <p className="text-2xl font-semibold text-white mb-2">Welcome to RAG Assistant</p>
                <p className="text-lg text-purple-200/70">Upload a PDF and start an intelligent conversation</p>
              </div>
              <div className="flex justify-center gap-4 mt-8">
                <div className="backdrop-blur-lg bg-white/5 border border-white/10 rounded-xl px-6 py-4 text-left max-w-xs">
                  <p className="text-purple-200 font-medium mb-1">📄 Step 1</p>
                  <p className="text-purple-200/70 text-sm">Upload your PDF document</p>
                </div>
                <div className="backdrop-blur-lg bg-white/5 border border-white/10 rounded-xl px-6 py-4 text-left max-w-xs">
                  <p className="text-purple-200 font-medium mb-1">💬 Step 2</p>
                  <p className="text-purple-200/70 text-sm">Ask questions about the content</p>
                </div>
              </div>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}
            >
              {msg.role === 'assistant' && (
                <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center shadow-lg">
                  <Bot className="w-6 h-6 text-white" />
                </div>
              )}
              
              <div
                className={`max-w-2xl rounded-2xl px-5 py-4 shadow-xl transition-all duration-300 hover:scale-[1.02] ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-br from-purple-500 to-blue-600 text-white'
                    : msg.isError
                    ? 'backdrop-blur-lg bg-red-500/20 text-red-100 border border-red-400/30'
                    : 'backdrop-blur-lg bg-white/10 text-white border border-white/20'
                }`}
              >
                <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
              </div>

              {msg.role === 'user' && (
                <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg">
                  <User className="w-6 h-6 text-white" />
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-3 justify-start animate-fadeIn">
              <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center shadow-lg">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div className="backdrop-blur-lg bg-white/10 text-white border border-white/20 rounded-2xl px-5 py-4 shadow-xl">
                <div className="flex items-center gap-2">
                  <Loader2 className="w-5 h-5 animate-spin text-purple-300" />
                  <span className="text-purple-200">Thinking...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="relative backdrop-blur-xl bg-white/10 border-t border-white/20 px-4 py-6 shadow-2xl">
        <div className="max-w-4xl mx-auto">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={isLoading}
              className="flex-1 px-6 py-4 backdrop-blur-lg bg-white/10 border border-white/20 text-white placeholder-purple-200/50 rounded-2xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 shadow-lg"
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className="group px-6 py-4 bg-gradient-to-r from-purple-500 to-blue-600 text-white rounded-2xl hover:from-purple-600 hover:to-blue-700 disabled:from-gray-500 disabled:to-gray-600 disabled:cursor-not-allowed transition-all duration-300 flex items-center gap-2 shadow-lg hover:shadow-purple-500/50 hover:scale-105"
            >
              <Send className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              <span className="font-semibold">Send</span>
            </button>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out;
        }
      `}</style>
    </div>
  );
}