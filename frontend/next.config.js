/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['localhost'],
  },
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
  async rewrites() {
    return [
      {
        source: '/api/sip/:path*',
        destination: 'http://localhost:5060/api/:path*',
      },
      {
        source: '/api/tts/:path*',
        destination: 'http://localhost:8002/api/:path*',
      },
      {
        source: '/api/ollama/:path*',
        destination: 'http://localhost:11434/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig
