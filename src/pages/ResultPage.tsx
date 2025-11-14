import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { CheckCircle, XCircle, TrendingUp, TrendingDown, Minus, Loader2 } from 'lucide-react';
import { apiService, PredictResponse } from '../services/api';
import { useToast } from '../components/Toast';

export function ResultPage() {
  const navigate = useNavigate();
  const { showToast, ToastComponent } = useToast();
  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState<PredictResponse | null>(null);

  useEffect(() => {
    fetchResult();
  }, []);

  const fetchResult = async () => {
    const sessionId = localStorage.getItem('loan_session_id');
    if (!sessionId) {
      showToast('Session not found', 'error');
      navigate('/');
      return;
    }

    try {
      const prediction = await apiService.predictEligibility(sessionId);
      setResult(prediction);
      await apiService.saveReport(sessionId);
    } catch (error) {
      showToast('Failed to fetch results', 'error');
    } finally {
      setLoading(false);
    }
  };

  const getImpactIcon = (direction: string) => {
    switch (direction) {
      case 'positive':
        return <TrendingUp className="w-5 h-5 text-green-600" />;
      case 'negative':
        return <TrendingDown className="w-5 h-5 text-red-600" />;
      default:
        return <Minus className="w-5 h-5 text-gray-600" />;
    }
  };

  const getImpactColor = (direction: string) => {
    switch (direction) {
      case 'positive':
        return 'bg-green-50 border-green-200';
      case 'negative':
        return 'bg-red-50 border-red-200';
      default:
        return 'bg-gray-50 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-16 h-16 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-xl text-gray-700">Calculating your eligibility...</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-xl text-gray-700">Unable to load results</p>
          <button
            onClick={() => navigate('/')}
            className="mt-4 text-blue-600 hover:text-blue-700"
          >
            Return to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {ToastComponent}

      <div className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Loan Eligibility Result</h1>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          <div className="text-center mb-8">
            {result.eligible ? (
              <>
                <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                  <CheckCircle className="w-16 h-16 text-green-600" />
                </div>
                <h2 className="text-3xl font-bold text-green-700 mb-2">
                  Congratulations!
                </h2>
                <p className="text-xl text-gray-700">You are eligible for the loan</p>
              </>
            ) : (
              <>
                <div className="w-24 h-24 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-6">
                  <XCircle className="w-16 h-16 text-orange-600" />
                </div>
                <h2 className="text-3xl font-bold text-orange-700 mb-2">
                  Needs Review
                </h2>
                <p className="text-xl text-gray-700">{result.message}</p>
              </>
            )}
          </div>

          <div className="mb-8">
            <div className="flex items-center justify-between mb-2">
              <span className="text-lg font-semibold text-gray-700">Eligibility Score</span>
              <span className="text-2xl font-bold text-blue-600">
                {(result.eligibility_score * 100).toFixed(0)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
              <div
                className="bg-blue-600 h-4 transition-all duration-1000 ease-out"
                style={{ width: `${result.eligibility_score * 100}%` }}
              />
            </div>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-gray-700">
              <span className="font-semibold">Note:</span> Your application has been sent to our
              managers for final review. You will be notified of the decision within 24-48 hours.
            </p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-8">
          <h3 className="text-xl font-bold text-gray-900 mb-6">
            Factors Affecting Your Eligibility
          </h3>
          <div className="space-y-4">
            {result.shap_explanation.map((factor, index) => (
              <div
                key={index}
                className={`border rounded-lg p-4 ${getImpactColor(factor.direction)}`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {getImpactIcon(factor.direction)}
                    <div>
                      <p className="font-semibold text-gray-900">{factor.feature}</p>
                      <p className="text-sm text-gray-600">
                        Value: {typeof factor.value === 'number' ? factor.value.toFixed(2) : factor.value}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className={`font-semibold ${
                      factor.direction === 'positive' ? 'text-green-700' :
                      factor.direction === 'negative' ? 'text-red-700' :
                      'text-gray-700'
                    }`}>
                      {factor.impact > 0 ? '+' : ''}{(factor.impact * 100).toFixed(0)}%
                    </p>
                    <p className="text-xs text-gray-600 capitalize">{factor.direction}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {!result.eligible && (
            <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-2">Suggestions for Improvement:</h4>
              <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                <li>Improve your credit score by paying bills on time</li>
                <li>Reduce existing EMI obligations</li>
                <li>Consider applying for a lower loan amount</li>
                <li>Increase your monthly income or add co-applicant</li>
              </ul>
            </div>
          )}
        </div>

        <div className="mt-8 text-center">
          <button
            onClick={() => {
              localStorage.removeItem('loan_session_id');
              navigate('/');
            }}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
          >
            Return to Home
          </button>
        </div>
      </div>
    </div>
  );
}
