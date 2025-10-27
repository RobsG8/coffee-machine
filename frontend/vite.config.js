import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// default to localhost when running the UI locally
const target = process.env.VITE_API_TARGET || 'http://localhost:8000'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': { target, changeOrigin: true }
    }
  }
})
