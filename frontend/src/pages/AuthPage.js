import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { toast } from 'sonner';
import Logo from '../components/Logo';
import { CheckCircle2, Users, BarChart3 } from 'lucide-react';
import { INDUSTRIES } from '../constants/industries';

function AuthPage() {
  const [activeTab, setActiveTab] = useState('signin');
  const [loading, setLoading] = useState(false);
  const { user, login, signup } = useAuth();
  const navigate = useNavigate();

  // Sign in form
  const [signInData, setSignInData] = useState({
    email: '',
    password: ''
  });

  // Sign up form
  const [signUpData, setSignUpData] = useState({
    name: '',
    email: '',
    password: '',
    organization_name: '',
    industry: ''
  });

  useEffect(() => {
    if (user) {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  const handleSignIn = async (e) => {
    e.preventDefault();
    setLoading(true);

    const result = await login(signInData.email, signInData.password);
    
    if (result.success) {
      toast.success('Welcome back!');
      navigate('/dashboard');
    } else {
      toast.error(result.error);
    }
    
    setLoading(false);
  };

  const handleSignUp = async (e) => {
    e.preventDefault();
    setLoading(true);

    if (signUpData.password.length < 6) {
      toast.error('Password must be at least 6 characters long');
      setLoading(false);
      return;
    }

    const result = await signup(signUpData);
    
    if (result.success) {
      toast.success('Account created successfully!');
      navigate('/dashboard');
    } else {
      toast.error(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-teal-50 flex items-center justify-center p-4">
      <div className="w-full max-w-6xl grid lg:grid-cols-2 gap-8 items-center">
        {/* Left Side - Branding & Features */}
        <div className="space-y-8 text-center lg:text-left">
          {/* Logo and Title */}
          <div className="space-y-4">
            <div className="flex items-center justify-center lg:justify-start space-x-3">
              <Logo className="h-16 w-16" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  AM AI SAFE
                </h1>
                <p className="text-sm text-teal-600 font-medium">
                  EMPOWERING TRUST IN AI
                </p>
              </div>
            </div>
            
            <div className="space-y-2">
              <h2 className="text-2xl lg:text-3xl font-bold text-gray-900 leading-tight">
                AI Governance, Risk & Assurance Platform
              </h2>
              <p className="text-lg text-gray-600">
                <span className="font-bold">A</span>ssurance & <span className="font-bold">M</span>easurement for <span className="font-bold">AI</span> <span className="font-bold">S</span>afety and <span className="font-bold">A</span>ccountability
              </p>
            </div>
          </div>

          {/* Journey Title */}
          <div className="space-y-2 mt-8">
            <h2 className="text-2xl font-bold text-gray-900">
              Discover Your AI Governance Journey
            </h2>
            <p className="text-base text-gray-600 font-bold">
              From Awareness to Assurance — Four Assessments, One Framework
            </p>
          </div>

          {/* Features */}
          <div className="grid gap-6">
            <div className="flex items-start space-x-4">
              <div className="bg-teal-100 p-2 rounded-lg flex-shrink-0">
                <CheckCircle2 className="h-6 w-6 text-teal-600" />
              </div>
              <div className="text-left">
                <h3 className="font-semibold text-gray-900 mb-1">
                  Comprehensive AI Assessment Suite
                </h3>
                <p className="text-gray-600 text-sm">
                  Progress through four assessments — <strong>Awareness & Foundations</strong>, <strong>Readiness</strong>, <strong>Organisation-wide Maturity</strong>, and <strong>System Maturity</strong> — guiding your organisation from AI awareness to full governance assurance.
                </p>
              </div>
            </div>
            
            <div className="flex items-start space-x-4">
              <div className="bg-teal-100 p-2 rounded-lg flex-shrink-0">
                <BarChart3 className="h-6 w-6 text-teal-600" />
              </div>
              <div className="text-left">
                <h3 className="font-semibold text-gray-900 mb-1">
                  Actionable Analytics
                </h3>
                <p className="text-gray-600 text-sm">
                  Visualise your results instantly with interactive heatmaps, maturity scores, and prioritised recommendations.
                </p>
              </div>
            </div>
            
            <div className="flex items-start space-x-4">
              <div className="bg-teal-100 p-2 rounded-lg flex-shrink-0">
                <Users className="h-6 w-6 text-teal-600" />
              </div>
              <div className="text-left">
                <h3 className="font-semibold text-gray-900 mb-1">
                  Built for Every Stage
                </h3>
                <p className="text-gray-600 text-sm">
                  Whether you're exploring AI or managing advanced deployments, AM AI SAFE adapts to your maturity level—helping you strengthen accountability, security, and compliance at every step.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Side - Auth Form */}
        <div className="flex justify-center">
          <Card className="w-full max-w-md shadow-xl border-0 bg-white/80 backdrop-blur">
            <CardHeader className="text-center pb-2">
              <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid w-full grid-cols-2 mb-4">
                  <TabsTrigger 
                    value="signup" 
                    className="data-[state=active]:bg-teal-600 data-[state=active]:text-white"
                    data-testid="create-account-tab"
                  >
                    Create Account
                  </TabsTrigger>
                  <TabsTrigger 
                    value="signin"
                    className="data-[state=active]:bg-teal-600 data-[state=active]:text-white"
                    data-testid="sign-in-tab"
                  >
                    Sign In
                  </TabsTrigger>
                </TabsList>

                <TabsContent value="signin">
                  <CardContent className="space-y-4 px-0">
                    <form onSubmit={handleSignIn} className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="signin-email">Email *</Label>
                        <Input
                          id="signin-email"
                          type="email"
                          placeholder="Enter your email"
                          value={signInData.email}
                          onChange={(e) => setSignInData({...signInData, email: e.target.value})}
                          required
                          className="focus:ring-teal focus:border-teal-500"
                          data-testid="signin-email-input"
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="signin-password">Password *</Label>
                        <Input
                          id="signin-password"
                          type="password"
                          placeholder="Enter your password"
                          value={signInData.password}
                          onChange={(e) => setSignInData({...signInData, password: e.target.value})}
                          required
                          className="focus:ring-teal focus:border-teal-500"
                          data-testid="signin-password-input"
                        />
                      </div>
                      
                      <div className="flex items-center justify-between text-sm">
                        <label className="flex items-center space-x-2 cursor-pointer">
                          <input type="checkbox" className="rounded border-gray-300" />
                          <span className="text-gray-600">Remember me</span>
                        </label>
                        <a href="#" className="text-teal-600 hover:text-teal-700">
                          Forgot password?
                        </a>
                      </div>
                      
                      <Button 
                        type="submit" 
                        className="w-full bg-teal-600 hover:bg-teal-700 btn-hover" 
                        disabled={loading}
                        data-testid="signin-submit-btn"
                      >
                        {loading ? (
                          <div className="flex items-center space-x-2">
                            <div className="loading-spinner w-4 h-4"></div>
                            <span>Signing In...</span>
                          </div>
                        ) : (
                          'Sign In'
                        )}
                      </Button>
                    </form>
                  </CardContent>
                </TabsContent>

                <TabsContent value="signup">
                  <CardContent className="space-y-4 px-0">
                    <form onSubmit={handleSignUp} className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="signup-name">Full Name *</Label>
                          <Input
                            id="signup-name"
                            placeholder="John Doe"
                            value={signUpData.name}
                            onChange={(e) => setSignUpData({...signUpData, name: e.target.value})}
                            required
                            className="focus:ring-teal focus:border-teal-500"
                            data-testid="signup-name-input"
                          />
                        </div>
                        
                        <div className="space-y-2">
                          <Label htmlFor="signup-email">Email *</Label>
                          <Input
                            id="signup-email"
                            type="email"
                            placeholder="john@company.com"
                            value={signUpData.email}
                            onChange={(e) => setSignUpData({...signUpData, email: e.target.value})}
                            required
                            className="focus:ring-teal focus:border-teal-500"
                            data-testid="signup-email-input"
                          />
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="signup-password">Password *</Label>
                        <Input
                          id="signup-password"
                          type="password"
                          placeholder="Create a secure password"
                          value={signUpData.password}
                          onChange={(e) => setSignUpData({...signUpData, password: e.target.value})}
                          required
                          minLength={6}
                          className="focus:ring-teal focus:border-teal-500"
                          data-testid="signup-password-input"
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="signup-org">Organization Name *</Label>
                        <Input
                          id="signup-org"
                          placeholder="Your Company Name"
                          value={signUpData.organization_name}
                          onChange={(e) => setSignUpData({...signUpData, organization_name: e.target.value})}
                          required
                          className="focus:ring-teal focus:border-teal-500"
                          data-testid="signup-org-input"
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="signup-industry">Industry / Sector *</Label>
                        <Select 
                          value={signUpData.industry} 
                          onValueChange={(value) => setSignUpData({...signUpData, industry: value})}
                          required
                        >
                          <SelectTrigger className="focus:ring-teal focus:border-teal-500" data-testid="signup-industry-select">
                            <SelectValue placeholder="Select your industry" />
                          </SelectTrigger>
                          <SelectContent>
                            {INDUSTRIES.map((industry) => (
                              <SelectItem 
                                key={industry} 
                                value={industry}
                                data-testid={`industry-${industry.toLowerCase().replace(' ', '-')}`}
                              >
                                {industry}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                      
                      <Button 
                        type="submit" 
                        className="w-full bg-teal-600 hover:bg-teal-700 btn-hover" 
                        disabled={loading}
                        data-testid="signup-submit-btn"
                      >
                        {loading ? (
                          <div className="flex items-center space-x-2">
                            <div className="loading-spinner w-4 h-4"></div>
                            <span>Creating Account...</span>
                          </div>
                        ) : (
                          'Create Account'
                        )}
                      </Button>
                    </form>
                  </CardContent>
                </TabsContent>
              </Tabs>
            </CardHeader>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default AuthPage;
