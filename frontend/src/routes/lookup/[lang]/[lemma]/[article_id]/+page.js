import { api_request } from "$lib/api_request.js";

export async function load({ fetch, params }) {
    let { article_id } = params;
    const objs = await api_request(`article/${article_id}`);

    if (!Array.isArray(objs)) {
        return {
            error: `response from \"articles/${article_id}\" was not an array`,
        };
    }
    const rendered = objs[0];

    let neighbors = await api_request(`neighbors/${article_id}`);
    
    if (!Array.isArray(neighbors)) {
        return {
            error: `response from \"neighbors/${article_id}\" was not an array`,
        }
    }

    let dictionary = await api_request(`dictionary/${article_id}`)

    if (!Array.isArray(dictionary[0])) {
        return {
            error: `response from \"dictionary/${article_id}\" was not an array`,
        }
    }
    
    dictionary = dictionary[0]

    return {
        rendered, neighbors, dictionary
    };
}
