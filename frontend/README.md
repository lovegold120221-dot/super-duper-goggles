# Eburon Voice Core Portal

A beautiful, Vercel-deployable frontend dashboard for the Eburon Voice Core system, inspired by Vapi.ai's modern interface.

## 🚀 Quick Start

### Option 1: Static HTML (Recommended for Vercel)
```bash
cd frontend
# Simply deploy the index.html to Vercel
vercel deploy --prod
```

### Option 2: Local Development
```bash
cd frontend
python -m http.server 3000
# Open http://localhost:3000
```

## 🎨 Features

### 📊 Real-time Dashboard
- **Live Call Monitoring**: Track active calls and total calls
- **System Status**: Real-time status of all components
- **Metrics Visualization**: Success rates, average duration
- **Auto-refresh**: Updates every 5 seconds

### 🎛️ Interactive Controls
- **Test Call Button**: Simulate phone calls instantly
- **Service Status**: Visual indicators for each component
- **Configuration Display**: System endpoints and settings

### 🎨 Modern UI/UX
- **Glass Morphism**: Beautiful frosted glass effects
- **Gradient Backgrounds**: Animated color gradients
- **Responsive Design**: Works on all devices
- **Dark Theme**: Easy on the eyes
- **Smooth Animations**: Hover effects and transitions

## 🏗️ Architecture

```
Frontend (Vercel) → API Routes → Backend Services
                      ↓
                   /api/sip/* → localhost:5060
                   /api/tts/* → localhost:8002
                   /api/ollama/* → localhost:11434
```

## 📱 Components

### Header Section
- System title and description
- Refresh status button
- Test call trigger

### Metrics Cards
- Active calls counter
- Total calls statistics
- Average duration display
- Success rate percentage

### System Status Grid
- SIP Gateway status
- TTS Server status
- Ollama LLM status
- Voice Agent status

### Configuration Panel
- Service endpoints
- Model information
- Connection details

## 🔧 API Integration

The frontend automatically connects to your Eburon Voice Core backend:

### System Status
```javascript
GET /api/sip/status
Response: {
  active_calls: {},
  total_calls: 0,
  services: {
    sip_gateway: "running",
    tts_server: "running",
    ollama: "running",
    voice_agent: "ready"
  }
}
```

### Test Call
```javascript
POST /api/sip/call
Body: {
  "from": "+1234567890",
  "to": "+0987654321"
}
Response: {
  "call_id": "call_1",
  "status": "connected",
  "room": "room-call_1"
}
```

## 🌐 Vercel Deployment

### 1. Install Vercel CLI
```bash
npm i -g vercel
```

### 2. Deploy
```bash
cd frontend
vercel --prod
```

### 3. Configure Environment (Optional)
Create `vercel.json`:
```json
{
  "rewrites": [
    {
      "source": "/api/sip/:path*",
      "destination": "http://localhost:5060/api/:path*"
    },
    {
      "source": "/api/tts/:path*", 
      "destination": "http://localhost:8002/api/:path*"
    },
    {
      "source": "/api/ollama/:path*",
      "destination": "http://localhost:11434/api/:path*"
    }
  ]
}
```

## 🎯 Usage

1. **Deploy to Vercel**: Push the frontend to Vercel
2. **Access Dashboard**: Open your Vercel URL
3. **Monitor System**: View real-time status
4. **Test Calls**: Use the test call button
5. **Scale**: Add more features as needed

## 🔒 Security

- **CORS Enabled**: Cross-origin requests handled
- **API Proxy**: Backend services proxied safely
- **No Secrets**: No sensitive data in frontend

## 📊 Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers

## 🎨 Customization

### Colors
Edit the CSS variables in `index.html`:
```css
:root {
  --primary-color: #0ea5e9;
  --secondary-color: #6366f1;
  --accent-color: #8b5cf6;
}
```

### Branding
Replace the logo and text in the header section.

## 🚀 Production Ready

The frontend is production-ready with:
- ✅ Optimized performance
- ✅ Responsive design
- ✅ Error handling
- ✅ Loading states
- ✅ User feedback
- ✅ Vercel optimization

## 📞 Integration with Eburon Voice Core

The frontend seamlessly integrates with your existing Eburon Voice Core setup:

1. **Backend Services**: Must be running on localhost
2. **API Routes**: Configured for proxy access
3. **Real-time Data**: Auto-refreshes system status
4. **Call Testing**: Direct integration with SIP gateway

---

**Deploy your beautiful voice AI dashboard today!** 🎉
