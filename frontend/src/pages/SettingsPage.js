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
  Bell
} from 'lucide-react';
import Logo from '../components/Logo';
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
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedAssessments, setSelectedAssessments] = useState([]);
  const [orgFilter, setOrgFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');
  const [userOrgFilter, setUserOrgFilter] = useState('all'); // Filter for user management tab

  // Check user role and permissions
  const isSuperAdmin = user?.role === 'SUPER_ADMIN';
  const isOrgAdmin = user?.role === 'ORG_ADMIN';
  const isAdmin = user?.role === 'ADMIN';
  const hasAdminAccess = isSuperAdmin || isOrgAdmin || isAdmin;

  useEffect(() => {
    // Check if user has any admin access
    if (!hasAdminAccess) {
      toast.error('Admin access required');
      navigate('/dashboard');
      return;
    }
    
    // Fetch unread notification count for Super Admin
    if (isSuperAdmin) {
      fetchUnreadCount();
    }
    
    if (activeTab === 'users') {
      fetchUsers();
    } else if (activeTab === 'fields') {
      fetchAllData();
    } else if (activeTab === 'analytics') {
      fetchAnalytics();
    } else if (activeTab === 'reviews') {
      fetchPendingReviews();
    } else if (activeTab === 'notifications') {
      fetchNotifications();
    }
  }, [activeTab, hasAdminAccess, navigate]);

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
                <span className="absolute top-1 right-1 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-500 rounded-full">
                  {unreadCount}
                </span>
              )}
            </button>
          )}
          
          {/* Pending Reviews tab - show only for SUPER_ADMIN */}
          {isSuperAdmin && (
            <button
              onClick={() => setActiveTab('reviews')}
              className={`px-4 py-2 font-medium text-sm border-b-2 transition-colors ${
                activeTab === 'reviews'
                  ? 'border-teal-600 text-teal-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <Database className="h-4 w-4 inline mr-2" />
              Pending Reviews
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
                            <p className="text-xs text-gray-500">{u.default_industry || u.industry || 'Not set'}</p>
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
                              <Badge className="bg-blue-100 text-blue-800">
                                {a.assessment_type}
                              </Badge>
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
                              <Badge className="bg-blue-100 text-blue-800">
                                {assessment.assessment_type}
                              </Badge>
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
                    <p className="text-gray-400 text-sm mt-2">You're all caught up!</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {notifications.map((notification) => (
                      <div
                        key={notification.id}
                        className={`border rounded-lg p-4 ${
                          notification.is_read ? 'bg-white' : 'bg-blue-50 border-blue-200'
                        } hover:shadow-md transition-shadow`}
                      >
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
                                  navigate(`/review-assessment/${notification.assessment_id}`);
                                }}
                                className="bg-teal-600 hover:bg-teal-700"
                              >
                                Review Now
                              </Button>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        )}

        {activeTab === 'fields' && (
          <div className="space-y-6">
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
      </div>
    </div>
  );
}

export default SettingsPage;
