import { api_request } from "$lib/api_request.js";

export async function load({ fetch, params }) {
    const { lang, lemma } = params;
    const objs = await api_request(`lookup/${lang}/${lemma}`);
    return { objs };
}
