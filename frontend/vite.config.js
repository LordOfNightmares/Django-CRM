import { sentrySvelteKit } from "@sentry/sveltekit";
import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const apiTarget = env.PUBLIC_DJANGO_API_URL || 'http://localhost:8000';
  return {
    server: {
      proxy: {
        '/admin': { target: apiTarget, changeOrigin: true },
        '/static': { target: apiTarget, changeOrigin: true },
        '/swagger-ui': { target: apiTarget, changeOrigin: true },
        '/schema': { target: apiTarget, changeOrigin: true },
        '/healthz': { target: apiTarget, changeOrigin: true }
      }
    },
    plugins: [sentrySvelteKit({
      org: "micropyramid-fa",
      project: "bottlecrm-app",
      sourceMapsUploadOptions: {
        authToken: env.SENTRY_AUTH_TOKEN
      },
      autoUploadSourceMaps: !!env.PUBLIC_SENTRY_DSN
    }), tailwindcss(), sveltekit()],
  };
});
