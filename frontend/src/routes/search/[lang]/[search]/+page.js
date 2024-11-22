import { api_request } from "$lib/api_request.js";

export async function load(obj) {
    const { fetch, params } = obj;
    const { lang, search } = params;

    const search_encoded = encodeURIComponent(search)

    const objs = await api_request(`search/${lang}/${search_encoded}`);

    return { objs, lang };
}
