/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./linefree/templates/**/*.html",    // app-level templates
    "./templates/**/*.html",             // project-level templates (if any)
    "./**/templates/**/*.html",          // any templates directory
    "./**/*.html",                       // any HTML file
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
