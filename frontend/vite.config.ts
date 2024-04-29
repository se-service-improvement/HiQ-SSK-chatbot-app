import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
***REMOVED***outDir: '../static',
***REMOVED***emptyOutDir: true,
***REMOVED***sourcemap: true
  },
  server: {
***REMOVED***proxy: {
***REMOVED***  '/ask': 'http://localhost:5000',
***REMOVED***  '/chat': 'http://localhost:5000'
***REMOVED***
  }
})
