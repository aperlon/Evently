/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['system-ui', '-apple-system', 'sans-serif'],
        'display': ['The Bold Font', 'system-ui', 'sans-serif'], // For large titles & "Evently"
        'mono': ['VCR OSD Mono', 'monospace'], // For subtitles, footer, small headers
      },
      colors: {
        // Mellow Ice Palette - Soft and minimal pastel colors
        'mellow': {
          'ice': '#D3EEF4',      // Soft blue
          'cream': '#F1EEC8',     // Soft yellow/cream
          'peach': '#F3A46C',     // Soft orange/peach
        },
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
      },
      backgroundImage: {
        'gradient-mellow': 'linear-gradient(90deg, #FFFFFF, #FFF8F0, #FFE8D6)',
        'gradient-mellow-vertical': 'linear-gradient(180deg, #D3EEF4, #F1EEC8, #F3A46C)',
      },
    },
  },
  plugins: [],
}
