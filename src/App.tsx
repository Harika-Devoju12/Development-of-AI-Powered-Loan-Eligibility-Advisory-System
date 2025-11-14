import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { LandingPage } from './pages/LandingPage';
import { ChatPage } from './pages/ChatPage';
import { UploadDocumentsPage } from './pages/UploadDocumentsPage';
import { AadhaarStatusPage } from './pages/AadhaarStatusPage';
import { ResultPage } from './pages/ResultPage';
import { ManagerLoginPage } from './pages/ManagerLoginPage';
import { ManagerDashboardPage } from './pages/ManagerDashboardPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/upload-documents" element={<UploadDocumentsPage />} />
        <Route path="/verify-aadhaar" element={<AadhaarStatusPage />} />
        <Route path="/result" element={<ResultPage />} />
        <Route path="/manager-login" element={<ManagerLoginPage />} />
        <Route path="/manager-dashboard" element={<ManagerDashboardPage />} />
      </Routes>
    </Router>
  );
}

export default App;
