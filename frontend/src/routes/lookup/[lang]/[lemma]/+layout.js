import { api_request } from "$lib/api_request";

export async function load({ params }) {
    return {
        entries: await api_request(`lookup/${params.lang}/${params.lemma}`),
    };
}
