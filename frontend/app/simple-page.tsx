'use client'

import { useState, useEffect } from 'react'

export default function Dashboard() {
  const [metrics, setMetrics] = useState({
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
      case 'running': 
      case 'ready': return 'bg-green-500'
      case 'checking': return 'bg-yellow-500'
      default: return 'bg-red-500'
    }
  }

  const handleTestCall = async () => {
    try {
      const response = await fetch('/api/sip/call', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from: '+1234567890',
          to: '+0987654321'
        })
      })
      const result = await response.json()
      alert(`Test call initiated: ${result.call_id}`)
    } catch (error) {
      alert('Test call failed: ' + error)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-lg text-white">Loading Eburon Voice Portal...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">Eburon Voice Core</h1>
          <p className="text-gray-300">Advanced AI Voice Assistant Dashboard</p>
        </div>
        <div className="flex gap-3">
          <button 
            onClick={handleTestCall}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            📞 Test Call
          </button>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-lg border border-gray-700">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-300">Active Calls</h3>
            <span className="text-blue-400">📞</span>
          </div>
          <div className="text-2xl font-bold text-white">{metrics.activeCalls}</div>
          <p className="text-xs text-gray-400">Live conversations</p>
        </div>

        <div className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-lg border border-gray-700">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-300">Total Calls</h3>
            <span className="text-blue-400">📈</span>
          </div>
          <div className="text-2xl font-bold text-white">{metrics.totalCalls}</div>
          <p className="text-xs text-gray-400">All time</p>
        </div>

        <div className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-lg border border-gray-700">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-300">Avg Duration</h3>
            <span className="text-blue-400">⏱️</span>
          </div>
          <div className="text-2xl font-bold text-white">{metrics.avgDuration}</div>
          <p className="text-xs text-gray-400">Per call</p>
        </div>

        <div className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-lg border border-gray-700">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-300">Success Rate</h3>
            <span className="text-blue-400">⚡</span>
          </div>
          <div className="text-2xl font-bold text-white">{metrics.successRate}%</div>
          <p className="text-xs text-gray-400">Call completion</p>
        </div>
      </div>

      {/* System Status */}
      <div className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-lg border border-gray-700 mb-8">
        <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <span>📊</span> System Status
        </h2>
        <p className="text-gray-300 mb-6">Real-time status of all Eburon Voice Core components</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {Object.entries(metrics.services).map(([service, status]) => (
            <div key={service} className="flex items-center justify-between p-3 rounded-lg bg-gray-900/50">
              <div>
                <p className="text-sm font-medium text-white capitalize">
                  {service.replace(/([A-Z])/g, ' $1').trim()}
                </p>
                <p className="text-xs text-gray-400">{status}</p>
              </div>
              <div className={`w-3 h-3 rounded-full ${getStatusColor(status)}`}></div>
            </div>
          ))}
        </div>
      </div>

      {/* Configuration */}
      <div className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-lg border border-gray-700">
        <h2 className="text-xl font-bold text-white mb-4">System Configuration</h2>
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
      </div>

      {/* Instructions */}
      <div className="mt-8 text-center">
        <h3 className="text-lg font-semibold text-white mb-2">🚀 Ready for Production</h3>
        <p className="text-gray-300 max-w-2xl mx-auto">
          Your Eburon Voice Core system is fully operational. Use the test call button to simulate phone calls,
          or configure your SIP provider to point to this server for real calls.
        </p>
      </div>
    </div>
  )
}
