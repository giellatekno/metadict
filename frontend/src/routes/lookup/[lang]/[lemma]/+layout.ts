import { resolve } from "$app/paths";
import { await_or_error } from "$lib/await_or_error";
import type { DictionaryEntries } from "$lib/utils";
import type { LayoutLoad } from "./$types";

export const load: LayoutLoad = async ({ params, fetch }) => {
    let url = resolve(
        `/api/lookup/${params.lang}/${encodeURIComponent(params.lemma)}`,
    );
    const response = await await_or_error(fetch(url), "fetch to api failed");
    const entries: DictionaryEntries = await await_or_error(
        response.json(),
        "decoding json from api failed",
    );
    return { entries };
};
