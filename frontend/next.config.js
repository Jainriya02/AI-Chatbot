/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://ai-chatbot-production-d2d5.up.railway.app/:path*',
      },
    ];
  },
};

module.exports = nextConfig;