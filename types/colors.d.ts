// Custom Tailwind Color Palette Types
export interface ColorShades {
	DEFAULT: string;
	100: string;
	200: string;
	300: string;
	400: string;
	500: string;
	600: string;
	700: string;
	800: string;
	900: string;
}

export interface CustomColors {
	"tea-green": ColorShades;
	"indigo-dye": ColorShades;
	emerald: ColorShades;
	"anti-flash-white": ColorShades;
}

// Extend Tailwind's default theme
declare module "tailwindcss/theme" {
	interface Theme {
		colors: CustomColors & {
			[key: string]: string | ColorShades;
		};
	}
}
