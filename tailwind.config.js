/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        brutal: {
          bg: '#FFFDF5',        // Warm parchment canvas
          surface: '#FFFFFF',   // Clean card surface
          dark: '#121212',      // Hard outline, drop shadow, text
          yellow: '#FFE600',    // Primary action highlight
          cyan: '#00F0FF',      // Secondary accent
          mint: '#00F0A8',      // Completed task indicator
          coral: '#FF5C5C',     // Destructive action / delete button
          lavender: '#D4B8FF',  // Decorative accent
          muted: '#E5E0D8',     // Secondary border / muted state
        },
      },
      borderWidth: {
        3: '3px',
      },
      boxShadow: {
        brutal: '4px 4px 0px 0px #121212',
        'brutal-lg': '6px 6px 0px 0px #121212',
        'brutal-sm': '2px 2px 0px 0px #121212',
        'brutal-hover': '2px 2px 0px 0px #121212',
        'brutal-pressed': '0px 0px 0px 0px #121212',
        'brutal-card': '6px 6px 0px 0px #121212',
      },
      fontFamily: {
        brutal: ['"Space Grotesk"', 'system-ui', '-apple-system', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
