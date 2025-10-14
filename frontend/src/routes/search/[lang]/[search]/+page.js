import { resolve } from "$app/paths";
import { api_request } from "$lib/api_request";
import { redirect } from "@sveltejs/kit";

export async function load({ params }) {
    const search_encoded = encodeURIComponent(params.search);

    const lemmas = await api_request(`search/${params.lang}/${search_encoded}`);

    if (lemmas.length === 1) {
        redirect(307, resolve(`/lookup/${params.lang}/${params.search}`));
    }
    return { lemmas };
}
