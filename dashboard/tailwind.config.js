/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./index.html",
      "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
      extend: {
        colors: {
          background: "#0b0e14", // Fundo quase preto
          card: "#151a23",       // Fundo dos cards
          primary: "#3b82f6",    // Azul
          secondary: "#8b5cf6",  // Roxo
          accent: "#f59e0b",     // Laranja
          success: "#10b981",    // Verde
          text: "#f8fafc"        // Texto claro
        },
        fontFamily: {
          sans: ['Inter', 'sans-serif'],
        }
      },
    },
    plugins: [],
  }