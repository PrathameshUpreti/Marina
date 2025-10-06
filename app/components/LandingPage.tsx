import React from 'react';

interface LandingPageProps {
  onGetStarted: () => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onGetStarted }) => {
  return (
    <div className="fixed inset-0 bg-gradient-to-br from-[#f7f7f7] to-[#9df9ef] z-50 flex items-center justify-center transition-all duration-500">
      <div className="w-[95%] max-w-[1100px] flex gap-10 items-center">
        <div className="flex-1 p-5">
          <h1 className="text-5xl font-extrabold mb-4 bg-gradient-to-r from-[#51e2f5] to-[#ffa8b6] bg-clip-text text-transparent tracking-tight">
            Marina AI
          </h1>
          <p className="text-lg text-[#4a4e69] mb-8 leading-relaxed">
            Your intelligent research assistant powered by advanced AI technology.
          </p>
          
          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="bg-white rounded-2xl p-4 shadow-lg border border-[#e5eaf5] transition-all hover:scale-105 hover:shadow-xl">
              <div className="text-3xl mb-3">🔍</div>
              <h3 className="text-lg font-semibold text-[#51e2f5] mb-2">Smart Search</h3>
              <p className="text-sm text-gray-600">Advanced search capabilities powered by AI</p>
            </div>
            
            <div className="bg-white rounded-2xl p-4 shadow-lg border border-[#e5eaf5] transition-all hover:scale-105 hover:shadow-xl">
              <div className="text-3xl mb-3">📚</div>
              <h3 className="text-lg font-semibold text-[#51e2f5] mb-2">Research</h3>
              <p className="text-sm text-gray-600">Deep research and analysis of topics</p>
            </div>
            
            <div className="bg-white rounded-2xl p-4 shadow-lg border border-[#e5eaf5] transition-all hover:scale-105 hover:shadow-xl">
              <div className="text-3xl mb-3">💡</div>
              <h3 className="text-lg font-semibold text-[#51e2f5] mb-2">Insights</h3>
              <p className="text-sm text-gray-600">Generate comprehensive reports and insights</p>
            </div>
          </div>
          
          <button
            onClick={onGetStarted}
            className="bg-gradient-to-r from-[#51e2f5] to-[#ffa8b6] text-white px-8 py-3 rounded-full text-lg font-semibold shadow-lg transition-all hover:scale-105 hover:shadow-xl"
          >
            Get Started
          </button>
        </div>
        
        <div className="flex-1 relative h-[380px]">
          <div className="absolute top-1/4 left-1/4 bg-white rounded-xl p-4 flex items-center gap-3 shadow-lg border border-[#edf756] animate-float">
            <div className="text-2xl">🔍</div>
            <p className="font-medium">Smart Search</p>
          </div>
          <div className="absolute top-1/2 left-1/3 bg-white rounded-xl p-4 flex items-center gap-3 shadow-lg border border-[#edf756] animate-float" style={{ animationDelay: '2s' }}>
            <div className="text-2xl">📚</div>
            <p className="font-medium">Research</p>
          </div>
          <div className="absolute top-3/4 left-1/4 bg-white rounded-xl p-4 flex items-center gap-3 shadow-lg border border-[#edf756] animate-float" style={{ animationDelay: '4s' }}>
            <div className="text-2xl">💡</div>
            <p className="font-medium">Insights</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage; 