/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",      // project-level templates
    "./**/templates/**/*.html"    // app-level templates
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
