import {defineConfig} from 'vite';
export default defineConfig({base:'/warehouse-lab-portfolio/',build:{rollupOptions:{output:{manualChunks:{three:['three','three/addons/controls/OrbitControls.js']}}}}});
