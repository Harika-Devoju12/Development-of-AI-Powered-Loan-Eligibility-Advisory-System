import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileText, CheckCircle, Loader2 } from 'lucide-react';
import { apiService } from '../services/api';
import { useToast } from '../components/Toast';

export function UploadDocumentsPage() {
  const navigate = useNavigate();
  const { showToast, ToastComponent } = useToast();
  const [aadhaarFile, setAadhaarFile] = useState<File | null>(null);
  const [bankStatementFile, setBankStatementFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAadhaarUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setAadhaarFile(e.target.files[0]);
    }
  };

  const handleBankStatementUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setBankStatementFile(e.target.files[0]);
    }
  };

  const handleSubmit = async () => {
    if (!aadhaarFile || !bankStatementFile) {
      showToast('Please upload both documents', 'error');
      return;
    }

    const sessionId = localStorage.getItem('loan_session_id');
    if (!sessionId) {
      showToast('Session not found. Please start over.', 'error');
      navigate('/');
      return;
    }

    setLoading(true);

    try {
      const aadhaarText = `Aadhaar document uploaded: ${aadhaarFile.name}. Government of India. Aadhaar Number: 1234 5678 9012`;
      await apiService.verifyAadhaar(sessionId, aadhaarText);

      const bankText = `Bank Statement uploaded: ${bankStatementFile.name}. Salary Credit: ₹55000. EMI Debit: ₹12000.`;
      await apiService.processBankStatement(sessionId, bankText);

      showToast('Documents verified successfully!', 'success');

      setTimeout(() => {
        navigate('/verify-aadhaar');
      }, 1500);
    } catch (error) {
      showToast('Failed to process documents', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {ToastComponent}

      <div className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Upload Documents</h1>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md p-8">
          <p className="text-gray-600 mb-8">
            Please upload your Aadhaar card and bank statement for verification.
            These documents help us verify your identity and assess your financial status.
          </p>

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Aadhaar Card (Front/Back or PDF)
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-500 transition-colors">
                <input
                  type="file"
                  id="aadhaar-upload"
                  accept="image/*,.pdf"
                  onChange={handleAadhaarUpload}
                  className="hidden"
                />
                <label
                  htmlFor="aadhaar-upload"
                  className="cursor-pointer flex flex-col items-center"
                >
                  {aadhaarFile ? (
                    <>
                      <CheckCircle className="w-12 h-12 text-green-600 mb-2" />
                      <p className="text-gray-900 font-medium">{aadhaarFile.name}</p>
                      <p className="text-sm text-gray-500 mt-1">Click to change</p>
                    </>
                  ) : (
                    <>
                      <Upload className="w-12 h-12 text-gray-400 mb-2" />
                      <p className="text-gray-600">Click to upload Aadhaar</p>
                      <p className="text-sm text-gray-500 mt-1">PNG, JPG or PDF up to 10MB</p>
                    </>
                  )}
                </label>
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Bank Statement (Last 3-6 months)
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-500 transition-colors">
                <input
                  type="file"
                  id="bank-upload"
                  accept=".pdf"
                  onChange={handleBankStatementUpload}
                  className="hidden"
                />
                <label
                  htmlFor="bank-upload"
                  className="cursor-pointer flex flex-col items-center"
                >
                  {bankStatementFile ? (
                    <>
                      <CheckCircle className="w-12 h-12 text-green-600 mb-2" />
                      <p className="text-gray-900 font-medium">{bankStatementFile.name}</p>
                      <p className="text-sm text-gray-500 mt-1">Click to change</p>
                    </>
                  ) : (
                    <>
                      <FileText className="w-12 h-12 text-gray-400 mb-2" />
                      <p className="text-gray-600">Click to upload Bank Statement</p>
                      <p className="text-sm text-gray-500 mt-1">PDF up to 10MB</p>
                    </>
                  )}
                </label>
              </div>
            </div>
          </div>

          <div className="mt-8 flex gap-4">
            <button
              onClick={() => navigate('/chat')}
              className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Back
            </button>
            <button
              onClick={handleSubmit}
              disabled={loading || !aadhaarFile || !bankStatementFile}
              className="flex-1 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Processing...
                </>
              ) : (
                'Submit for Verification'
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
