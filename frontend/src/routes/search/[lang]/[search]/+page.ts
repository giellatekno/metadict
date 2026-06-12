import type { PageLoad } from "./$types";
import { error, redirect } from "@sveltejs/kit";
import { resolve } from "$app/paths";
import { SEARCH_OPTIONS } from "$lib/utils";
import { SearchResponse } from "$lib/schemas";

export const load: PageLoad = async ({ params, fetch }) => {
    // "all" is a frontend shorthand which expands to full lang list for the api
    let langs = params.lang === "all" ? SEARCH_OPTIONS.join(",") : params.lang;

    // Double encode because SvelteKit automatically decodes path params,
    // so a single encodeURIComponent would leave a bare % that breaks fetch
    let url = resolve(
        `/api/search/${langs}/${encodeURIComponent(encodeURIComponent(params.search))}`,
    );
    const res = await fetch(url);

    if (!res.ok) {
        error(res.status, "fetch to api failed");
    }

    let json: unknown;
    try {
        json = await res.json();
    } catch {
        error(502, "api returned non-JSON response");
    }

    const parsed = SearchResponse.safeParse(json);
    if (!parsed.success) {
        console.error(parsed.error);
        error(502, "bad response from api");
    }

    // Skip the results list when there is exactly one match
    if (parsed.data.length === 1) {
        redirect(
            307,
            resolve("/lookup/[lang]/[lemma]", {
                lang: parsed.data[0].lang,
                lemma: encodeURIComponent(parsed.data[0].lemma),
            }),
        );
    }

    return { lemmas: parsed.data };
};
