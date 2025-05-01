import React, { useState, useRef, useEffect } from 'react';

interface Message {
  type: 'user' | 'bot';
  content: string;
  searchType?: 'search' | 'research';
  model?: string;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState('gpt3.5');
  const [searchType, setSearchType] = useState<'search' | 'research'>('search');
  const [isModelDropdownOpen, setIsModelDropdownOpen] = useState(false);
  const modelDropdownRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

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

  const models = [
    { 
      id: 'gpt3.5', 
      name: 'GPT-3.5 : OpenAI',
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
      name: 'Deepseek : OpenRouter',
      icon: '🔍',
      description: 'Balanced performance and efficiency',
      gradient: 'from-green-500 to-teal-600'
    }
  ];

  const formatResponse = (content: string) => {
    // Remove extra # symbols and clean up the content
    const cleanContent = content
      .replace(/#{3,}/g, '##') // Convert ### or more to ##
      .replace(/\n#+\s*\n/g, '\n') // Remove empty headers
      .trim();

    // Split into sections based on headers
    const sections = cleanContent.split(/(?=^#\s|^##\s)/m);
    
    return sections.map((section, index) => {
      // Clean up the section
      const cleanSection = section.trim();
      
      if (cleanSection.startsWith('# ')) {
        // Main header (Prompt/Response)
        const [header, ...content] = cleanSection.split('\n');
        const title = header.replace(/^#\s+/, '').trim();
        
        return (
          <div key={index} className="mb-4">
            <div className="text-sm font-medium text-gray-500 mb-2">
              {title}:
            </div>
            <div className="text-gray-800">
              {processContent(content.join('\n'))}
            </div>
          </div>
        );
      } else if (cleanSection.startsWith('## ')) {
        // Subheader (Section titles)
        const [header, ...content] = cleanSection.split('\n');
        const title = header.replace(/^##\s+/, '').trim();
        
        return (
          <div key={index} className="mb-3">
            <h3 className="text-base font-medium text-gray-700 mb-2">
              {title}
            </h3>
            <div className="text-gray-600 pl-4">
              {processContent(content.join('\n'))}
            </div>
          </div>
        );
      } else {
        // Regular text
        return processContent(cleanSection);
      }
    }).filter(Boolean);
  };

  // Helper function to process content and handle code blocks
  const processContent = (text: string) => {
    const lines = text.split('\n');
    const result = [];
    let codeBlock = null;
    let codeContent = [];
    let language = '';

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      
      if (line.startsWith('```')) {
        if (codeBlock === null) {
          // Start of code block
          language = line.slice(3).trim();
          codeBlock = true;
        } else {
          // End of code block
          result.push(
            <div key={`code-${i}`} className="code-block">
              <div className="code-header">
                <span className="language">{language || 'code'}</span>
                <div className="actions">
                  <button>Copy</button>
                  <button>Edit</button>
                </div>
              </div>
              <div className="code-content">
                <pre>
                  <code>{codeContent.join('\n')}</code>
                </pre>
              </div>
            </div>
          );
          codeBlock = null;
          codeContent = [];
        }
      } else if (codeBlock) {
        // Inside code block
        codeContent.push(line);
      } else if (line !== '') {
        // Regular text
        if (line.startsWith('- ')) {
          // Bullet points
          result.push(
            <div key={i} className="flex items-start mb-2">
              <span className="mr-2 text-[#10a37f]">•</span>
              <span>{line.replace('- ', '')}</span>
            </div>
          );
        } else if (line.match(/^\d+\./)) {
          // Numbered lists
          const match = line.match(/^\d+\./);
          const number = match ? match[0] : '';
          result.push(
            <div key={i} className="flex items-start mb-2">
              <span className="mr-2 font-medium text-[#10a37f] min-w-[20px]">
                {number}
              </span>
              <span>{line.replace(/^\d+\.\s/, '')}</span>
            </div>
          );
        } else if (line.includes('**')) {
          // Bold text
          const parts = line.split(/\*\*/);
          result.push(
            <p key={i} className="mb-2">
              {parts.map((part, j) => (
                j % 2 === 0 ? 
                  <span key={j}>{part}</span> : 
                  <strong key={j} className="font-medium text-gray-900">{part}</strong>
              ))}
            </p>
          );
        } else {
          // Regular paragraph
          result.push(<p key={i} className="mb-2">{line}</p>);
        }
      }
    }

    return result;
  };

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
      const endpoint = searchType === 'search' ? '/search' : '/reason';
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
                {models.find(m => m.id === selectedModel)?.name || 'Select Model'}
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
                  {models.map((model) => (
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

        {/* Optional: Right side of header */}
        <div className="flex items-center gap-2">
          {/* Add any additional header elements here */}
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-4 space-y-6">
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
                  {message.searchType === 'search' ? '🔍 Quick Search' : '📚 Deep Research'}
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
                  <div className="prose max-w-none">
                    {formatResponse(message.content)}
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
        {isLoading && (
          <div className="flex gap-4">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#3b82f6] to-[#2563eb] flex items-center justify-center flex-shrink-0">
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div className="relative max-w-[85%] sm:max-w-[75%] md:max-w-[65%]">
              <div className="flex items-center gap-2 mb-1 text-xs text-gray-500">
                <span className="px-2 py-0.5 rounded-full bg-gray-100 font-medium">
                  {searchType === 'search' ? '🔍 Quick Search' : '📚 Deep Research'}
                </span>
              </div>
              <div className="p-5 bg-gray-50 rounded-2xl shadow-sm">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-[#3b82f6] rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-[#3b82f6] rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-[#3b82f6] rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
              <div className="absolute top-0 -left-1 w-2 h-2 transform rotate-45 bg-gray-50" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-100 bg-white">
        <div className="max-w-[85%] sm:max-w-[75%] md:max-w-[65%] mx-auto">
          <div className="flex flex-col bg-white rounded-xl border border-gray-200 shadow-sm">
            {/* Search bar */}
            <div className="relative flex items-center">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={searchType === 'search' ? 'Search anything...' : 'Ask for in-depth research...'}
                className="flex-1 px-4 py-3 text-sm text-gray-700 placeholder-gray-400 bg-transparent border-none focus:outline-none focus:ring-0"
              />
              <div className="flex items-center gap-2 pr-2">
                <button
                  type="button"
                  onClick={() => setSearchType('search')}
                  className={`p-1.5 rounded-lg transition-colors ${
                    searchType === 'search'
                      ? 'text-[#10a37f] bg-[#10a37f]/5'
                      : 'text-gray-400 hover:text-gray-600'
                  }`}
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </button>
                <button
                  type="button"
                  onClick={() => setSearchType('research')}
                  className={`p-1.5 rounded-lg transition-colors ${
                    searchType === 'research'
                      ? 'text-[#10a37f] bg-[#10a37f]/5'
                      : 'text-gray-400 hover:text-gray-600'
                  }`}
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </button>
                <div className="w-px h-6 bg-gray-200 mx-1" />
                <button
                  type="submit"
                  disabled={isLoading}
                  className="p-1.5 text-[#10a37f] hover:text-[#0e9279] rounded-lg transition-colors disabled:opacity-50"
                  title={searchType === 'search' ? 'Search' : 'Research'}
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

      <style jsx global>{`
        .prose {
          max-width: none;
          color: #374151;
        }

        .prose pre {
          background-color: #f6f6f6 !important;
          border-radius: 6px;
          padding: 16px;
          margin: 16px 0;
          overflow-x: auto;
          position: relative;
        }

        .prose code {
          background-color: #f6f6f6 !important;
          color: #333333;
          font-family: 'JetBrains Mono', monospace;
          font-size: 14px;
          line-height: 1.5;
          padding: 2px 4px;
          border-radius: 4px;
        }

        .prose pre code {
          padding: 0;
          background-color: transparent !important;
        }

        /* Code block styling */
        .prose .code-block {
          background-color: #f6f6f6 !important;
          border-radius: 6px;
          margin: 16px 0;
          overflow: hidden;
        }

        .prose .code-header {
          background-color: #f0f0f0 !important;
          border-bottom: 1px solid #e5e5e5;
          padding: 8px 12px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .prose .code-content {
          padding: 16px;
          background-color: #f6f6f6 !important;
        }

        /* Syntax highlighting */
        .prose .token.keyword,
        .prose .token.import,
        .prose .token.export,
        .prose .token.from {
          color: #0000ff !important;
        }

        .prose .token.string,
        .prose .token.template-string {
          color: #a31515 !important;
        }

        .prose .token.comment {
          color: #008000 !important;
        }

        .prose .token.function {
          color: #795E26 !important;
        }

        .prose .token.variable {
          color: #001080 !important;
        }

        .prose .token.operator,
        .prose .token.punctuation {
          color: #000000 !important;
        }

        .code-block {
          @apply my-4 rounded-lg overflow-hidden;
          background-color: #f6f6f6;
        }

        .code-block .code-header {
          @apply flex justify-between items-center px-4 py-2 border-b border-gray-200;
          background-color: #f0f0f0;
        }

        .code-block .language {
          @apply text-xs text-gray-600 font-medium;
        }

        .code-block .actions {
          @apply flex gap-2;
        }

        .code-block .actions button {
          @apply text-xs text-gray-500 hover:text-gray-700 transition-colors;
          padding: 2px 6px;
          border-radius: 4px;
        }

        .code-block .actions button:hover {
          background-color: rgba(0, 0, 0, 0.05);
        }

        .code-block .code-content {
          @apply p-4;
        }

        .code-block pre {
          @apply m-0 text-sm font-mono;
          font-family: 'JetBrains Mono', monospace;
        }

        .code-block code {
          @apply text-gray-800;
        }
      `}</style>
    </div>
  );
};

export default ChatInterface; 