import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { CheckCircle, Loader2 } from 'lucide-react';
import { useToast } from '../components/Toast';

export function AadhaarStatusPage() {
  const navigate = useNavigate();
  const { showToast, ToastComponent } = useToast();
  const [loading, setLoading] = useState(true);
  const [verified, setVerified] = useState(false);

  useEffect(() => {
    const sessionId = localStorage.getItem('loan_session_id');
    if (!sessionId) {
      showToast('Session not found', 'error');
      navigate('/');
      return;
    }

    setTimeout(() => {
      setVerified(true);
      setLoading(false);
    }, 2000);
  }, [navigate, showToast]);

  const handleContinue = () => {
    navigate('/result');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-16 h-16 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-xl text-gray-700">Verifying your Aadhaar...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {ToastComponent}

      <div className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Verification Status</h1>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          {verified ? (
            <>
              <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <CheckCircle className="w-16 h-16 text-green-600" />
              </div>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Verification Successful!
              </h2>
              <p className="text-gray-600 mb-8">
                Your Aadhaar has been verified successfully. We are now processing your bank statement
                and calculating your loan eligibility.
              </p>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
                <p className="text-sm text-gray-700">
                  <span className="font-semibold">Next Step:</span> We will analyze your documents
                  and provide your eligibility result.
                </p>
              </div>
              <button
                onClick={handleContinue}
                className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
              >
                View Eligibility Result
              </button>
            </>
          ) : (
            <>
              <div className="w-24 h-24 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-4xl">✕</span>
              </div>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Verification Failed
              </h2>
              <p className="text-gray-600 mb-8">
                We could not verify your Aadhaar. Please ensure you uploaded a valid document.
              </p>
              <button
                onClick={() => navigate('/upload-documents')}
                className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
              >
                Try Again
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
