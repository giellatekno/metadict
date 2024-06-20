import { env } from "$env/dynamic/public";

export async function load({ fetch, params }) {
    let { lang, lemma } = params;
    let url = `${env.PUBLIC_API_ENDPOINT}/lookup/${lang}/${lemma}`;
    url = encodeURI(url);
    let resp = await fetch(url);
    let objs = await resp.json();
    return {
        objs,
    };
}
