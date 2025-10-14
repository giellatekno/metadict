import { api_request } from "$lib/api_request";

export async function load({ params }) {
    let { article_id } = params;

    const objs = await Promise.all([
        api_request(`article/${article_id}`),
        api_request(`neighbors/${article_id}`),
        api_request(`dictionary/${article_id}`),
    ]);

    if (!Array.isArray(objs[0])) {
        return {
            error: `response from \"article/${article_id}\" was not an array`,
        };
    }

    if (!Array.isArray(objs[1])) {
        return {
            error: `response from \"neighbors/${article_id}\" was not an array`,
        };
    }

    if (!Array.isArray(objs[2])) {
        return {
            error: `response from \"dictionary/${article_id}\" was not an array`,
        };
    }

    const rendered = objs[0][0]; // only one article is returned
    const neighbors = objs[1]; // array of neighboring articles
    const dictionary = objs[2][0]; // only one dictionary entry is returned

    return {
        rendered,
        neighbors,
        dictionary,
    };
}
