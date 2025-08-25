import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import eslint from 'vite-plugin-eslint'

export default defineConfig({
  plugins: [react(), 
        tailwindcss(),
        eslint({
      include: ['src/**/*.js', 'src/**/*.jsx']
    })
  ],
  build: {
    outDir: 'build',
  },
});