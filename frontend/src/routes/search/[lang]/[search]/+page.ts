import type { PageLoad } from "./$types";
import { error, redirect } from "@sveltejs/kit";
import { resolve } from "$app/paths";
import type { SearchResponse } from "$lib/utils";

export const load: PageLoad = async ({ params, fetch }) => {
    let url = resolve(
        `/api/search/${params.lang}/${encodeURIComponent(params.search)}`,
    );
    const res = await fetch(url);
    console.debug("STATUS:", res.status);

    if (!res.ok) {
        error(res.status, "fetch to api failed");
    }
    const lemmas: SearchResponse = await res.json();

    if (lemmas && lemmas.length === 1) {
        redirect(307, resolve(`/lookup/${params.lang}/${params.search}`));
    }

    return { lemmas };
};
