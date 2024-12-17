import { goto } from "$app/navigation";
import { base } from "$app/paths";
import { api_request } from "$lib/api_request";

export async function load(obj) {
    const { fetch, params } = obj;
    const { lang, search } = params;

    const search_encoded = encodeURIComponent(search)

    const objs = await api_request(`search/${lang}/${search_encoded}`);

    if (objs.length === 1) {
        goto(`${base}/lookup/${lang}/${search}`)
    }

    return { objs, lang };
}
