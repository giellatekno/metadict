import { resolve } from "$app/paths";
import { SEARCH_OPTIONS } from "$lib/utils";
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

    let url = resolve(`/api/lookup/${params.lang}/${encodeURIComponent(params.lemma)}`);
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

    const parsed = LookupResponse.safeParse(json);
    if (!parsed.success) {
        console.error(parsed.error);
        error(502, "bad response from api");
    }

    return { entries: parsed.data };
};
