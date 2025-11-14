import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogOut, Eye, CheckCircle, XCircle, Loader2, FileText, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { apiService, ApplicationSummary, ApplicationDetail } from '../services/api';
import { useToast } from '../components/Toast';

export function ManagerDashboardPage() {
  const navigate = useNavigate();
  const { showToast, ToastComponent } = useToast();
  const [applications, setApplications] = useState<ApplicationSummary[]>([]);
  const [selectedApp, setSelectedApp] = useState<ApplicationDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [managerName, setManagerName] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('manager_token');
    const name = localStorage.getItem('manager_name');

    if (!token) {
      showToast('Please login first', 'error');
      navigate('/manager-login');
      return;
    }

    setManagerName(name || 'Manager');
    fetchApplications();
  }, [navigate, showToast]);

  const fetchApplications = async () => {
    const token = localStorage.getItem('manager_token');
    if (!token) return;

    try {
      const response = await apiService.getApplications(token);
      setApplications(response.applications);
    } catch (error) {
      showToast('Failed to fetch applications', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = async (applicationId: string) => {
    const token = localStorage.getItem('manager_token');
    if (!token) return;

    try {
      const detail = await apiService.getApplicationDetail(applicationId, token);
      setSelectedApp(detail);
    } catch (error) {
      showToast('Failed to fetch application details', 'error');
    }
  };

  const handleApprove = async () => {
    if (!selectedApp) return;

    const token = localStorage.getItem('manager_token');
    const email = localStorage.getItem('manager_email');
    if (!token || !email) return;

    setActionLoading(true);

    try {
      await apiService.approveApplication(selectedApp.id, email, token);
      showToast('Application approved successfully', 'success');
      setSelectedApp(null);
      fetchApplications();
    } catch (error) {
      showToast('Failed to approve application', 'error');
    } finally {
      setActionLoading(false);
    }
  };

  const handleReject = async () => {
    if (!selectedApp) return;

    const token = localStorage.getItem('manager_token');
    const email = localStorage.getItem('manager_email');
    if (!token || !email) return;

    setActionLoading(true);

    try {
      await apiService.rejectApplication(selectedApp.id, email, token);
      showToast('Application rejected', 'success');
      setSelectedApp(null);
      fetchApplications();
    } catch (error) {
      showToast('Failed to reject application', 'error');
    } finally {
      setActionLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('manager_token');
    localStorage.removeItem('manager_name');
    localStorage.removeItem('manager_email');
    navigate('/manager-login');
  };

  const getStatusBadge = (status: string) => {
    const styles = {
      pending: 'bg-yellow-100 text-yellow-800',
      eligible: 'bg-green-100 text-green-800',
      needs_review: 'bg-orange-100 text-orange-800',
      approved: 'bg-blue-100 text-blue-800',
      rejected: 'bg-red-100 text-red-800',
    };

    return (
      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${styles[status as keyof typeof styles] || 'bg-gray-100 text-gray-800'}`}>
        {status.replace('_', ' ').toUpperCase()}
      </span>
    );
  };

  const getImpactIcon = (direction: string) => {
    switch (direction) {
      case 'positive':
        return <TrendingUp className="w-4 h-4 text-green-600" />;
      case 'negative':
        return <TrendingDown className="w-4 h-4 text-red-600" />;
      default:
        return <Minus className="w-4 h-4 text-gray-600" />;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loader2 className="w-16 h-16 text-blue-600 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {ToastComponent}

      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Manager Dashboard</h1>
            <p className="text-sm text-gray-600">Welcome, {managerName}</p>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900"
          >
            <LogOut className="w-5 h-5" />
            Logout
          </button>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="px-6 py-4 border-b">
            <h2 className="text-xl font-bold text-gray-900">Loan Applications</h2>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Income
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Loan Amount
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Credit Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {applications.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                      No applications found
                    </td>
                  </tr>
                ) : (
                  applications.map((app) => (
                    <tr key={app.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {app.name || 'N/A'}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {app.income_claimed ? `₹${app.income_claimed.toLocaleString()}` : 'N/A'}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {app.loan_amount ? `₹${app.loan_amount.toLocaleString()}` : 'N/A'}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {app.credit_score || 'N/A'}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {getStatusBadge(app.final_status)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <button
                          onClick={() => handleViewDetails(app.id)}
                          className="text-blue-600 hover:text-blue-800 flex items-center gap-1"
                        >
                          <Eye className="w-4 h-4" />
                          View
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {selectedApp && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b px-6 py-4 flex items-center justify-between">
              <h3 className="text-xl font-bold text-gray-900">Application Details</h3>
              <button
                onClick={() => setSelectedApp(null)}
                className="text-gray-600 hover:text-gray-900 text-2xl"
              >
                ×
              </button>
            </div>

            <div className="p-6">
              <div className="grid md:grid-cols-2 gap-6 mb-6">
                <div>
                  <h4 className="text-sm font-semibold text-gray-600 mb-1">Applicant Name</h4>
                  <p className="text-lg text-gray-900">{selectedApp.name || 'N/A'}</p>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-gray-600 mb-1">Status</h4>
                  {getStatusBadge(selectedApp.final_status)}
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-gray-600 mb-1">Income (Claimed)</h4>
                  <p className="text-lg text-gray-900">
                    ₹{selectedApp.income_claimed?.toLocaleString() || 'N/A'}
                  </p>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-gray-600 mb-1">Income (Extracted)</h4>
                  <p className="text-lg text-gray-900">
                    ₹{selectedApp.income_extracted?.toLocaleString() || 'N/A'}
                  </p>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-gray-600 mb-1">Loan Amount</h4>
                  <p className="text-lg text-gray-900">
                    ₹{selectedApp.loan_amount?.toLocaleString() || 'N/A'}
                  </p>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-gray-600 mb-1">Credit Score</h4>
                  <p className="text-lg text-gray-900">{selectedApp.credit_score || 'N/A'}</p>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-gray-600 mb-1">Employment Type</h4>
                  <p className="text-lg text-gray-900">{selectedApp.employment_type || 'N/A'}</p>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-gray-600 mb-1">EMI Detected</h4>
                  <p className="text-lg text-gray-900">
                    ₹{selectedApp.emi_detected?.toLocaleString() || 'N/A'}
                  </p>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6 mb-6">
                <div>
                  <h4 className="text-sm font-semibold text-gray-600 mb-1">Aadhaar Verified</h4>
                  <p className={`text-lg font-semibold ${selectedApp.aadhaar_verified ? 'text-green-600' : 'text-red-600'}`}>
                    {selectedApp.aadhaar_verified ? 'Yes' : 'No'}
                  </p>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-gray-600 mb-1">Documents Verified</h4>
                  <p className={`text-lg font-semibold ${selectedApp.documents_verified ? 'text-green-600' : 'text-red-600'}`}>
                    {selectedApp.documents_verified ? 'Yes' : 'No'}
                  </p>
                </div>
              </div>

              {selectedApp.eligibility_score !== null && (
                <div className="mb-6">
                  <h4 className="text-sm font-semibold text-gray-600 mb-2">Eligibility Score</h4>
                  <div className="flex items-center gap-4">
                    <div className="flex-1 bg-gray-200 rounded-full h-4">
                      <div
                        className="bg-blue-600 h-4 rounded-full"
                        style={{ width: `${(selectedApp.eligibility_score || 0) * 100}%` }}
                      />
                    </div>
                    <span className="text-xl font-bold text-blue-600">
                      {((selectedApp.eligibility_score || 0) * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              )}

              {selectedApp.shap_explanation && (
                <div className="mb-6">
                  <h4 className="text-lg font-bold text-gray-900 mb-3">SHAP Explanation</h4>
                  <div className="space-y-2">
                    {selectedApp.shap_explanation.map((factor: any, index: number) => (
                      <div
                        key={index}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                      >
                        <div className="flex items-center gap-2">
                          {getImpactIcon(factor.direction)}
                          <span className="font-medium text-gray-900">{factor.feature}</span>
                          <span className="text-sm text-gray-600">
                            ({typeof factor.value === 'number' ? factor.value.toFixed(2) : factor.value})
                          </span>
                        </div>
                        <span className={`font-semibold ${
                          factor.direction === 'positive' ? 'text-green-600' :
                          factor.direction === 'negative' ? 'text-red-600' :
                          'text-gray-600'
                        }`}>
                          {factor.impact > 0 ? '+' : ''}{(factor.impact * 100).toFixed(0)}%
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {(selectedApp.final_status === 'eligible' || selectedApp.final_status === 'needs_review') && (
                <div className="flex gap-4">
                  <button
                    onClick={handleApprove}
                    disabled={actionLoading}
                    className="flex-1 bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-semibold flex items-center justify-center gap-2"
                  >
                    {actionLoading ? (
                      <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                      <>
                        <CheckCircle className="w-5 h-5" />
                        Approve
                      </>
                    )}
                  </button>
                  <button
                    onClick={handleReject}
                    disabled={actionLoading}
                    className="flex-1 bg-red-600 text-white py-3 rounded-lg hover:bg-red-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-semibold flex items-center justify-center gap-2"
                  >
                    {actionLoading ? (
                      <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                      <>
                        <XCircle className="w-5 h-5" />
                        Reject
                      </>
                    )}
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
