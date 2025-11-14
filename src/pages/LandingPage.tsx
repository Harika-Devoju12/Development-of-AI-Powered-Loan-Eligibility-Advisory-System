import { useNavigate } from 'react-router-dom';
import { MessageCircle, Phone } from 'lucide-react';

export function LandingPage() {
  const navigate = useNavigate();

  const handleStartChat = () => {
    navigate('/chat');
  };

  const handleVoiceCall = () => {
    alert('Voice call feature: Please call +1-800-LOAN-APP or use the web call feature (coming soon)');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Loan Eligibility AI System
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Smart, fast, and secure loan application process powered by AI
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto mb-12">
          <div
            onClick={handleStartChat}
            className="bg-white rounded-2xl shadow-lg p-8 cursor-pointer hover:shadow-xl transition-shadow duration-300 border-2 border-transparent hover:border-blue-500"
          >
            <div className="flex flex-col items-center text-center">
              <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mb-6">
                <MessageCircle className="w-10 h-10 text-blue-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-3">
                Start Chat with AI Assistant
              </h2>
              <p className="text-gray-600 mb-6">
                Chat with our intelligent AI assistant to complete your loan application quickly and easily.
              </p>
              <button className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
                Start Chat
              </button>
            </div>
          </div>

          <div
            onClick={handleVoiceCall}
            className="bg-white rounded-2xl shadow-lg p-8 cursor-pointer hover:shadow-xl transition-shadow duration-300 border-2 border-transparent hover:border-green-500"
          >
            <div className="flex flex-col items-center text-center">
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mb-6">
                <Phone className="w-10 h-10 text-green-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-3">
                Talk to AI (Voice Call)
              </h2>
              <p className="text-gray-600 mb-6">
                Prefer to speak? Connect with our voice AI system for a conversational experience.
              </p>
              <button className="bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors">
                Start Voice Call
              </button>
            </div>
          </div>
        </div>

        <div className="max-w-4xl mx-auto bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
          <p className="text-gray-700">
            Both modes follow the same loan verification and eligibility process.
            Your data is secure and processed using advanced AI technology.
          </p>
        </div>

        <div className="mt-16 text-center">
          <button
            onClick={() => navigate('/manager-login')}
            className="text-gray-600 hover:text-gray-900 underline"
          >
            Manager Login
          </button>
        </div>
      </div>
    </div>
  );
}
