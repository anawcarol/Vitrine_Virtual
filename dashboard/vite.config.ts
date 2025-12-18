import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Isso libera o acesso por links públicos (ngrok, localhost.run, etc)
    allowedHosts: true,
    host: true // Opcional: Garante que ele ouça conexões externas
  }
})