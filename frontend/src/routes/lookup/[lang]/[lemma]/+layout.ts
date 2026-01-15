import { resolve } from "$app/paths";
import type { LookupResponse } from "$lib/utils";
import { error } from "@sveltejs/kit";
import type { LayoutLoad } from "./$types";

export const load: LayoutLoad = async ({ params, fetch }) => {
    let url = resolve(
        `/api/lookup/${params.lang}/${encodeURIComponent(params.lemma)}`,
    );
    const res = await fetch(url);
    if (!res.ok) {
        error(res.status, "fetch to api failed");
    }
    const entries: LookupResponse = await res.json();

    return { entries };
};
