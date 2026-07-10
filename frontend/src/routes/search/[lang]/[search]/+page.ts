import type { PageLoad } from "./$types";
import { redirect } from "@sveltejs/kit";
import { resolve } from "$app/paths";
import { api_fetch, SEARCH_OPTIONS } from "$lib/utils";
import { SearchResponse } from "$lib/schemas";

export const load: PageLoad = async ({ params, fetch, url }) => {
    // "all" is a frontend shorthand which expands to full lang list for the api
    let langs = params.lang === "all" ? SEARCH_OPTIONS.join(",") : params.lang;

    // Forward the target-language filter (`l2`) so the API only returns lemmas
    // that have a translation into an enabled target language. Without it the
    // API defaults to all target languages.
    const l2 = url.searchParams.get("l2");
    const l2_query = l2 ? `?l2=${encodeURIComponent(l2)}` : "";

    const result = await api_fetch(
        `search/${langs}/${encodeURIComponent(params.search)}${l2_query}`,
        fetch,
        SearchResponse,
    );

    // Skip the results list when there is exactly one match and it is equal to the search
    // This is to make sure you get the list if you use wildcard symbols
    if (
        result.length === 1 &&
        result[0].lemma.toLowerCase() === params.search.toLowerCase()
    ) {
        redirect(
            307,
            resolve("/lookup/[lang]/[lemma]", {
                lang: result[0].lang,
                lemma: encodeURIComponent(result[0].lemma),
            }),
        );
    }

    return { lemmas: result };
};
