import js from '@eslint/js';
import tseslint from 'typescript-eslint';

export default [
	js.configs.recommended,
	...tseslint.configs.recommended,
	{
		files: ['**/*.{ts,tsx}'],
		rules: {
			'no-unused-vars': 'warn',
			'@typescript-eslint/no-unused-vars': ['warn', {
				argsIgnorePattern: '^_',
				varsIgnorePattern: '^_',
			}],
			'@typescript-eslint/no-explicit-any': 'error',
		},
	},
	{
		ignores: ['dist', 'node_modules', '.astro', 'public', '**/*.astro'],
	},
];
