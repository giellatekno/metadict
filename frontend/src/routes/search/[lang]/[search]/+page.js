import { env } from "$env/dynamic/public";

export async function load({ fetch, params }) {
    let { lang, search } = params;

    let url = `${env.PUBLIC_API_ENDPOINT}/search/${lang}/${search}`;
    url = encodeURI(url);

    let resp = await fetch(url, { credentials: "include" });

    let objs = await resp.json();
    return {
        objs,
    };
}
