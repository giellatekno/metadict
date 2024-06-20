import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
    server: {
        // needed for the local nginx to see the dev server
        host: '0.0.0.0',
    },

	plugins: [sveltekit()]
});
