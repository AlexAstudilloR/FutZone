/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        manrope: ["Manrope", "sans-serif"],
        sans: ["Manrope", "sans-serif"],
      },
    },
  },
  plugins: [
    // Agregamos soporte para text rendering
    function ({ addUtilities }) {
      addUtilities({
        ".antialiased": {
          "-webkit-font-smoothing": "antialiased",
          "-moz-osx-font-smoothing": "grayscale",
        },
        ".subpixel-antialiased": {
          "-webkit-font-smoothing": "subpixel-antialiased",
          "-moz-osx-font-smoothing": "auto",
        },
      });
    },
  ],
};
