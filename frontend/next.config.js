/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  // Ensure proper routing
  trailingSlash: false,
}

module.exports = nextConfig

