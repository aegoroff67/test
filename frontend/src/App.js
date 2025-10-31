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
import AssessmentPage from './pages/AssessmentPage';
import ResultsPage from './pages/ResultsPage';

// Import context
import { AuthProvider, useAuth } from './context/AuthContext';

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
            <Route path="/" element={<Navigate to="/dashboard" />} />
          </Routes>
          <Toaster position="top-right" richColors />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
