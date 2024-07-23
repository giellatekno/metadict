import { api_request } from "$lib/api_request.js";

export async function load({ fetch, params }) {
    let { article_id } = params;
    const objs = await api_request(`article/${article_id}`);

    if (!Array.isArray(objs)) {
        return {
            error: `response from \"articles/[article_id]\" was not an array`,
        };
    }
    const rendered = objs[0];

    let neighbors = await api_request(`neighbors/${article_id}`);
    
    if (!Array.isArray(neighbors)) {
        return {
            error: `response from \"neighbors/[article_id]\" was not an array`,
        }
    }

    return {
        rendered, neighbors
    };
}
