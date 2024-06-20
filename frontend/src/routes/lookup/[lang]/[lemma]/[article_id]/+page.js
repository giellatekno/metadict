import { env } from "$env/dynamic/public";

export async function load({ fetch, params }) {
    let { article_id } = params;
    let url = `${env.PUBLIC_API_ENDPOINT}/article/${article_id}`;
    url = encodeURI(url);
    const resp = await fetch(url, { credentials: "include" });
    const objs = await resp.json();

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
