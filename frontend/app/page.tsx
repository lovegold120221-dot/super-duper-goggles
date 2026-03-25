'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Activity, Phone, MessageSquare, Zap, Users, TrendingUp, Clock, CheckCircle, AlertCircle } from 'lucide-react'
import { CallMetrics } from '@/components/call-metrics'
import { LiveCalls } from '@/components/live-calls'
import { SystemStatus } from '@/components/system-status'
import { CallHistory } from '@/components/call-history'

interface SystemMetrics {
  activeCalls: number
  totalCalls: number
  avgDuration: string
  successRate: number
  services: {
    sipGateway: string
    ttsServer: string
    ollama: string
    voiceAgent: string
  }
}

export default function Dashboard() {
  const [metrics, setMetrics] = useState<SystemMetrics>({
    activeCalls: 0,
    totalCalls: 0,
    avgDuration: '0:00',
    successRate: 0,
    services: {
      sipGateway: 'checking',
      ttsServer: 'checking',
      ollama: 'checking',
      voiceAgent: 'checking'
    }
  })
  
  const [loading, setLoading] = useState(true)
  const [selectedTab, setSelectedTab] = useState('overview')

  useEffect(() => {
    const fetchSystemStatus = async () => {
      try {
        const response = await fetch('/api/sip/status')
        const data = await response.json()
        
        setMetrics(prev => ({
          ...prev,
          activeCalls: data.active_calls?.length || 0,
          totalCalls: data.total_calls || 0,
          services: {
            sipGateway: data.services?.sip_gateway || 'unknown',
            ttsServer: data.services?.tts_server || 'unknown',
            ollama: data.services?.ollama || 'unknown',
            voiceAgent: data.services?.voice_agent || 'unknown'
          }
        }))
      } catch (error) {
        console.error('Failed to fetch system status:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchSystemStatus()
    const interval = setInterval(fetchSystemStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-green-500'
      case 'ready': return 'bg-blue-500'
      case 'checking': return 'bg-yellow-500'
      default: return 'bg-red-500'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running':
      case 'ready': return <CheckCircle className="w-4 h-4" />
      case 'checking': return <Clock className="w-4 h-4" />
      default: return <AlertCircle className="w-4 h-4" />
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-lg">Loading Eburon Voice Portal...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">Eburon Voice Core</h1>
          <p className="text-gray-300">Advanced AI Voice Assistant Dashboard</p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline" className="glass-effect text-white border-gray-600">
            <Activity className="w-4 h-4 mr-2" />
            Live Status
          </Button>
          <Button className="bg-primary hover:bg-primary/600">
            <Phone className="w-4 h-4 mr-2" />
            Test Call
          </Button>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="glass-effect card-hover">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-300">Active Calls</CardTitle>
            <Phone className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{metrics.activeCalls}</div>
            <p className="text-xs text-gray-400">Live conversations</p>
          </CardContent>
        </Card>

        <Card className="glass-effect card-hover">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-300">Total Calls</CardTitle>
            <TrendingUp className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{metrics.totalCalls}</div>
            <p className="text-xs text-gray-400">All time</p>
          </CardContent>
        </Card>

        <Card className="glass-effect card-hover">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-300">Avg Duration</CardTitle>
            <Clock className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{metrics.avgDuration}</div>
            <p className="text-xs text-gray-400">Per call</p>
          </CardContent>
        </Card>

        <Card className="glass-effect card-hover">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-300">Success Rate</CardTitle>
            <Zap className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{metrics.successRate}%</div>
            <p className="text-xs text-gray-400">Call completion</p>
          </CardContent>
        </Card>
      </div>

      {/* System Status */}
      <Card className="glass-effect">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <Activity className="w-5 h-5" />
            System Status
          </CardTitle>
          <CardDescription className="text-gray-300">
            Real-time status of all Eburon Voice Core components
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {Object.entries(metrics.services).map(([service, status]) => (
              <div key={service} className="flex items-center justify-between p-3 rounded-lg bg-gray-800/50">
                <div>
                  <p className="text-sm font-medium text-white capitalize">
                    {service.replace(/([A-Z])/g, ' $1').trim()}
                  </p>
                  <p className="text-xs text-gray-400">{status}</p>
                </div>
                <div className={`p-2 rounded-full ${getStatusColor(status)} bg-opacity-20`}>
                  <div className={`${getStatusColor(status)} text-white`}>
                    {getStatusIcon(status)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Main Content Tabs */}
      <Tabs value={selectedTab} onValueChange={setSelectedTab} className="w-full">
        <TabsList className="grid w-full grid-cols-4 glass-effect">
          <TabsTrigger value="overview" className="text-white data-[state=active]:bg-primary">Overview</TabsTrigger>
          <TabsTrigger value="calls" className="text-white data-[state=active]:bg-primary">Live Calls</TabsTrigger>
          <TabsTrigger value="analytics" className="text-white data-[state=active]:bg-primary">Analytics</TabsTrigger>
          <TabsTrigger value="settings" className="text-white data-[state=active]:bg-primary">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <CallMetrics />
            <SystemStatus />
          </div>
        </TabsContent>

        <TabsContent value="calls" className="space-y-6">
          <LiveCalls />
        </TabsContent>

        <TabsContent value="analytics" className="space-y-6">
          <CallHistory />
        </TabsContent>

        <TabsContent value="settings" className="space-y-6">
          <Card className="glass-effect">
            <CardHeader>
              <CardTitle className="text-white">System Configuration</CardTitle>
              <CardDescription className="text-gray-300">
                Configure your Eburon Voice Core settings
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-300">SIP Gateway</label>
                  <p className="text-xs text-gray-400">localhost:5060</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-300">TTS Server</label>
                  <p className="text-xs text-gray-400">localhost:8002</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-300">LLM Server</label>
                  <p className="text-xs text-gray-400">localhost:11434</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-300">Model</label>
                  <p className="text-xs text-gray-400">llama3:latest</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
