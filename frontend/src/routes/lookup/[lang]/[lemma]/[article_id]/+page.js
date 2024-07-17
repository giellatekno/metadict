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
    return {
        rendered,
    };
}
