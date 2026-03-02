import type { Load } from "@sveltejs/kit";
import { error } from "@sveltejs/kit";
import { resolve } from "$app/paths";
import {
    ArticleResponse,
    DictionaryResponse,
    NeighborsResponse,
} from "$lib/utils";

export const load: Load = async ({ params, fetch }) => {
    let { article_id } = params;

    const urls = [
        `article/${article_id}`,
        `neighbors/${article_id}`,
        `dictionary/${article_id}`,
    ];

    const responses = await Promise.all(
        urls.map((url) => fetch(resolve(`/api/${url}`))),
    );

    responses.forEach((res) => {
        if (!res.ok) {
            error(res.status, "fetch to api failed");
        }
    });

    const jsons = await Promise.all(
        responses.map((response) => response.json()),
    );

    urls.forEach((url, i) => {
        if (!Array.isArray(jsons[i])) {
            error(500, `response from "${url}" was not an array`);
        }
    });

    const article = ArticleResponse.parse(jsons[0]);
    const neighbors = NeighborsResponse.parse(jsons[1]);
    const dictionary = DictionaryResponse.parse(jsons[2]);

    return {
        rendered: article[0], // only one article is returned
        neighbors,
        dictionary: dictionary[0], // only one dictionary entry is returned
    };
};
