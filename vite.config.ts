import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Configuração padrão para apps React + TS
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist', // pasta final de saída
  },
  server: {
    port: 5173,
  },
})
