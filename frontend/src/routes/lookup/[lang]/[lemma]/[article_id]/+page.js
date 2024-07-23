import { error } from "@sveltejs/kit";
import { env } from "$env/dynamic/public";
import { browser, dev } from "$app/environment";

export async function load({ fetch, params }) {
    let { article_id } = params;
    let url = `${env.PUBLIC_API_ENDPOINT}/article/${article_id}`;
    url = new URL(url);
    url = encodeURI(url);
    let response = await fetch(url, { credentials: "include" });
    if (response.status !== 200) {
        error(response.status, "non-200 when calling api");
    }
    const objs = await response.json();

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
