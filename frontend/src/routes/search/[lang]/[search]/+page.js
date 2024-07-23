import { api_request } from "$lib/api_request.js";

export async function load(obj) {
    const { fetch, params, cookies } = obj;
    const { lang, search } = params;
    const objs = await api_request(`search/${lang}/${search}`);

    return { objs, lang };
}
