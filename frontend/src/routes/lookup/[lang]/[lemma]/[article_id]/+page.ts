import type { Load } from "@sveltejs/kit";
import { error } from '@sveltejs/kit';
import { await_or_error } from "$lib/await_or_error";
import { resolve } from "$app/paths";

export const load: Load = async ({ params, fetch }) => {
    let { article_id } = params;

    const urls = [
        `/api/article/${article_id}`,
        `/api/neighbors/${article_id}`,
        `/api/dictionary/${article_id}`,
    ];

    const responses = await await_or_error(
        Promise.all(urls.map((url) => fetch(resolve(url)))),
        "fetch to api failed",
    );

    const jsons = await await_or_error(
        Promise.all(responses.map((response) => response.json())),
        "decoding json from api failed",
    );

    for (let i = 0; i < urls.length; i++) {
        if (!Array.isArray(jsons[i])) {
            error(500, `response from "${urls[i]}" was not an array`);
        }
    }

    const [ articles, neighbors, dictionary ] = jsons;

    return {
        rendered: articles[0], // only one article is returned
        neighbors,
        dictionary: dictionary[0], // only one dictionary entry is returned
    };
}
