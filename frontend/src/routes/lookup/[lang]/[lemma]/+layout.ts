import { resolve } from "$app/paths";
import { LookupResponse, SEARCH_LANGS } from "$lib/utils";
import { error } from "@sveltejs/kit";
import type { LayoutLoad } from "./$types";

export const load: LayoutLoad = async ({ params, fetch }) => {
    const langs = params.lang === "all" ? SEARCH_LANGS.join(",") : params.lang;

    let url = resolve(
        `/api/lookup/${langs}/${encodeURIComponent(params.lemma)}`,
    );
    const res = await fetch(url);
    if (!res.ok) {
        error(res.status, "fetch to api failed");
    }
    const entries = LookupResponse.parse(await res.json());

    return { entries };
};
