import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

type SearchType = 'search' | 'research';

interface Message {
  type: 'user' | 'bot';
  content: string;
  searchType?: SearchType;
  model?: string;
}

interface Model {
  id: string;
  name: string;
  icon: string;
  description: string;
  gradient: string;
}

interface CodeProps {
  inline?: boolean;
  className?: string;
  
  [key: string]: any;  
}

const getSearchTypeLabel = (type: SearchType): string => {
  switch(type) {
    case 'search': return '🔍 Quick Search';
    case 'research': return '📚 Deep Research';
    default: return '🔍 Quick Search';
  }
};

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState('gpt3.5');
  const [searchType, setSearchType] = useState<SearchType>('search');
  const [isModelDropdownOpen, setIsModelDropdownOpen] = useState(false);
  const modelDropdownRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Define available models for each search type
  const modelsByType: Record<SearchType, Model[]> = {
    search: [
      { 
        id: 'gpt3.5', 
        name: 'GPT-3.5 Turbo : OpenAI',
        icon: '🤖',
        description: 'Fast and reliable for everyday tasks',
        gradient: 'from-blue-500 to-purple-600'
      },
      { 
        id: 'bedrock', 
        name: 'Claude-3-Sonnet : AWS',
        icon: '🌟',
        description: 'Advanced reasoning and analysis',
        gradient: 'from-orange-500 to-pink-600'
      },
      { 
        id: 'openrouter', 
        name: 'Deepseek R1 : OpenRouter',
        icon: '🔍',
        description: 'Balanced performance and efficiency',
        gradient: 'from-green-500 to-teal-600'
      }
    ],
    research: [
      { 
        id: 'gpt3.5', 
        name: 'GPT-3.5 Turbo : OpenAI',
        icon: '🤖',
        description: 'Research and analysis',
        gradient: 'from-blue-500 to-purple-600'
      }
    ]
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Update selected model when search type changes
  useEffect(() => {
    const availableModels = modelsByType[searchType];
    if (!availableModels.find(m => m.id === selectedModel)) {
      setSelectedModel(availableModels[0].id);
    }
  }, [searchType, selectedModel]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (modelDropdownRef.current && !modelDropdownRef.current.contains(event.target as Node)) {
        setIsModelDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { 
      type: 'user', 
      content: userMessage,
      searchType,
      model: selectedModel
    }]);
    setIsLoading(true);

    try {
      let endpoint = searchType === 'research' ? '/reason' : '/search';

      const response = await fetch(`http://localhost:5000${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query: userMessage,
          model: selectedModel
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setMessages(prev => [...prev, { 
        type: 'bot', 
        content: data.response,
        searchType,
        model: selectedModel
      }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        type: 'bot', 
        content: 'Sorry, there was an error processing your request. Please try again.',
        searchType,
        model: selectedModel
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-white">
      <header className="flex items-center justify-between p-4 bg-white border-b border-gray-200">
        <div className="flex items-center gap-4">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-[#10a37f] to-[#0e9279] flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <span className="text-lg font-semibold text-gray-800">Marina AI</span>
          </div>

          {/* Divider */}
          <div className="h-6 w-px bg-gray-200"></div>

          {/* Model Selector */}
          <div className="relative" ref={modelDropdownRef}>
            <button
              onClick={() => setIsModelDropdownOpen(!isModelDropdownOpen)}
              className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <span className="flex items-center gap-2">
                {modelsByType[searchType].find(m => m.id === selectedModel)?.name || 'Select Model'}
                <svg className={`w-4 h-4 text-gray-400 transition-transform duration-200 ${
                  isModelDropdownOpen ? 'rotate-180' : ''
                }`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </span>
            </button>

            {isModelDropdownOpen && (
              <div className="absolute left-0 mt-2 w-72 bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden z-10">
                <div className="p-2 space-y-1">
                  {modelsByType[searchType].map((model) => (
                    <div 
                      key={model.id}
                      className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer hover:bg-gray-50 group ${
                        selectedModel === model.id ? 'bg-gray-50' : ''
                      }`}
                      onClick={() => {
                        setSelectedModel(model.id);
                        setIsModelDropdownOpen(false);
                      }}
                    >
                      <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${model.gradient} flex items-center justify-center text-white`}>
                        <span className="text-lg">{model.icon}</span>
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium text-gray-900">{model.name}</span>
                          {selectedModel === model.id && (
                            <svg className="w-4 h-4 text-[#10a37f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                            </svg>
                          )}
                        </div>
                        <p className="text-xs text-gray-500">{model.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="max-w-xl">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">Marina AI Assistant</h1>
              <p className="text-lg text-gray-600 mb-8">Ask anything or explore topics in depth.</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl border border-gray-200 bg-white shadow-sm hover:border-gray-300 transition-colors">
                  <div className="text-2xl mb-2">🔍</div>
                  <h2 className="text-lg font-medium mb-2">Quick Search</h2>
                  <p className="text-sm text-gray-600">Get instant answers to your questions</p>
                </div>
                <div className="p-4 rounded-xl border border-gray-200 bg-white shadow-sm hover:border-gray-300 transition-colors">
                  <div className="text-2xl mb-2">📚</div>
                  <h2 className="text-lg font-medium mb-2">Deep Research</h2>
                  <p className="text-sm text-gray-600">Comprehensive analysis and insights</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex gap-4 ${
              message.type === 'user' ? 'flex-row-reverse' : ''
            }`}
          >
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                message.type === 'user'
                  ? 'bg-gradient-to-br from-[#10a37f] to-[#0e9279]'
                  : 'bg-gradient-to-br from-[#3b82f6] to-[#2563eb]'
              }`}
            >
              {message.type === 'user' ? (
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              ) : (
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              )}
            </div>
            <div
              className={`group relative max-w-[85%] sm:max-w-[75%] md:max-w-[65%] ${
                message.type === 'user' ? 'items-end' : 'items-start'
              }`}
            >
              <div className={`flex items-center gap-2 mb-1 text-xs text-gray-500 ${
                message.type === 'user' ? 'justify-end' : 'justify-start'
              }`}>
                <span className="px-2 py-0.5 rounded-full bg-gray-100 font-medium">
                  {message.searchType ? getSearchTypeLabel(message.searchType) : getSearchTypeLabel('search')}
                </span>
              </div>
              <div
                className={`relative p-5 rounded-2xl shadow-sm ${
                  message.type === 'user'
                    ? 'bg-[#10a37f]/5 text-gray-800'
                    : 'bg-white text-gray-800'
                }`}
              >
                {message.type === 'user' ? (
                  <p className="text-sm">{message.content}</p>
                ) : (
                  <div className="prose prose-sm max-w-none">
                    <ReactMarkdown 
                      remarkPlugins={[remarkGfm]}
                      components={{
                        p: ({children}) => <p className="mb-4 last:mb-0">{children}</p>,
                        h1: ({children}) => <h1 className="text-2xl font-bold mb-4">{children}</h1>,
                        h2: ({children}) => <h2 className="text-xl font-bold mb-3">{children}</h2>,
                        h3: ({children}) => <h3 className="text-lg font-bold mb-2">{children}</h3>,
                        ul: ({children}) => <ul className="list-disc list-inside mb-4">{children}</ul>,
                        ol: ({children}) => <ol className="list-decimal list-inside mb-4">{children}</ol>,
                        li: ({children}) => <li className="mb-1">{children}</li>,
                        code: ({inline, className, children}: CodeProps) => {
                          const match = /language-(\w+)/.exec(className || '');
                          return inline ? (
                            <code className="bg-gray-100 rounded px-1 py-0.5">
                              {children}
                            </code>
                          ) : (
                            <code className={`block bg-gray-100 rounded p-2 mb-4 overflow-x-auto ${match ? `language-${match[1]}` : ''}`}>
                              {children}
                            </code>
                          );
                        },
                        pre: ({children}) => <pre className="bg-gray-100 rounded p-2 mb-4 overflow-x-auto">{children}</pre>,
                        blockquote: ({children}) => <blockquote className="border-l-4 border-gray-200 pl-4 mb-4 italic">{children}</blockquote>,
                        table: ({children}) => <table className="min-w-full border border-gray-200 mb-4">{children}</table>,
                        th: ({children}) => <th className="border border-gray-200 px-4 py-2 bg-gray-50">{children}</th>,
                        td: ({children}) => <td className="border border-gray-200 px-4 py-2">{children}</td>
                      }}
                    >
                      {message.content}
                    </ReactMarkdown>
                  </div>
                )}
                <div className={`absolute top-0 ${message.type === 'user' ? '-right-1' : '-left-1'} w-2 h-2 transform rotate-45 ${
                  message.type === 'user'
                    ? 'bg-[#10a37f]/5'
                    : 'bg-white'
                }`} />
              </div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-100 bg-white">
        <div className="max-w-[85%] sm:max-w-[75%] md:max-w-[65%] mx-auto">
          <div className="flex flex-col bg-white rounded-xl border border-gray-200 shadow-sm hover:border-gray-300 transition-colors">
            <div className="relative flex items-center">
              <div className="flex items-center gap-1 px-2">
                <button
                  type="button"
                  onClick={() => setSearchType('search')}
                  className={`p-1.5 rounded-md transition-colors ${
                    searchType === 'search'
                      ? 'text-[#10a37f] bg-[#10a37f]/5'
                      : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'
                  }`}
                  title="Quick Search"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </button>
                <button
                  type="button"
                  onClick={() => setSearchType('research')}
                  className={`p-1.5 rounded-md transition-colors ${
                    searchType === 'research'
                      ? 'text-[#10a37f] bg-[#10a37f]/5'
                      : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'
                  }`}
                  title="Deep Research"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </button>
              </div>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={
                  searchType === 'research'
                    ? "Ask for in-depth research..."
                    : "Ask anything..."
                }
                className="flex-1 px-0 py-3 text-sm text-gray-700 placeholder-gray-400 bg-transparent border-none focus:outline-none focus:ring-0"
                disabled={isLoading}
              />
              <div className="flex items-center gap-2 pr-2">
                <button
                  type="submit"
                  disabled={isLoading || !input.trim()}
                  className={`p-2 rounded-lg transition-colors ${
                    isLoading || !input.trim()
                      ? 'text-gray-300 cursor-not-allowed'
                      : 'text-[#10a37f] hover:text-[#0e9279] hover:bg-[#10a37f]/5'
                  }`}
                  title="Send Message"
                >
                  {isLoading ? (
                    <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                  ) : (
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                    </svg>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;