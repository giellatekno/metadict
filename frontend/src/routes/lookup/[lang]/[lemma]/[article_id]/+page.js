import { api_request } from "$lib/api_request.js";

export async function load({ fetch, params }) {
    let { article_id } = params;
    const objs = await api_request(`article/${article_id}`);

    if (!Array.isArray(objs)) {
        return {
            error: `response from ${url} was not an array`,
        };
    }
    const rendered = objs[0];

    let neighbors_url = `${env.PUBLIC_API_ENDPOINT}/neighbors/${article_id}`;
    neighbors_url = new URL(neighbors_url)
    neighbors_url = encodeURI(neighbors_url)
    response = await fetch(neighbors_url, { credentials: "include" });
    if (response.status !== 200) {
        error(response.status, "non-200 when calling api");
    }
    const neighbors = await response.json();
    if (!Array.isArray(neighbors)) {
        return {
            error: `response from ${neighbors_url} was not an array`,
        }
    }

    return {
        rendered, neighbors
    };
}
