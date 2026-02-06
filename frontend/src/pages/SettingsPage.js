import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { 
  ArrowLeft, 
  Users, 
  Database, 
  Building2,
  UserCheck,
  UserX,
  Trash2,
  Key,
  Shield as ShieldIcon,
  Search,
  Edit,
  Bell,
  AlertCircle,
  Download,
  ScrollText
} from 'lucide-react';
import Logo from '../components/Logo';
import LoggingTab from '../components/LoggingTab';
import { toast } from 'sonner';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ROLE_COLORS = {
  SUPER_ADMIN: { bg: 'bg-red-100', text: 'text-red-800', label: 'Super Admin' },
  ORG_ADMIN: { bg: 'bg-blue-100', text: 'text-blue-800', label: 'Org Admin' },
  ADMIN: { bg: 'bg-purple-100', text: 'text-purple-800', label: 'Admin' },
  MEMBER: { bg: 'bg-gray-100', text: 'text-gray-800', label: 'Member' }
};

// Assessment type color scheme
const getAssessmentTypeBadge = (assessmentType) => {
  const type = assessmentType || 'System';
  
  switch(type) {
    case 'Awareness':
      return { bgColor: 'bg-green-100', textColor: 'text-green-700', label: 'Awareness' };
    case 'Readiness':
      return { bgColor: 'bg-blue-100', textColor: 'text-blue-700', label: 'Readiness' };
    case 'Organisation':
    case 'Orgwide':
      return { bgColor: 'bg-purple-100', textColor: 'text-purple-700', label: 'Organisation-wide' };
    case 'System':
    default:
      return { bgColor: 'bg-teal-100', textColor: 'text-teal-700', label: 'System' };
  }
};

function SettingsPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('users');
  const [users, setUsers] = useState([]);
  const [assessments, setAssessments] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [pendingReviews, setPendingReviews] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [selectedNotifications, setSelectedNotifications] = useState([]);
  const [metadataFields, setMetadataFields] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedAssessments, setSelectedAssessments] = useState([]);
  const [orgFilter, setOrgFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');
  const [userOrgFilter, setUserOrgFilter] = useState('all'); // Filter for user management tab
  const [systemSettings, setSystemSettings] = useState({ allow_public_registration: true });
  const [updatingSettings, setUpdatingSettings] = useState(false);

  // Check user role and permissions
  const isSuperAdmin = user?.role === 'SUPER_ADMIN';
  const isOrgAdmin = user?.role === 'ORG_ADMIN';
  const isAdmin = user?.role === 'ADMIN';
  const hasAdminAccess = isSuperAdmin || isOrgAdmin || isAdmin;

  // Debug logging
  useEffect(() => {
    console.log('SettingsPage - User object:', user);
    console.log('SettingsPage - User role:', user?.role);
    console.log('SettingsPage - Has admin access:', hasAdminAccess);
  }, [user, hasAdminAccess]);

  useEffect(() => {
    // Wait for user to be loaded
    if (user === null) {
      console.log('User is still loading...');
      return;
    }
    
    // Check if user has any admin access
    if (!hasAdminAccess) {
      console.log('No admin access, redirecting...');
      toast.error('Admin access required');
      navigate('/dashboard');
      return;
    }
    
    if (activeTab === 'users') {
      fetchUsers();
      if (isSuperAdmin) {
        fetchSystemSettings();
      }
    } else if (activeTab === 'fields') {
      fetchAllData();
      fetchMetadataFields();
    } else if (activeTab === 'analytics') {
      fetchAnalytics();
    } else if (activeTab === 'reviews') {
      fetchPendingReviews();
    } else if (activeTab === 'notifications') {
      fetchNotifications();
    }
  }, [activeTab, hasAdminAccess, navigate]);

  // Separate useEffect for fetching counts on mount
  useEffect(() => {
    if (isSuperAdmin) {
      fetchUnreadCount();
      fetchPendingReviewsCount();
    }
  }, [isSuperAdmin]);

  // Refresh notification counts when window gains focus or user navigates back
  useEffect(() => {
    const handleFocus = () => {
      if (isSuperAdmin) {
        fetchUnreadCount();
        fetchPendingReviewsCount();
      }
    };

    window.addEventListener('focus', handleFocus);
    
    // Also refresh on visibility change (user switches tabs)
    const handleVisibilityChange = () => {
      if (!document.hidden && isSuperAdmin) {
        fetchUnreadCount();
        fetchPendingReviewsCount();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      window.removeEventListener('focus', handleFocus);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [isSuperAdmin]);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      // SUPER_ADMIN uses /admin/users, ORG_ADMIN uses /org/users
      const endpoint = isSuperAdmin ? `${API}/admin/users` : `${API}/org/users`;
      const response = await axios.get(endpoint);
      setUsers(response.data);
    } catch (error) {
      toast.error('Failed to fetch users');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSystemSettings = async () => {
    try {
      const response = await axios.get(`${API}/admin/system/settings`);
      setSystemSettings(response.data);
    } catch (error) {
      console.error('Failed to fetch system settings:', error);
    }
  };

  const togglePublicRegistration = async () => {
    setUpdatingSettings(true);
    try {
      const newValue = !systemSettings.allow_public_registration;
      await axios.put(`${API}/admin/system/settings`, {
        allow_public_registration: newValue
      });
      setSystemSettings({ ...systemSettings, allow_public_registration: newValue });
      toast.success(newValue ? 'Public registration enabled' : 'Public registration disabled');
    } catch (error) {
      toast.error('Failed to update settings');
      console.error(error);
    } finally {
      setUpdatingSettings(false);
    }
  };

  const fetchAllData = async () => {
    setLoading(true);
    try {
      const endpoint = isSuperAdmin ? `${API}/admin/users` : `${API}/org/users`;
      const [usersRes, assessmentsRes] = await Promise.all([
        axios.get(endpoint),
        axios.get(`${API}/assessments`)
      ]);
      setUsers(usersRes.data);
      setAssessments(assessmentsRes.data);
    } catch (error) {
      toast.error('Failed to fetch data');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMetadataFields = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/admin/metadata-fields`);
      setMetadataFields(response.data);
    } catch (error) {
      toast.error('Failed to fetch metadata fields');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/org/analytics`);
      setAnalytics(response.data);
    } catch (error) {
      toast.error('Failed to fetch analytics');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPendingReviews = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/admin/assessments/pending-reviews`);
      setPendingReviews(response.data);
    } catch (error) {
      toast.error('Failed to fetch pending reviews');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchNotifications = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/admin/notifications`);
      setNotifications(response.data);
    } catch (error) {
      toast.error('Failed to fetch notifications');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchUnreadCount = async () => {
    try {
      const response = await axios.get(`${API}/admin/notifications/unread-count`);
      setUnreadCount(response.data.count);
    } catch (error) {
      console.error('Failed to fetch unread count:', error);
    }
  };

  const fetchPendingReviewsCount = async () => {
    try {
      const response = await axios.get(`${API}/admin/assessments/pending-reviews`);
      setPendingReviews(response.data); // Update the full state so the badge shows
    } catch (error) {
      console.error('Failed to fetch pending reviews count:', error);
    }
  };

  const markNotificationRead = async (notificationId) => {
    try {
      await axios.put(`${API}/admin/notifications/${notificationId}/mark-read`);
      fetchNotifications();
      fetchUnreadCount();
    } catch (error) {
      toast.error('Failed to mark notification as read');
      console.error(error);
    }
  };

  const markAllRead = async () => {
    try {
      await axios.put(`${API}/admin/notifications/mark-all-read`);
      fetchNotifications();
      fetchUnreadCount();
      toast.success('All notifications marked as read');
    } catch (error) {
      toast.error('Failed to mark all as read');
      console.error(error);
    }
  };

  const handleSelectNotification = (notificationId) => {
    setSelectedNotifications(prev => 
      prev.includes(notificationId) 
        ? prev.filter(id => id !== notificationId)
        : [...prev, notificationId]
    );
  };

  const handleSelectAllNotifications = (checked) => {
    if (checked) {
      setSelectedNotifications(notifications.map(n => n.id));
    } else {
      setSelectedNotifications([]);
    }
  };

  const handleBulkDeleteNotifications = async () => {
    if (selectedNotifications.length === 0) {
      toast.error('Please select notifications to delete');
      return;
    }

    try {
      await axios.post(`${API}/admin/notifications/bulk-delete`, selectedNotifications);
      toast.success(`${selectedNotifications.length} notification(s) deleted`);
      setSelectedNotifications([]);
      fetchNotifications();
      fetchUnreadCount();
    } catch (error) {
      toast.error('Failed to delete notifications');
      console.error(error);
    }
  };

  const downloadMetadataCSV = (collectionName, collectionData) => {
    // Prepare CSV data
    const headers = ['Field Path', 'Type', 'Example Value'];
    const rows = [];

    // Flatten the nested structure for CSV
    const flattenFields = (fields, prefix = '') => {
      Object.entries(fields).forEach(([fieldPath, fieldInfo]) => {
        rows.push([
          fieldPath,
          fieldInfo.type,
          fieldInfo.example || 'null'
        ]);

        // Add nested structure if exists
        if (fieldInfo.nested_structure) {
          flattenFields(fieldInfo.nested_structure, fieldPath);
        }
      });
    };

    flattenFields(collectionData.fields);

    // Create CSV content
    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
    ].join('\n');

    // Create blob and download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `${collectionName}_metadata_fields.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    toast.success(`Downloaded ${collectionName} metadata fields`);
  };


  const toggleUserActive = async (userId, currentStatus) => {
    try {
      const endpoint = isSuperAdmin 
        ? `${API}/admin/users/${userId}/toggle-active`
        : `${API}/org/users/${userId}/toggle-active`;
      const response = await axios.put(endpoint);
      toast.success(response.data.is_active ? 'User enabled' : 'User disabled');
      fetchUsers();
    } catch (error) {
      toast.error('Failed to update user status');
      console.error(error);
    }
  };

  const updateUserRole = async (userId, newRole) => {
    try {
      const endpoint = isSuperAdmin 
        ? `${API}/admin/users/${userId}/role`
        : `${API}/org/users/${userId}/role`;
      await axios.put(endpoint, null, {
        params: { new_role: newRole }
      });
      toast.success('User role updated');
      fetchUsers();
    } catch (error) {
      toast.error('Failed to update user role');
      console.error(error);
    }
  };


  const updateAssessmentAccess = async (userId, assessmentAccess) => {
    if (!isSuperAdmin) return; // Only Super Admins can update assessment access
    
    try {
      await axios.put(`${API}/admin/users/${userId}/assessment-access`, assessmentAccess);
      toast.success('Assessment access updated');
      fetchUsers();
    } catch (error) {
      toast.error('Failed to update assessment access');
      console.error(error);
    }
  };

  const updateUserTier = async (userId, tier) => {
    try {
      await axios.put(`${API}/admin/users/${userId}/tier`, null, { params: { tier } });
      toast.success(`User tier updated to Tier ${tier}`);
      fetchUsers();
    } catch (error) {
      toast.error('Failed to update user tier');
      console.error(error);
    }
  };


  const resetPassword = async (userId, userEmail) => {
    if (!window.confirm(`Generate temporary password for ${userEmail}?`)) return;
    
    try {
      const endpoint = isSuperAdmin 
        ? `${API}/admin/users/${userId}/reset-password`
        : `${API}/org/users/${userId}/reset-password`;
      const response = await axios.post(endpoint);
      
      // Show password in a copyable format
      const tempPass = response.data.temporary_password;
      navigator.clipboard.writeText(tempPass);
      
      toast.success(
        <div>
          <p>Password reset! Temporary password copied to clipboard:</p>
          <code className="bg-gray-100 px-2 py-1 rounded text-sm">{tempPass}</code>
        </div>,
        { duration: 10000 }
      );
    } catch (error) {
      toast.error('Failed to reset password');
      console.error(error);
    }
  };

  const deleteUser = async (userId, userEmail) => {
    if (!window.confirm(`Permanently delete user ${userEmail}? This cannot be undone.`)) return;
    
    try {
      const endpoint = isSuperAdmin 
        ? `${API}/admin/users/${userId}`
        : `${API}/org/users/${userId}`;
      await axios.delete(endpoint);
      toast.success('User deleted');
      fetchUsers();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to delete user');
      console.error(error);
    }
  };

  const filteredUsers = users.filter(u => {
    const searchMatch = 
      u.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      u.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      u.organization_name.toLowerCase().includes(searchTerm.toLowerCase());
    
    const orgMatch = userOrgFilter === 'all' || u.organization_name === userOrgFilter;
    
    return searchMatch && orgMatch;
  });

  const handleSelectAssessment = (assessmentId) => {
    setSelectedAssessments(prev => 
      prev.includes(assessmentId)
        ? prev.filter(id => id !== assessmentId)
        : [...prev, assessmentId]
    );
  };

  const handleSelectAllAssessments = () => {
    if (selectedAssessments.length === filteredAssessments.length) {
      setSelectedAssessments([]);
    } else {
      setSelectedAssessments(filteredAssessments.map(a => a.id));
    }
  };

  const handleBulkDelete = async () => {
    if (selectedAssessments.length === 0) return;
    
    if (!window.confirm(`Delete ${selectedAssessments.length} selected assessment(s)? This cannot be undone.`)) return;
    
    try {
      const response = await axios.post(`${API}/org/assessments/bulk-delete`, selectedAssessments);
      toast.success(response.data.message);
      setSelectedAssessments([]);
      fetchAnalytics();
    } catch (error) {
      toast.error('Failed to delete assessments');
      console.error(error);
    }
  };

  // Get unique organizations for filters
  const uniqueUserOrgs = [...new Set(users.map(u => u.organization_name))];
  const uniqueOrgs = [...new Set(analytics?.assessments?.map(a => a.organization_name))];
  const uniqueTypes = [...new Set(analytics?.assessments?.map(a => a.assessment_type))];

  // Filter assessments
  const filteredAssessments = analytics?.assessments?.filter(a => {
    const orgMatch = orgFilter === 'all' || a.organization_name === orgFilter;
    const typeMatch = typeFilter === 'all' || a.assessment_type === typeFilter;
    return orgMatch && typeMatch;
  }) || [];

  return (
    <div className="min-h-screen bg-gradient-bg">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <Logo className="h-10 w-10" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  Settings & Administration
                </h1>
                <p className="text-xs text-teal-600 font-medium">
                  {isSuperAdmin && 'SUPER ADMIN PANEL'}
                  {isOrgAdmin && 'ORG ADMIN PANEL'}
                  {isAdmin && 'ADMIN PANEL'}
                </p>
              </div>
            </div>
            
            <Button 
              variant="outline" 
              onClick={() => navigate('/dashboard')}
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tabs */}
        <div className="flex space-x-2 mb-6 border-b">
          {/* User Management tab - show for SUPER_ADMIN and ORG_ADMIN */}
          {(isSuperAdmin || isOrgAdmin) && (
            <button
              onClick={() => setActiveTab('users')}
              className={`px-4 py-2 font-medium text-sm border-b-2 transition-colors ${
                activeTab === 'users'
                  ? 'border-teal-600 text-teal-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <Users className="h-4 w-4 inline mr-2" />
              User Management
            </button>
          )}
          
          {/* Analytics tab - show for ADMIN and above */}
          {(isSuperAdmin || isOrgAdmin || isAdmin) && (
            <button
              onClick={() => setActiveTab('analytics')}
              className={`px-4 py-2 font-medium text-sm border-b-2 transition-colors ${
                activeTab === 'analytics'
                  ? 'border-teal-600 text-teal-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <Database className="h-4 w-4 inline mr-2" />
              Organization Analytics
            </button>
          )}
          
          {/* View All Fields tab - show only for SUPER_ADMIN */}
          {isSuperAdmin && (
            <button
              onClick={() => setActiveTab('fields')}
              className={`px-4 py-2 font-medium text-sm border-b-2 transition-colors ${
                activeTab === 'fields'
                  ? 'border-teal-600 text-teal-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <Database className="h-4 w-4 inline mr-2" />
              View All Fields
            </button>
          )}
          
          {/* Notifications tab - show only for SUPER_ADMIN */}
          {isSuperAdmin && (
            <button
              onClick={() => setActiveTab('notifications')}
              className={`px-4 py-2 font-medium text-sm border-b-2 transition-colors relative ${
                activeTab === 'notifications'
                  ? 'border-teal-600 text-teal-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <Bell className="h-4 w-4 inline mr-2" />
              Notifications
              {unreadCount > 0 && (
                <>
                  <span className="absolute top-1 right-1 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-500 rounded-full">
                    {unreadCount}
                  </span>
                  <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                    <span className="relative inline-flex items-center justify-center rounded-full h-5 w-5 bg-red-600">
                      <AlertCircle className="h-3 w-3 text-white" />
                    </span>
                  </span>
                </>
              )}
            </button>
          )}
          
          {/* Pending Reviews tab - show only for SUPER_ADMIN */}
          {isSuperAdmin && (
            <button
              onClick={() => setActiveTab('reviews')}
              className={`px-4 py-2 font-medium text-sm border-b-2 transition-colors relative ${
                activeTab === 'reviews'
                  ? 'border-teal-600 text-teal-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <Database className="h-4 w-4 inline mr-2" />
              Pending Reviews
              {pendingReviews.length > 0 && (
                <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                  <span className="relative inline-flex items-center justify-center rounded-full h-5 w-5 bg-red-600">
                    <AlertCircle className="h-3 w-3 text-white" />
                  </span>
                </span>
              )}
            </button>
          )}
          
          {/* Logging tab - show only for SUPER_ADMIN */}
          {isSuperAdmin && (
            <button
              onClick={() => setActiveTab('logging')}
              className={`px-4 py-2 font-medium text-sm border-b-2 transition-colors ${
                activeTab === 'logging'
                  ? 'border-teal-600 text-teal-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <ScrollText className="h-4 w-4 inline mr-2" />
              Logging
            </button>
          )}
          
          <button
            onClick={() => setActiveTab('organization')}
            className={`px-4 py-2 font-medium text-sm border-b-2 transition-colors ${
              activeTab === 'organization'
                ? 'border-teal-600 text-teal-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            <Building2 className="h-4 w-4 inline mr-2" />
            Organization Settings
          </button>
        </div>

        {/* Tab Content */}
        {activeTab === 'users' && (
          <Card>
            <CardHeader>
              {/* Public Registration Toggle - Super Admin Only */}
              {isSuperAdmin && (
                <div className="mb-4 p-4 bg-gray-50 rounded-lg border">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <UserCheck className="h-5 w-5 text-gray-600" />
                      <div>
                        <p className="font-medium text-gray-900">Public Registration</p>
                        <p className="text-sm text-gray-500">
                          {systemSettings.allow_public_registration 
                            ? 'New users can create accounts via the login page' 
                            : 'Account creation is disabled - users must be invited'}
                        </p>
                      </div>
                    </div>
                    <Button
                      variant={systemSettings.allow_public_registration ? "default" : "outline"}
                      size="sm"
                      onClick={togglePublicRegistration}
                      disabled={updatingSettings}
                      className={systemSettings.allow_public_registration 
                        ? "bg-green-600 hover:bg-green-700" 
                        : "border-gray-300"}
                      data-testid="toggle-public-registration-btn"
                    >
                      {updatingSettings ? (
                        "Updating..."
                      ) : systemSettings.allow_public_registration ? (
                        <>
                          <UserCheck className="h-4 w-4 mr-2" />
                          Enabled
                        </>
                      ) : (
                        <>
                          <UserX className="h-4 w-4 mr-2" />
                          Disabled
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              )}
              
              <div className="flex justify-between items-center">
                <CardTitle>User Management</CardTitle>
                <div className="flex items-center space-x-2">
                  {/* Organization Filter (SUPER_ADMIN only) */}
                  {isSuperAdmin && uniqueUserOrgs.length > 1 && (
                    <select
                      value={userOrgFilter}
                      onChange={(e) => setUserOrgFilter(e.target.value)}
                      className="text-sm border rounded px-3 py-2"
                    >
                      <option value="all">All Organizations</option>
                      {uniqueUserOrgs.map(org => (
                        <option key={org} value={org}>{org}</option>
                      ))}
                    </select>
                  )}
                  
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                    <Input
                      placeholder="Search users..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10 w-64"
                    />
                  </div>
                  <Badge variant="outline">{filteredUsers.length} users</Badge>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-center py-8">
                  <div className="loading-spinner w-8 h-8 mx-auto mb-2"></div>
                  <p className="text-gray-500">Loading users...</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-50 border-b">
                      <tr>
                        <th className="text-left p-3 font-medium text-gray-700">User</th>
                        <th className="text-left p-3 font-medium text-gray-700">Organization</th>
                        <th className="text-left p-3 font-medium text-gray-700">Role</th>
                        <th className="text-left p-3 font-medium text-gray-700">Tier</th>
                        {isSuperAdmin && <th className="text-left p-3 font-medium text-gray-700">Assessment Types</th>}
                        <th className="text-left p-3 font-medium text-gray-700">Status</th>
                        <th className="text-right p-3 font-medium text-gray-700">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredUsers.map((u) => (
                        <tr key={u.id} className={`border-b hover:bg-gray-50 ${u.id === user.id ? 'bg-green-50' : ''}`}>
                          <td className="p-3">
                            <div className="flex items-center gap-2">
                              <div>
                                <div className="flex items-center gap-2">
                                  <p className="font-medium text-gray-900">{u.name}</p>
                                  {u.id === user.id && (
                                    <Badge className="bg-green-600 text-white text-xs">
                                      You
                                    </Badge>
                                  )}
                                </div>
                                <p className="text-xs text-gray-500">{u.email}</p>
                              </div>
                            </div>
                          </td>
                          <td className="p-3">
                            <p className="text-gray-700">{u.organization_name}</p>
                          </td>
                          <td className="p-3">
                            <select
                              value={u.role}
                              onChange={(e) => updateUserRole(u.id, e.target.value)}
                              className="text-xs border rounded px-2 py-1"
                              disabled={u.id === user.id}
                            >
                              {/* SUPER_ADMIN can assign any role, ORG_ADMIN cannot assign SUPER_ADMIN */}
                              {isSuperAdmin && <option value="SUPER_ADMIN">Super Admin</option>}
                              <option value="ORG_ADMIN">Org Admin</option>
                              <option value="ADMIN">Admin</option>
                              <option value="MEMBER">Member</option>
                            </select>
                          </td>
                          <td className="p-3">
                            <select
                              value={u.tier || 1}
                              onChange={(e) => updateUserTier(u.id, parseInt(e.target.value))}
                              className="text-xs border rounded px-2 py-1"
                              disabled={u.id === user.id}
                              title={
                                u.tier === 1 ? 'Tier 1: Awareness, Readiness' :
                                u.tier === 2 ? 'Tier 2: Awareness, Readiness, Org-wide' :
                                'Tier 3: All assessments'
                              }
                            >
                              <option value={1}>Tier 1</option>
                              <option value={2}>Tier 2</option>
                              <option value={3}>Tier 3</option>
                            </select>
                          </td>
                          {isSuperAdmin && (
                            <td className="p-3">
                              <div className="flex flex-col gap-1">
                                {/* Define tier-based access - these cannot be removed */}
                                {(() => {
                                  const tierAccess = {
                                    1: ['awareness', 'readiness'],
                                    2: ['awareness', 'readiness', 'orgwide'],
                                    3: ['awareness', 'readiness', 'orgwide', 'system', 'faira']
                                  };
                                  const userTier = u.tier || 1;
                                  const baseTierAccess = tierAccess[userTier] || [];
                                  
                                  const assessmentTypes = [
                                    { key: 'awareness', label: 'Awareness' },
                                    { key: 'readiness', label: 'Readiness' },
                                    { key: 'orgwide', label: 'Org-wide' },
                                    { key: 'system', label: 'System' },
                                    { key: 'faira', label: 'FAIRA' }
                                  ];
                                  
                                  return assessmentTypes.map(({ key, label }) => {
                                    const isBaseTier = baseTierAccess.includes(key);
                                    const isChecked = u.assessment_access?.includes(key) || false;
                                    
                                    return (
                                      <label key={key} className="flex items-center gap-1 text-xs">
                                        <input
                                          type="checkbox"
                                          checked={isChecked}
                                          disabled={isBaseTier}
                                          onChange={(e) => {
                                            if (isBaseTier) return; // Cannot remove tier-based access
                                            const newAccess = e.target.checked
                                              ? [...(u.assessment_access || []), key]
                                              : (u.assessment_access || []).filter(a => a !== key);
                                            updateAssessmentAccess(u.id, newAccess);
                                          }}
                                          className="rounded"
                                          title={isBaseTier ? `Included in Tier ${userTier} (cannot remove)` : `Add ${label} access`}
                                        />
                                        <span className={isBaseTier ? 'text-gray-400' : 'text-gray-700'}>
                                          {label}
                                          {isBaseTier && <span className="text-xs text-gray-400 ml-1">(Tier)</span>}
                                        </span>
                                      </label>
                                    );
                                  });
                                })()}
                              </div>
                            </td>
                          )}
                          <td className="p-3">
                            <Badge className={u.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                              {u.is_active ? 'Active' : 'Disabled'}
                            </Badge>
                          </td>
                          <td className="p-3">
                            <div className="flex justify-end space-x-1">
                              <Button
                                size="sm"
                                variant="ghost"
                                onClick={() => toggleUserActive(u.id, u.is_active)}
                                title={u.is_active ? 'Disable user' : 'Enable user'}
                              >
                                {u.is_active ? <UserX className="h-4 w-4" /> : <UserCheck className="h-4 w-4" />}
                              </Button>
                              <Button
                                size="sm"
                                variant="ghost"
                                onClick={() => resetPassword(u.id, u.email)}
                                title="Reset password"
                              >
                                <Key className="h-4 w-4" />
                              </Button>
                              <Button
                                size="sm"
                                variant="ghost"
                                onClick={() => deleteUser(u.id, u.email)}
                                disabled={u.id === user.id}
                                title="Delete user"
                                className="text-red-600 hover:text-red-700"
                              >
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {activeTab === 'analytics' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Total Assessments</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-gray-900">{analytics?.total_assessments || 0}</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Completed</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-green-600">{analytics?.completed_assessments || 0}</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">In Progress</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-orange-600">{analytics?.incomplete_assessments || 0}</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Average Score</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-teal-600">{analytics?.average_score || 0}%</div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <div className="flex justify-between items-center">
                  <CardTitle>Assessment List</CardTitle>
                  <div className="flex items-center gap-3">
                    {/* Filters */}
                    {isSuperAdmin && uniqueOrgs.length > 1 && (
                      <select
                        value={orgFilter}
                        onChange={(e) => setOrgFilter(e.target.value)}
                        className="text-sm border rounded px-3 py-1.5"
                      >
                        <option value="all">All Organizations</option>
                        {uniqueOrgs.map(org => (
                          <option key={org} value={org}>{org}</option>
                        ))}
                      </select>
                    )}
                    
                    {uniqueTypes.length > 1 && (
                      <select
                        value={typeFilter}
                        onChange={(e) => setTypeFilter(e.target.value)}
                        className="text-sm border rounded px-3 py-1.5"
                      >
                        <option value="all">All Types</option>
                        {uniqueTypes.map(type => (
                          <option key={type} value={type}>{type}</option>
                        ))}
                      </select>
                    )}
                    
                    {selectedAssessments.length > 0 && (
                      <Button
                        onClick={handleBulkDelete}
                        variant="destructive"
                        size="sm"
                        className="bg-red-600 hover:bg-red-700"
                      >
                        <Trash2 className="h-4 w-4 mr-2" />
                        Delete ({selectedAssessments.length})
                      </Button>
                    )}
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="text-center py-8">
                    <div className="loading-spinner w-8 h-8 mx-auto mb-2"></div>
                    <p className="text-gray-500">Loading analytics...</p>
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead className="bg-gray-50 border-b">
                        <tr>
                          <th className="text-left p-3 font-medium text-gray-700 w-10">
                            <input
                              type="checkbox"
                              checked={selectedAssessments.length === filteredAssessments.length && filteredAssessments.length > 0}
                              onChange={handleSelectAllAssessments}
                              className="rounded border-gray-300"
                            />
                          </th>
                          <th className="text-left p-3 font-medium text-gray-700">Assessment Name</th>
                          {isSuperAdmin && <th className="text-left p-3 font-medium text-gray-700">Organization</th>}
                          <th className="text-left p-3 font-medium text-gray-700">Type</th>
                          <th className="text-left p-3 font-medium text-gray-700">Status</th>
                          <th className="text-left p-3 font-medium text-gray-700">Score</th>
                          <th className="text-left p-3 font-medium text-gray-700">Created</th>
                          <th className="text-left p-3 font-medium text-gray-700">Completed</th>
                        </tr>
                      </thead>
                      <tbody>
                        {filteredAssessments.map((a) => (
                          <tr key={a.id} className="border-b hover:bg-gray-50">
                            <td className="p-3">
                              <input
                                type="checkbox"
                                checked={selectedAssessments.includes(a.id)}
                                onChange={() => handleSelectAssessment(a.id)}
                                className="rounded border-gray-300"
                              />
                            </td>
                            <td className="p-3">
                              <p className="font-medium text-gray-900">{a.name}</p>
                            </td>
                            {isSuperAdmin && (
                              <td className="p-3">
                                <p className="text-gray-700">{a.organization_name}</p>
                              </td>
                            )}
                            <td className="p-3">
                              {(() => {
                                const typeBadge = getAssessmentTypeBadge(a.assessment_type);
                                return (
                                  <Badge className={`${typeBadge.bgColor} ${typeBadge.textColor}`}>
                                    {typeBadge.label}
                                  </Badge>
                                );
                              })()}
                            </td>
                            <td className="p-3">
                              <div className="flex items-center gap-2">
                                <Badge className={a.status === 'COMPLETED' ? 'bg-green-100 text-green-800' : 'bg-orange-100 text-orange-800'}>
                                  {a.status}
                                </Badge>
                                {a.pending_review_count > 0 && (
                                  <Badge className="bg-yellow-100 text-yellow-800">
                                    {a.pending_review_count} Pending Review
                                  </Badge>
                                )}
                              </div>
                            </td>
                            <td className="p-3">
                              {a.overall_percentage ? `${a.overall_percentage}%` : 'N/A'}
                            </td>
                            <td className="p-3">
                              {a.started_at ? new Date(a.started_at).toLocaleDateString() : 'N/A'}
                            </td>
                            <td className="p-3">
                              {a.completed_at ? new Date(a.completed_at).toLocaleDateString() : '-'}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        )}

        {activeTab === 'reviews' && (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Assessments Pending Review</CardTitle>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="text-center py-8">
                    <div className="loading-spinner w-8 h-8 mx-auto mb-2"></div>
                    <p className="text-gray-500">Loading pending reviews...</p>
                  </div>
                ) : pendingReviews.length === 0 ? (
                  <div className="text-center py-12">
                    <p className="text-gray-500 text-lg">No assessments pending review</p>
                    <p className="text-gray-400 text-sm mt-2">All custom responses have been scored</p>
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead className="bg-gray-50 border-b">
                        <tr>
                          <th className="text-left p-3 font-medium text-gray-700">Assessment Name</th>
                          <th className="text-left p-3 font-medium text-gray-700">Organization</th>
                          <th className="text-left p-3 font-medium text-gray-700">Type</th>
                          <th className="text-left p-3 font-medium text-gray-700">Pending Answers</th>
                          <th className="text-left p-3 font-medium text-gray-700">Score</th>
                          <th className="text-left p-3 font-medium text-gray-700">Completed</th>
                          <th className="text-left p-3 font-medium text-gray-700">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {pendingReviews.map((assessment) => (
                          <tr key={assessment.id} className="border-b hover:bg-gray-50">
                            <td className="p-3">
                              <p className="font-medium text-gray-900">{assessment.name}</p>
                            </td>
                            <td className="p-3">
                              <p className="text-gray-700">{assessment.organization_name}</p>
                            </td>
                            <td className="p-3">
                              {(() => {
                                const typeBadge = getAssessmentTypeBadge(assessment.assessment_type);
                                return (
                                  <Badge className={`${typeBadge.bgColor} ${typeBadge.textColor}`}>
                                    {typeBadge.label}
                                  </Badge>
                                );
                              })()}
                            </td>
                            <td className="p-3">
                              <Badge className="bg-yellow-100 text-yellow-800">
                                {assessment.pending_review_count} answers
                              </Badge>
                            </td>
                            <td className="p-3">
                              {assessment.overall_percentage ? `${assessment.overall_percentage}%` : 'N/A'}
                            </td>
                            <td className="p-3">
                              {assessment.completed_at ? new Date(assessment.completed_at).toLocaleDateString() : 'N/A'}
                            </td>
                            <td className="p-3">
                              <Button
                                size="sm"
                                onClick={() => navigate(`/assessment/${assessment.id}`)}
                                className="bg-teal-600 hover:bg-teal-700"
                              >
                                Review
                              </Button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        )}

        {activeTab === 'notifications' && (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <div className="flex justify-between items-center">
                  <CardTitle>Notifications</CardTitle>
                  <div className="flex space-x-2">
                    {selectedNotifications.length > 0 && (
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={handleBulkDeleteNotifications}
                        className="bg-red-600 hover:bg-red-700"
                      >
                        <Trash2 className="h-4 w-4 mr-2" />
                        Delete Selected ({selectedNotifications.length})
                      </Button>
                    )}
                    {notifications.length > 0 && unreadCount > 0 && (
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={markAllRead}
                      >
                        Mark All as Read
                      </Button>
                    )}
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="text-center py-8">
                    <div className="loading-spinner w-8 h-8 mx-auto mb-2"></div>
                    <p className="text-gray-500">Loading notifications...</p>
                  </div>
                ) : notifications.length === 0 ? (
                  <div className="text-center py-12">
                    <Bell className="h-12 w-12 mx-auto text-gray-300 mb-3" />
                    <p className="text-gray-500 text-lg">No notifications</p>
                    <p className="text-gray-400 text-sm mt-2">You&apos;re all caught up!</p>
                  </div>
                ) : (
                  <>
                    {/* Select All Checkbox */}
                    <div className="mb-3 pb-3 border-b flex items-center">
                      <input
                        type="checkbox"
                        checked={selectedNotifications.length === notifications.length}
                        onChange={(e) => handleSelectAllNotifications(e.target.checked)}
                        className="h-4 w-4 text-teal-600 rounded border-gray-300 focus:ring-teal-500"
                      />
                      <label className="ml-2 text-sm font-medium text-gray-700">
                        Select All
                      </label>
                    </div>
                    
                    <div className="space-y-3">
                    {notifications.map((notification) => (
                      <div
                        key={notification.id}
                        className={`border rounded-lg p-4 ${
                          notification.is_read ? 'bg-white' : 'bg-blue-50 border-blue-200'
                        } hover:shadow-md transition-shadow`}
                      >
                        <div className="flex items-start space-x-3">
                          {/* Checkbox */}
                          <input
                            type="checkbox"
                            checked={selectedNotifications.includes(notification.id)}
                            onChange={() => handleSelectNotification(notification.id)}
                            className="mt-1 h-4 w-4 text-teal-600 rounded border-gray-300 focus:ring-teal-500"
                            onClick={(e) => e.stopPropagation()}
                          />
                          
                          <div className="flex-1">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <div className="flex items-center space-x-2 mb-1">
                              <h3 className="font-semibold text-gray-900">{notification.title}</h3>
                              {!notification.is_read && (
                                <Badge className="bg-blue-500 text-white text-xs">New</Badge>
                              )}
                            </div>
                            <p className="text-gray-700 mb-2">{notification.message}</p>
                            <div className="flex items-center space-x-4 text-sm text-gray-500">
                              <span>{new Date(notification.created_at).toLocaleString()}</span>
                              {notification.type === 'PENDING_REVIEW' && (
                                <Badge className="bg-yellow-100 text-yellow-800 text-xs">
                                  {notification.pending_count} pending
                                </Badge>
                              )}
                            </div>
                          </div>
                          <div className="flex space-x-2 ml-4">
                            {!notification.is_read && (
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => markNotificationRead(notification.id)}
                              >
                                Mark Read
                              </Button>
                            )}
                            {notification.type === 'PENDING_REVIEW' && (
                              <Button
                                size="sm"
                                onClick={() => {
                                  markNotificationRead(notification.id);
                                  navigate(`/assessment/${notification.assessment_id}`);
                                }}
                                className="bg-teal-600 hover:bg-teal-700"
                              >
                                Review Now
                              </Button>
                            )}
                          </div>
                        </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  </>
                )}
              </CardContent>
            </Card>
          </div>
        )}

        {activeTab === 'fields' && (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>All Metadata Fields</CardTitle>
                <p className="text-sm text-gray-600 mt-2">
                  Complete list of all metadata fields across all database collections
                </p>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="text-center py-8">
                    <div className="loading-spinner w-8 h-8 mx-auto mb-2"></div>
                    <p className="text-gray-500">Loading metadata fields...</p>
                  </div>
                ) : metadataFields ? (
                  <div className="space-y-6">
                    {Object.entries(metadataFields).map(([collectionName, collectionData]) => (
                      <div key={collectionName} className="border rounded-lg p-4">
                        <div className="flex items-center justify-between mb-3">
                          <div className="flex items-center space-x-3">
                            <h3 className="text-lg font-semibold text-gray-900 capitalize">
                              {collectionName}
                            </h3>
                            <Badge className="bg-gray-100 text-gray-700">
                              {collectionData.total_documents} document(s)
                            </Badge>
                          </div>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => downloadMetadataCSV(collectionName, collectionData)}
                            className="flex items-center space-x-2"
                          >
                            <Download className="h-4 w-4" />
                            <span>Download CSV</span>
                          </Button>
                        </div>
                        
                        {Object.keys(collectionData.fields).length > 0 ? (
                          <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200">
                              <thead className="bg-gray-50">
                                <tr>
                                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Field Path</th>
                                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Example Value</th>
                                </tr>
                              </thead>
                              <tbody className="bg-white divide-y divide-gray-200">
                                {Object.entries(collectionData.fields).map(([fieldPath, fieldInfo]) => {
                                  const depth = (fieldPath.match(/\./g) || []).length;
                                  const isNested = depth > 0;
                                  const hasNestedStructure = fieldInfo.nested_structure;
                                  
                                  return (
                                    <React.Fragment key={fieldPath}>
                                      <tr className={`hover:bg-gray-50 ${isNested ? 'bg-blue-50' : ''}`}>
                                        <td className="px-4 py-2 text-sm font-mono text-gray-900" style={{paddingLeft: `${(depth * 20) + 16}px`}}>
                                          {isNested && <span className="text-gray-400 mr-1">└─</span>}
                                          {fieldPath}
                                        </td>
                                        <td className="px-4 py-2 text-sm text-gray-600">
                                          <Badge variant="outline" className="text-xs">{fieldInfo.type}</Badge>
                                        </td>
                                        <td className="px-4 py-2 text-sm text-gray-600 max-w-md truncate">
                                          {fieldInfo.example || 'null'}
                                        </td>
                                      </tr>
                                      {hasNestedStructure && Object.entries(fieldInfo.nested_structure).map(([nestedPath, nestedInfo]) => {
                                        const nestedDepth = (nestedPath.match(/\./g) || []).length;
                                        return (
                                          <tr key={nestedPath} className="hover:bg-gray-50 bg-purple-50">
                                            <td className="px-4 py-2 text-sm font-mono text-gray-900" style={{paddingLeft: `${(nestedDepth * 20) + 16}px`}}>
                                              <span className="text-gray-400 mr-1">└─</span>
                                              {nestedPath}
                                            </td>
                                            <td className="px-4 py-2 text-sm text-gray-600">
                                              <Badge variant="outline" className="text-xs">{nestedInfo.type}</Badge>
                                            </td>
                                            <td className="px-4 py-2 text-sm text-gray-600 max-w-md truncate">
                                              {nestedInfo.example || 'null'}
                                            </td>
                                          </tr>
                                        );
                                      })}
                                    </React.Fragment>
                                  );
                                })}
                              </tbody>
                            </table>
                          </div>
                        ) : (
                          <p className="text-sm text-gray-500 italic">No fields found (empty collection)</p>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">No metadata available</p>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>User Data</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <pre className="bg-gray-50 p-4 rounded text-xs">
                    {JSON.stringify(users, null, 2)}
                  </pre>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Assessment Data</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <pre className="bg-gray-50 p-4 rounded text-xs">
                    {JSON.stringify(assessments, null, 2)}
                  </pre>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {activeTab === 'organization' && (
          <Card>
            <CardHeader>
              <CardTitle>Organization Settings</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <Label>Organization Name</Label>
                  <Input value={user?.organization_name || ''} disabled />
                </div>
                <div>
                  <Label>Industry</Label>
                  <Input value={user?.industry || ''} disabled />
                </div>
                <p className="text-sm text-gray-500 mt-4">
                  Organization-level settings and templates will be available here in the future.
                </p>
              </div>
            </CardContent>
          </Card>
        )}

        {activeTab === 'logging' && isSuperAdmin && (
          <LoggingTab />
        )}
      </div>
    </div>
  );
}

export default SettingsPage;
