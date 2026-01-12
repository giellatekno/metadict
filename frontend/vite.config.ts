import { paraglideVitePlugin } from "@inlang/paraglide-js";
import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
    server: {
        // needed for the local nginx to see the dev server
        host: "0.0.0.0",
    },

    plugins: [
        tailwindcss(),
        sveltekit(),
        paraglideVitePlugin({
            project: "./project.inlang",
            outdir: "./src/lib/paraglide",
            strategy: ['localStorage', 'baseLocale'],
        }),
    ],
});
