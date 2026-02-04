import React, { useState, useEffect, useCallback } from 'react';
import { 
  FileText, 
  BarChart3, 
  AlertTriangle, 
  Download, 
  RefreshCw,
  Search,
  Filter,
  ChevronDown,
  ChevronUp,
  CheckCircle2,
  XCircle,
  Clock,
  Trash2,
  Eye
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../components/ui/select';
import { Badge } from '../components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '../components/ui/dialog';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

// Sub-tab navigation
const SUB_TABS = [
  { id: 'audit', label: 'Audit Trail', icon: FileText },
  { id: 'analytics', label: 'Analytics', icon: BarChart3 },
  { id: 'errors', label: 'Error Log', icon: AlertTriangle },
  { id: 'cache', label: 'AI Cache', icon: RefreshCw },
];

// Severity colors
const SEVERITY_COLORS = {
  low: 'bg-blue-100 text-blue-800',
  medium: 'bg-yellow-100 text-yellow-800',
  high: 'bg-orange-100 text-orange-800',
  critical: 'bg-red-100 text-red-800',
};

// Action type colors
const ACTION_COLORS = {
  auth_login_success: 'bg-green-100 text-green-800',
  auth_login_failed: 'bg-red-100 text-red-800',
  auth_logout: 'bg-gray-100 text-gray-800',
  assessment_created: 'bg-blue-100 text-blue-800',
  assessment_completed: 'bg-green-100 text-green-800',
  assessment_deleted: 'bg-red-100 text-red-800',
  report_generated: 'bg-purple-100 text-purple-800',
  report_downloaded: 'bg-purple-100 text-purple-800',
  evidence_uploaded: 'bg-teal-100 text-teal-800',
  user_created: 'bg-indigo-100 text-indigo-800',
  settings_changed: 'bg-orange-100 text-orange-800',
};

export default function LoggingTab() {
  const [activeSubTab, setActiveSubTab] = useState('audit');
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  
  // Audit state
  const [auditLogs, setAuditLogs] = useState([]);
  const [auditTotal, setAuditTotal] = useState(0);
  const [auditPage, setAuditPage] = useState(0);
  const [auditFilters, setAuditFilters] = useState({ action: '', user: '' });
  const [actionTypes, setActionTypes] = useState([]);
  const [auditUsers, setAuditUsers] = useState([]);
  const [selectedAuditLog, setSelectedAuditLog] = useState(null);
  
  // Analytics state
  const [analyticsData, setAnalyticsData] = useState(null);
  const [analyticsDays, setAnalyticsDays] = useState(30);
  
  // Error state
  const [errorLogs, setErrorLogs] = useState([]);
  const [errorTotal, setErrorTotal] = useState(0);
  const [errorPage, setErrorPage] = useState(0);
  const [errorFilters, setErrorFilters] = useState({ severity: '', resolved: '' });
  const [errorSummary, setErrorSummary] = useState(null);
  const [selectedError, setSelectedError] = useState(null);

  // AI Cache state
  const [aiCacheStats, setAiCacheStats] = useState(null);
  const [clearingCache, setClearingCache] = useState(false);

  const token = localStorage.getItem('token');

  // Fetch stats
  const fetchStats = useCallback(async () => {
    try {
      const response = await fetch(`${API}/admin/logs/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  }, [token]);

  // Fetch audit logs
  const fetchAuditLogs = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        skip: auditPage * 50,
        limit: 50,
      });
      if (auditFilters.action) params.append('action', auditFilters.action);
      if (auditFilters.user) params.append('actor_email', auditFilters.user);
      
      const response = await fetch(`${API}/admin/logs/audit?${params}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setAuditLogs(data.logs);
        setAuditTotal(data.total);
      }
    } catch (error) {
      console.error('Error fetching audit logs:', error);
    }
    setLoading(false);
  }, [token, auditPage, auditFilters]);

  // Fetch action types
  const fetchActionTypes = useCallback(async () => {
    try {
      const response = await fetch(`${API}/admin/logs/audit/actions`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setActionTypes(data.actions);
      }
    } catch (error) {
      console.error('Error fetching action types:', error);
    }
  }, [token]);

  // Fetch audit users
  const fetchAuditUsers = useCallback(async () => {
    try {
      const response = await fetch(`${API}/admin/logs/audit/users`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setAuditUsers(data.users);
      }
    } catch (error) {
      console.error('Error fetching audit users:', error);
    }
  }, [token]);

  // Fetch analytics
  const fetchAnalytics = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API}/admin/logs/analytics?days=${analyticsDays}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setAnalyticsData(data);
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
    setLoading(false);
  }, [token, analyticsDays]);

  // Fetch error logs
  const fetchErrorLogs = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        skip: errorPage * 50,
        limit: 50,
      });
      if (errorFilters.severity) params.append('severity', errorFilters.severity);
      if (errorFilters.resolved !== '') params.append('resolved', errorFilters.resolved);
      
      const response = await fetch(`${API}/admin/logs/errors?${params}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setErrorLogs(data.logs);
        setErrorTotal(data.total);
      }
    } catch (error) {
      console.error('Error fetching error logs:', error);
    }
    setLoading(false);
  }, [token, errorPage, errorFilters]);

  // Fetch error summary
  const fetchErrorSummary = useCallback(async () => {
    try {
      const response = await fetch(`${API}/admin/logs/errors/summary?days=7`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setErrorSummary(data);
      }
    } catch (error) {
      console.error('Error fetching error summary:', error);
    }
  }, [token]);

  // Export audit logs
  const handleExportAuditLogs = async () => {
    try {
      const response = await fetch(`${API}/admin/logs/export`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `audit_logs_${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
        window.URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Error exporting logs:', error);
    }
  };

  // Cleanup old logs
  const handleCleanupLogs = async () => {
    if (!window.confirm('This will permanently delete logs older than 90 days. Continue?')) return;
    
    try {
      const response = await fetch(`${API}/admin/logs/cleanup?retention_days=90`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        alert(`Cleanup complete. Deleted: ${JSON.stringify(data.deleted_counts)}`);
        fetchStats();
      }
    } catch (error) {
      console.error('Error cleaning up logs:', error);
    }
  };

  // Effects
  useEffect(() => {
    fetchStats();
    fetchActionTypes();
    fetchAuditUsers();
  }, [fetchStats, fetchActionTypes, fetchAuditUsers]);

  useEffect(() => {
    if (activeSubTab === 'audit') {
      fetchAuditLogs();
    } else if (activeSubTab === 'analytics') {
      fetchAnalytics();
    } else if (activeSubTab === 'errors') {
      fetchErrorLogs();
      fetchErrorSummary();
    }
  }, [activeSubTab, fetchAuditLogs, fetchAnalytics, fetchErrorLogs, fetchErrorSummary]);

  // Format timestamp - prefer AEST if available, otherwise convert UTC
  const formatTimestamp = (timestamp, timestampAest) => {
    if (timestampAest) {
      // Use pre-formatted AEST timestamp from backend
      const date = new Date(timestampAest);
      return date.toLocaleString('en-AU', { 
        timeZone: 'Australia/Sydney',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      }) + ' AEST';
    }
    if (!timestamp) return '-';
    // Fallback for legacy entries without AEST
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  // Format action label
  const formatAction = (action) => {
    return action?.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) || '-';
  };

  return (
    <div className="space-y-6">
      {/* Header with stats */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-900">Logging & Analytics</h2>
          <p className="text-sm text-gray-500">Monitor application activity, errors, and user behavior</p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={handleExportAuditLogs}>
            <Download className="h-4 w-4 mr-1" />
            Export CSV
          </Button>
          <Button variant="outline" size="sm" onClick={handleCleanupLogs}>
            <Trash2 className="h-4 w-4 mr-1" />
            Cleanup (90d)
          </Button>
          <Button variant="outline" size="sm" onClick={fetchStats}>
            <RefreshCw className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Stats overview */}
      {stats && (
        <div className="grid grid-cols-4 gap-4">
          <Card>
            <CardContent className="pt-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-gray-500">Audit Logs (24h)</p>
                  <p className="text-2xl font-bold">{stats.audit_logs?.last_24h || 0}</p>
                </div>
                <FileText className="h-8 w-8 text-blue-500 opacity-50" />
              </div>
              <p className="text-xs text-gray-400 mt-1">Total: {stats.audit_logs?.total || 0}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-gray-500">Analytics Events (24h)</p>
                  <p className="text-2xl font-bold">{stats.analytics_events?.last_24h || 0}</p>
                </div>
                <BarChart3 className="h-8 w-8 text-green-500 opacity-50" />
              </div>
              <p className="text-xs text-gray-400 mt-1">Total: {stats.analytics_events?.total || 0}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-gray-500">Errors (24h)</p>
                  <p className="text-2xl font-bold">{stats.error_logs?.last_24h || 0}</p>
                </div>
                <AlertTriangle className="h-8 w-8 text-red-500 opacity-50" />
              </div>
              <p className="text-xs text-gray-400 mt-1">Unresolved: {stats.error_logs?.unresolved || 0}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-gray-500">Retention</p>
                  <p className="text-2xl font-bold">90 days</p>
                </div>
                <Clock className="h-8 w-8 text-purple-500 opacity-50" />
              </div>
              <p className="text-xs text-gray-400 mt-1">Auto-cleanup enabled</p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Sub-tab navigation */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8">
          {SUB_TABS.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveSubTab(tab.id)}
                className={`flex items-center space-x-2 py-3 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeSubTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab content */}
      {activeSubTab === 'audit' && (
        <div className="space-y-4">
          {/* Filters */}
          <div className="flex items-center space-x-4">
            <Select
              value={auditFilters.action}
              onValueChange={(value) => {
                setAuditFilters(prev => ({ ...prev, action: value === 'all' ? '' : value }));
                setAuditPage(0);
              }}
            >
              <SelectTrigger className="w-[200px]">
                <SelectValue placeholder="Filter by action" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Actions</SelectItem>
                {actionTypes.map((action) => (
                  <SelectItem key={action.value} value={action.value}>
                    {action.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select
              value={auditFilters.user}
              onValueChange={(value) => {
                setAuditFilters(prev => ({ ...prev, user: value === 'all' ? '' : value }));
                setAuditPage(0);
              }}
            >
              <SelectTrigger className="w-[220px]">
                <SelectValue placeholder="Filter by user" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Users</SelectItem>
                {auditUsers.map((user) => (
                  <SelectItem key={user.value} value={user.value}>
                    {user.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button variant="outline" size="sm" onClick={() => { setAuditFilters({ action: '', user: '' }); setAuditPage(0); }}>
              Clear Filters
            </Button>
          </div>

          {/* Audit table */}
          <Card>
            <CardContent className="p-0">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50 border-b">
                    <tr>
                      <th className="text-left p-3 font-medium text-gray-600">Timestamp (AEST)</th>
                      <th className="text-left p-3 font-medium text-gray-600">Action</th>
                      <th className="text-left p-3 font-medium text-gray-600">User</th>
                      <th className="text-left p-3 font-medium text-gray-600">Object</th>
                      <th className="text-left p-3 font-medium text-gray-600">Result</th>
                      <th className="text-left p-3 font-medium text-gray-600">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y">
                    {loading ? (
                      <tr><td colSpan={6} className="p-8 text-center text-gray-500">Loading...</td></tr>
                    ) : auditLogs.length === 0 ? (
                      <tr><td colSpan={6} className="p-8 text-center text-gray-500">No audit logs found</td></tr>
                    ) : (
                      auditLogs.map((log, idx) => (
                        <tr key={idx} className="hover:bg-gray-50">
                          <td className="p-3 text-gray-600 text-xs">{formatTimestamp(log.timestamp, log.timestamp_aest)}</td>
                          <td className="p-3">
                            <Badge className={ACTION_COLORS[log.action] || 'bg-gray-100 text-gray-800'}>
                              {formatAction(log.action)}
                            </Badge>
                          </td>
                          <td className="p-3 text-gray-900">{log.actor_email || '-'}</td>
                          <td className="p-3 text-gray-600">
                            {log.object_type && (
                              <span className="text-xs">
                                {log.object_type}: {log.object_name || log.object_id || '-'}
                              </span>
                            )}
                          </td>
                          <td className="p-3">
                            {log.result === 'success' ? (
                              <CheckCircle2 className="h-4 w-4 text-green-500" />
                            ) : (
                              <XCircle className="h-4 w-4 text-red-500" />
                            )}
                          </td>
                          <td className="p-3">
                            <Button variant="ghost" size="sm" onClick={() => setSelectedAuditLog(log)}>
                              <Eye className="h-4 w-4" />
                            </Button>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
              
              {/* Pagination */}
              <div className="flex items-center justify-between p-3 border-t bg-gray-50">
                <p className="text-sm text-gray-600">
                  Showing {auditPage * 50 + 1} - {Math.min((auditPage + 1) * 50, auditTotal)} of {auditTotal}
                </p>
                <div className="flex items-center space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setAuditPage(p => Math.max(0, p - 1))}
                    disabled={auditPage === 0}
                  >
                    Previous
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setAuditPage(p => p + 1)}
                    disabled={(auditPage + 1) * 50 >= auditTotal}
                  >
                    Next
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {activeSubTab === 'analytics' && (
        <div className="space-y-4">
          {/* Period selector */}
          <div className="flex items-center space-x-4">
            <Select value={analyticsDays.toString()} onValueChange={(v) => setAnalyticsDays(parseInt(v))}>
              <SelectTrigger className="w-[150px]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="7">Last 7 days</SelectItem>
                <SelectItem value="30">Last 30 days</SelectItem>
                <SelectItem value="90">Last 90 days</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" size="sm" onClick={fetchAnalytics}>
              <RefreshCw className="h-4 w-4 mr-1" />
              Refresh
            </Button>
          </div>

          {analyticsData && (
            <div className="grid grid-cols-2 gap-4">
              {/* Event Counts */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Event Summary</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {Object.entries(analyticsData.event_counts || {}).map(([event, count]) => (
                      <div key={event} className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">{formatAction(event)}</span>
                        <Badge variant="secondary">{count}</Badge>
                      </div>
                    ))}
                    {Object.keys(analyticsData.event_counts || {}).length === 0 && (
                      <p className="text-sm text-gray-500">No events recorded yet</p>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Assessment Types */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Assessment Types</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {Object.entries(analyticsData.assessment_types || {}).map(([type, count]) => (
                      <div key={type} className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">{type}</span>
                        <Badge variant="secondary">{count}</Badge>
                      </div>
                    ))}
                    {Object.keys(analyticsData.assessment_types || {}).length === 0 && (
                      <p className="text-sm text-gray-500">No assessment data yet</p>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Daily Activity */}
              <Card className="col-span-2">
                <CardHeader>
                  <CardTitle className="text-sm">Daily Activity (Last {analyticsDays} Days)</CardTitle>
                </CardHeader>
                <CardContent>
                  {analyticsData.daily_activity?.length > 0 ? (
                    <div className="flex items-end space-x-1 h-32">
                      {analyticsData.daily_activity.map((day, idx) => {
                        const maxCount = Math.max(...analyticsData.daily_activity.map(d => d.count));
                        const height = maxCount > 0 ? (day.count / maxCount) * 100 : 0;
                        return (
                          <div
                            key={idx}
                            className="flex-1 bg-blue-500 rounded-t hover:bg-blue-600 transition-colors"
                            style={{ height: `${Math.max(height, 2)}%` }}
                            title={`${day.date}: ${day.count} events`}
                          />
                        );
                      })}
                    </div>
                  ) : (
                    <p className="text-sm text-gray-500 text-center py-8">No activity data available</p>
                  )}
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      )}

      {activeSubTab === 'errors' && (
        <div className="space-y-4">
          {/* Error summary */}
          {errorSummary && (
            <div className="grid grid-cols-4 gap-4">
              <Card>
                <CardContent className="pt-4">
                  <p className="text-xs text-gray-500">Total Errors (7d)</p>
                  <p className="text-2xl font-bold">{errorSummary.total_errors}</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-4">
                  <p className="text-xs text-gray-500">Unresolved</p>
                  <p className="text-2xl font-bold text-red-600">{errorSummary.unresolved_count}</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-4">
                  <p className="text-xs text-gray-500">Critical</p>
                  <p className="text-2xl font-bold text-red-600">{errorSummary.severity_breakdown?.critical || 0}</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-4">
                  <p className="text-xs text-gray-500">High</p>
                  <p className="text-2xl font-bold text-orange-600">{errorSummary.severity_breakdown?.high || 0}</p>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Filters */}
          <div className="flex items-center space-x-4">
            <Select
              value={errorFilters.severity}
              onValueChange={(value) => {
                setErrorFilters(prev => ({ ...prev, severity: value === 'all' ? '' : value }));
                setErrorPage(0);
              }}
            >
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="Severity" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Severities</SelectItem>
                <SelectItem value="critical">Critical</SelectItem>
                <SelectItem value="high">High</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="low">Low</SelectItem>
              </SelectContent>
            </Select>
            <Select
              value={errorFilters.resolved}
              onValueChange={(value) => {
                setErrorFilters(prev => ({ ...prev, resolved: value === 'all' ? '' : value }));
                setErrorPage(0);
              }}
            >
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="false">Unresolved</SelectItem>
                <SelectItem value="true">Resolved</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" size="sm" onClick={() => { setErrorFilters({ severity: '', resolved: '' }); setErrorPage(0); }}>
              Clear Filters
            </Button>
          </div>

          {/* Error table */}
          <Card>
            <CardContent className="p-0">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50 border-b">
                    <tr>
                      <th className="text-left p-3 font-medium text-gray-600">Timestamp (AEST)</th>
                      <th className="text-left p-3 font-medium text-gray-600">Severity</th>
                      <th className="text-left p-3 font-medium text-gray-600">Type</th>
                      <th className="text-left p-3 font-medium text-gray-600">Message</th>
                      <th className="text-left p-3 font-medium text-gray-600">Endpoint</th>
                      <th className="text-left p-3 font-medium text-gray-600">Status</th>
                      <th className="text-left p-3 font-medium text-gray-600">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y">
                    {loading ? (
                      <tr><td colSpan={7} className="p-8 text-center text-gray-500">Loading...</td></tr>
                    ) : errorLogs.length === 0 ? (
                      <tr><td colSpan={7} className="p-8 text-center text-gray-500">No error logs found</td></tr>
                    ) : (
                      errorLogs.map((log, idx) => (
                        <tr key={idx} className="hover:bg-gray-50">
                          <td className="p-3 text-gray-600 text-xs">{formatTimestamp(log.timestamp, log.timestamp_aest)}</td>
                          <td className="p-3">
                            <Badge className={SEVERITY_COLORS[log.severity] || 'bg-gray-100'}>
                              {log.severity}
                            </Badge>
                          </td>
                          <td className="p-3 text-gray-900 font-mono text-xs">{log.error_type}</td>
                          <td className="p-3 text-gray-600 max-w-xs truncate">{log.error_message}</td>
                          <td className="p-3 text-gray-600 font-mono text-xs">{log.endpoint || '-'}</td>
                          <td className="p-3">
                            {log.resolved ? (
                              <Badge className="bg-green-100 text-green-800">Resolved</Badge>
                            ) : (
                              <Badge className="bg-red-100 text-red-800">Open</Badge>
                            )}
                          </td>
                          <td className="p-3">
                            <Button variant="ghost" size="sm" onClick={() => setSelectedError(log)}>
                              <Eye className="h-4 w-4" />
                            </Button>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
              
              {/* Pagination */}
              <div className="flex items-center justify-between p-3 border-t bg-gray-50">
                <p className="text-sm text-gray-600">
                  Showing {errorPage * 50 + 1} - {Math.min((errorPage + 1) * 50, errorTotal)} of {errorTotal}
                </p>
                <div className="flex items-center space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setErrorPage(p => Math.max(0, p - 1))}
                    disabled={errorPage === 0}
                  >
                    Previous
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setErrorPage(p => p + 1)}
                    disabled={(errorPage + 1) * 50 >= errorTotal}
                  >
                    Next
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Audit Log Detail Dialog */}
      <Dialog open={!!selectedAuditLog} onOpenChange={() => setSelectedAuditLog(null)}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Audit Log Details</DialogTitle>
          </DialogHeader>
          {selectedAuditLog && (
            <div className="space-y-3 text-sm">
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <p className="text-gray-500">Timestamp (AEST)</p>
                  <p className="font-medium">{formatTimestamp(selectedAuditLog.timestamp, selectedAuditLog.timestamp_aest)}</p>
                </div>
                <div>
                  <p className="text-gray-500">Action</p>
                  <Badge className={ACTION_COLORS[selectedAuditLog.action] || 'bg-gray-100'}>
                    {formatAction(selectedAuditLog.action)}
                  </Badge>
                </div>
                <div>
                  <p className="text-gray-500">User</p>
                  <p className="font-medium">{selectedAuditLog.actor_email || '-'}</p>
                </div>
                <div>
                  <p className="text-gray-500">Result</p>
                  <p className="font-medium">{selectedAuditLog.result}</p>
                </div>
                <div>
                  <p className="text-gray-500">Object Type</p>
                  <p className="font-medium">{selectedAuditLog.object_type || '-'}</p>
                </div>
                <div>
                  <p className="text-gray-500">Object ID</p>
                  <p className="font-medium font-mono text-xs">{selectedAuditLog.object_id || '-'}</p>
                </div>
              </div>
              {selectedAuditLog.details && Object.keys(selectedAuditLog.details).length > 0 && (
                <div>
                  <p className="text-gray-500 mb-1">Details</p>
                  <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto max-h-40">
                    {JSON.stringify(selectedAuditLog.details, null, 2)}
                  </pre>
                </div>
              )}
              {selectedAuditLog.source_ip && (
                <div>
                  <p className="text-gray-500">Source IP</p>
                  <p className="font-medium font-mono">{selectedAuditLog.source_ip}</p>
                </div>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* Error Detail Dialog */}
      <Dialog open={!!selectedError} onOpenChange={() => setSelectedError(null)}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Error Details</DialogTitle>
          </DialogHeader>
          {selectedError && (
            <div className="space-y-3 text-sm">
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <p className="text-gray-500">Timestamp (AEST)</p>
                  <p className="font-medium">{formatTimestamp(selectedError.timestamp, selectedError.timestamp_aest)}</p>
                </div>
                <div>
                  <p className="text-gray-500">Severity</p>
                  <Badge className={SEVERITY_COLORS[selectedError.severity] || 'bg-gray-100'}>
                    {selectedError.severity}
                  </Badge>
                </div>
                <div>
                  <p className="text-gray-500">Type</p>
                  <p className="font-medium font-mono">{selectedError.error_type}</p>
                </div>
                <div>
                  <p className="text-gray-500">Endpoint</p>
                  <p className="font-medium font-mono">{selectedError.endpoint || '-'}</p>
                </div>
              </div>
              <div>
                <p className="text-gray-500 mb-1">Message</p>
                <p className="bg-red-50 p-2 rounded text-red-800">{selectedError.error_message}</p>
              </div>
              {selectedError.stack_trace && (
                <div>
                  <p className="text-gray-500 mb-1">Stack Trace</p>
                  <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto max-h-60 font-mono">
                    {selectedError.stack_trace}
                  </pre>
                </div>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
