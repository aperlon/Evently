import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: path.resolve(__dirname, '../.dist'),
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    watch: {
      usePolling: true,
      interval: 1000,
    },
    hmr: {
      host: 'localhost',
      port: 3000,
    },
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
