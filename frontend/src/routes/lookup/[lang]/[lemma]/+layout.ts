import { api_fetch, SEARCH_OPTIONS } from "$lib/utils";
import { LookupResponse } from "$lib/schemas";
import { error } from "@sveltejs/kit";
import type { LayoutLoad } from "./$types";

export const load: LayoutLoad = async ({ params, fetch }) => {
    // Verify langs in url are valid
    if (!SEARCH_OPTIONS.includes(params.lang)) {
        error(
            400,
            "Can only lookup one of the known langs: " + SEARCH_OPTIONS.join(", "),
        );
    }

    const result = await api_fetch(
        `lookup/${params.lang}/${encodeURIComponent(params.lemma)}`,
        fetch,
        LookupResponse,
    );

    return { entries: result };
};
