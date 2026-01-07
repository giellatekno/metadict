import type { PageLoad } from "./$types";
import { redirect } from "@sveltejs/kit";
import { resolve } from "$app/paths";

export const load: PageLoad = async ({ params, fetch }) => {
    const encoded_search = encodeURIComponent(params.search);
    const response = await fetch(`/api/search/${params.lang}/${encoded_search}`);
    const lemmas = await response.json();

    if (lemmas.length === 1) {
        redirect(307, resolve(`/lookup/${params.lang}/${params.search}`));
    }

    return { lemmas };
};
