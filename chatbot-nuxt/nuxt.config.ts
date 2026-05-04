// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
  typescript: {
    strict: true,
    typeCheck: true,
    shim: false
  },
  runtimeConfig: {
    backendUrl: process.env.BACKEND_URL ?? 'http://localhost:8000',
    public: {
      openaiApiKey: process.env.OPENAI_API_KEY,
    },
  },
  app: {
    head: {
      link: [
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Inter+Tight:ital,wght@0,300;0,600;1,300&family=JetBrains+Mono:wght@400&display=swap'
        }
      ]
    }
  }
})

