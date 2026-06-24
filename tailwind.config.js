/** @type {import('tailwindcss').Config} */
// Build: ./.build/tailwindcss -c tailwind.config.js -i src/input.css -o styles.css --minify
// Replaces the old runtime cdn.tailwindcss.com JIT compiler with a precompiled stylesheet.
// The standalone CLI binary lives in .build/ (gitignored, download for your platform from
// https://github.com/tailwindlabs/tailwindcss/releases - v3 standalone). No Node project required.
module.exports = {
  content: [
    './*.html',
    './services/*.html',
    './suburbs/*.html',
    './pricing/*.html',
    './coaches/*.html',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          black: '#0A0A0A',
          dark: '#141414',
          mid: '#1A1A1A',
          grey: '#2A2A2A',
          muted: '#888888',
          light: '#CCCCCC',
          white: '#F5F5F5',
        },
      },
    },
  },
  plugins: [],
}
