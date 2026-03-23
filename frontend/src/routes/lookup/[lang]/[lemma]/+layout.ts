import { resolve } from "$app/paths";
import { SEARCH_OPTIONS, LookupResponse } from "$lib/utils";
import { error } from "@sveltejs/kit";
import type { LayoutLoad } from "./$types";

export const load: LayoutLoad = async ({ params, fetch }) => {
    if (!SEARCH_OPTIONS.includes(params.lang)) {
        error(
            400,
            "Can only lookup one of the known langs: " +
                SEARCH_OPTIONS.join(", "),
        );
    }

    let url = resolve(
        `/api/lookup/${params.lang}/${encodeURIComponent(params.lemma)}`,
    );
    const res = await fetch(url);
    if (!res.ok) {
        error(res.status, "fetch to api failed");
    }
    const entries = LookupResponse.parse(await res.json());

    return { entries };
};
