/**
 * Universal Color Palette for Tani AI
 *
 * This file contains the centralized color definitions that match
 * the Tailwind CSS custom theme configuration.
 */

export const colorPalette = {
	"tea-green": {
		DEFAULT: "#D8FFB4",
		100: "#F4FFE6",
		200: "#EEFFDD",
		300: "#E6FFD1",
		400: "#DFFFC5",
		500: "#D8FFB4",
		600: "#C2E89A",
		700: "#A8CC7F",
		800: "#8FB065",
		900: "#75944A",
	},
	"indigo-dye": {
		DEFAULT: "#154360",
		100: "#040d13",
		200: "#081b26",
		300: "#0d283a",
		400: "#11364d",
		500: "#154360",
		600: "#2371a1",
		700: "#3e9bd5",
		800: "#7ebce3",
		900: "#bfdef1",
	},
	emerald: {
		DEFAULT: "#60ce80",
		100: "#0e2e17",
		200: "#1c5c2e",
		300: "#2a8a46",
		400: "#39b85d",
		500: "#60ce80",
		600: "#7fd898",
		700: "#9fe2b2",
		800: "#bfebcc",
		900: "#dff5e5",
	},
	"anti-flash-white": {
		DEFAULT: "#f0f0f0",
		100: "#303030",
		200: "#606060",
		300: "#909090",
		400: "#c0c0c0",
		500: "#f0f0f0",
		600: "#f3f3f3",
		700: "#f6f6f6",
		800: "#f9f9f9",
		900: "#fcfcfc",
	},
} as const;

// Helper function to get a specific color value
export const getColor = (
	colorName: keyof typeof colorPalette,
	shade?: keyof (typeof colorPalette)["tea-green"],
) => {
	const color = colorPalette[colorName];
	if (!color) return null;

	if (shade && shade in color) {
		return color[shade as keyof typeof color];
	}

	return color.DEFAULT;
};

// CSS custom property names for use in CSS-in-JS or styled components
export const cssVariables = {
	"tea-green": {
		DEFAULT: "var(--color-tea-green)",
		100: "var(--color-tea-green-100)",
		200: "var(--color-tea-green-200)",
		300: "var(--color-tea-green-300)",
		400: "var(--color-tea-green-400)",
		500: "var(--color-tea-green-500)",
		600: "var(--color-tea-green-600)",
		700: "var(--color-tea-green-700)",
		800: "var(--color-tea-green-800)",
		900: "var(--color-tea-green-900)",
	},
	"indigo-dye": {
		DEFAULT: "var(--color-indigo-dye)",
		100: "var(--color-indigo-dye-100)",
		200: "var(--color-indigo-dye-200)",
		300: "var(--color-indigo-dye-300)",
		400: "var(--color-indigo-dye-400)",
		500: "var(--color-indigo-dye-500)",
		600: "var(--color-indigo-dye-600)",
		700: "var(--color-indigo-dye-700)",
		800: "var(--color-indigo-dye-800)",
		900: "var(--color-indigo-dye-900)",
	},
	emerald: {
		DEFAULT: "var(--color-emerald)",
		100: "var(--color-emerald-100)",
		200: "var(--color-emerald-200)",
		300: "var(--color-emerald-300)",
		400: "var(--color-emerald-400)",
		500: "var(--color-emerald-500)",
		600: "var(--color-emerald-600)",
		700: "var(--color-emerald-700)",
		800: "var(--color-emerald-800)",
		900: "var(--color-emerald-900)",
	},
	"anti-flash-white": {
		DEFAULT: "var(--color-anti-flash-white)",
		100: "var(--color-anti-flash-white-100)",
		200: "var(--color-anti-flash-white-200)",
		300: "var(--color-anti-flash-white-300)",
		400: "var(--color-anti-flash-white-400)",
		500: "var(--color-anti-flash-white-500)",
		600: "var(--color-anti-flash-white-600)",
		700: "var(--color-anti-flash-white-700)",
		800: "var(--color-anti-flash-white-800)",
		900: "var(--color-anti-flash-white-900)",
	},
} as const;
