import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";
import precompileIntl from "svelte-intl-precompile/sveltekit-plugin.js";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
    server: {
        // needed for the local nginx to see the dev server
        host: "0.0.0.0",
    },

    plugins: [tailwindcss(), precompileIntl("src/locales"), sveltekit()],
});
