import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';
import { Toaster } from '@/components/ui/sonner';
import { toast } from 'sonner';
import './App.css';

// Import pages
import AuthPage from './pages/AuthPage';
import Dashboard from './pages/Dashboard';
import AssessmentSelector from './pages/AssessmentSelector';
import SystemPreAssessmentForm from './pages/SystemPreAssessmentForm';
import OrgPreAssessmentForm from './pages/OrgPreAssessmentForm';
import ReadinessPreAssessmentForm from './pages/ReadinessPreAssessmentForm';
import AwarenessPreAssessmentForm from './pages/AwarenessPreAssessmentForm';
import FairaAssessmentForm from './pages/FairaAssessmentForm';
import FairaResultsPage from './pages/FairaResultsPage';
import SettingsPage from './pages/SettingsPage';
import ReviewAssessmentPage from './pages/ReviewAssessmentPage';
import AssessmentPage from './pages/AssessmentPage';
import ResultsPage from './pages/ResultsPage';
import FrameworkCoveragePage from './pages/FrameworkCoveragePage';
import EvidenceRegisterPage from './pages/EvidenceRegisterPage';

// Import context
import { AuthProvider, useAuth } from './context/AuthContext';

// Import Error Boundary
import ErrorBoundary from './components/ErrorBoundary';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Axios interceptor for auth
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/auth';
    }
    return Promise.reject(error);
  }
);

// Protected Route component
function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }
  
  return user ? children : <Navigate to="/auth" />;
}

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <Router>
          <div className="App min-h-screen bg-gray-50">
            <Routes>
              <Route path="/auth" element={<AuthPage />} />
              <Route 
                path="/dashboard" 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/settings" 
                element={
                  <ProtectedRoute>
                    <SettingsPage />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/review-assessment/:assessmentId" 
                element={
                  <ProtectedRoute>
                    <ReviewAssessmentPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/assessment-selector" 
              element={
                <ProtectedRoute>
                  <AssessmentSelector />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/assessment/:id/onboarding" 
              element={
                <ProtectedRoute>
                  <SystemPreAssessmentForm />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/assessment/:id/org-onboarding" 
              element={
                <ProtectedRoute>
                  <OrgPreAssessmentForm />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/assessment/:assessmentId/readiness-onboarding" 
              element={
                <ProtectedRoute>
                  <ReadinessPreAssessmentForm />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/assessment/:id/awareness-onboarding" 
              element={
                <ProtectedRoute>
                  <AwarenessPreAssessmentForm />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/assessment/:id/faira-onboarding" 
              element={
                <ProtectedRoute>
                  <FairaAssessmentForm />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/assessment/:id" 
              element={
                <ProtectedRoute>
                  <AssessmentPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/results/:id" 
              element={
                <ProtectedRoute>
                  <ResultsPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/framework-coverage/:id" 
              element={
                <ProtectedRoute>
                  <FrameworkCoveragePage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/evidence-register/:id" 
              element={
                <ProtectedRoute>
                  <EvidenceRegisterPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/faira-results/:id" 
              element={
                <ProtectedRoute>
                  <FairaResultsPage />
                </ProtectedRoute>
              } 
            />
            <Route path="/" element={<Navigate to="/dashboard" />} />
          </Routes>
          <Toaster position="top-right" richColors />
        </div>
      </Router>
    </AuthProvider>
    </ErrorBoundary>
  );
}

export default App;
