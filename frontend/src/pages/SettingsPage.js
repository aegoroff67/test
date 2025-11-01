import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { 
  Shield, 
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
  Edit
} from 'lucide-react';
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
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  // Check if user is super admin
  const isSuperAdmin = user?.role === 'SUPER_ADMIN';

  useEffect(() => {
    if (!isSuperAdmin) {
      toast.error('Super Admin access required');
      navigate('/dashboard');
      return;
    }
    
    if (activeTab === 'users') {
      fetchUsers();
    } else if (activeTab === 'fields') {
      fetchAllData();
    }
  }, [activeTab, isSuperAdmin, navigate]);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/admin/users`);
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
      const [usersRes, assessmentsRes] = await Promise.all([
        axios.get(`${API}/admin/users`),
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

  const toggleUserActive = async (userId, currentStatus) => {
    try {
      const response = await axios.put(`${API}/admin/users/${userId}/toggle-active`);
      toast.success(response.data.is_active ? 'User enabled' : 'User disabled');
      fetchUsers();
    } catch (error) {
      toast.error('Failed to update user status');
      console.error(error);
    }
  };

  const updateUserRole = async (userId, newRole) => {
    try {
      await axios.put(`${API}/admin/users/${userId}/role`, null, {
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
      const response = await axios.post(`${API}/admin/users/${userId}/reset-password`);
      
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
      await axios.delete(`${API}/admin/users/${userId}`);
      toast.success('User deleted');
      fetchUsers();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to delete user');
      console.error(error);
    }
  };

  const filteredUsers = users.filter(u => 
    u.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.organization_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-bg">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="bg-teal-600 p-2 rounded-lg">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Settings & Administration</h1>
                <p className="text-xs text-teal-600 font-medium">SUPER ADMIN PANEL</p>
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
                            <p className="text-xs text-gray-500">{u.industry}</p>
                          </td>
                          <td className="p-3">
                            <select
                              value={u.role}
                              onChange={(e) => updateUserRole(u.id, e.target.value)}
                              className="text-xs border rounded px-2 py-1"
                              disabled={u.id === user.id}
                            >
                              <option value="SUPER_ADMIN">Super Admin</option>
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
