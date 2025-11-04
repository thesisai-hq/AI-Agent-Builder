/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				primary: {
					DEFAULT: '#3B82F6',
					50: '#EBF2FE',
					100: '#D7E6FD',
					200: '#AFCDFA',
					300: '#87B4F8',
					400: '#5F9BF5',
					500: '#3B82F6',
					600: '#1E63D3',
					700: '#17499E',
					800: '#103069',
					900: '#081734'
				}
			}
		}
	},
	plugins: []
};
