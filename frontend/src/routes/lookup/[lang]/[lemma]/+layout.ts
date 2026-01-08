import type { Load } from "@sveltejs/kit";
import { resolve } from "$app/paths";

export const load: Load = async ({ params, fetch }) => {
    let url = resolve(`/api/lookup/${params.lang}/${encodeURIComponent(params.lemma!)}`);
    const response = await fetch(url);
    const entries = await response.json();
    return { entries };
}
