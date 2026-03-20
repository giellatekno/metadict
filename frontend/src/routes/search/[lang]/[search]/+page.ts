import type { PageLoad } from "./$types";
import { error, redirect } from "@sveltejs/kit";
import { resolve } from "$app/paths";
import { SEARCH_OPTIONS, SearchResponse } from "$lib/utils";

export const load: PageLoad = async ({ params, fetch }) => {
    let langs = params.lang === "all" ? SEARCH_OPTIONS.join(",") : params.lang;

    let url = resolve(
        `/api/search/${langs}/${encodeURIComponent(params.search)}`,
    );
    const res = await fetch(url);

    if (!res.ok) {
        // console.debug("DEBUG:", await res.text());
        error(res.status, "fetch to api failed");
    }
    const lemmas = SearchResponse.parse(await res.json());
    // console.log(lemmas);

    if (lemmas && lemmas.length === 1) {
        redirect(307, resolve(`/lookup/${params.lang}/${params.search}`));
    }

    return { lemmas };
};
