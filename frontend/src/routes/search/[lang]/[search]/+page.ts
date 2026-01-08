import type { PageLoad } from "./$types";
import { redirect } from "@sveltejs/kit";
import { resolve } from "$app/paths";

export const load: PageLoad = async ({ params, fetch }) => {
    let url = resolve(`/api/search/${params.lang}/${encodeURIComponent(params.search)}`);
    const response = await fetch(url);
    const lemmas = await response.json();

    if (lemmas.length === 1) {
        redirect(307, resolve(`/lookup/${params.lang}/${params.search}`));
    }

    return { lemmas };
};
