import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
***REMOVED***plugins: [react()],
***REMOVED***build: {
***REMOVED***outDir: "../static",
***REMOVED***emptyOutDir: true,
***REMOVED***sourcemap: true
***REMOVED***,
***REMOVED***server: {
***REMOVED***proxy: {
***REMOVED******REMOVED***"/ask": "http://localhost:5000",
***REMOVED******REMOVED***"/chat": "http://localhost:5000"
***REMOVED***
***REMOVED***
});
