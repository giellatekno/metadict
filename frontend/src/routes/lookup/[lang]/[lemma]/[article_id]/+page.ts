import { error } from "@sveltejs/kit";
import { await_or_error } from "$lib/await_or_error";
import { resolve } from "$app/paths";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, fetch }) => {
    let { article_id } = params;

    const urls = [
        `article/${article_id}`,
        `neighbors/${article_id}`,
        `dictionary/${article_id}`,
    ];

    const responses = await await_or_error(
        Promise.all(urls.map((url) => fetch(`${resolve("/api")}/${url}`))),
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

    const [articles, neighbors, dictionary] = jsons;

    return {
        rendered: articles[0], // only one article is returned
        neighbors,
        dictionary: dictionary[0], // only one dictionary entry is returned
    };
};
