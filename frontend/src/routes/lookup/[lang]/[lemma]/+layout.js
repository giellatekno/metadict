import { error } from "@sveltejs/kit";
import { env } from "$env/dynamic/public";
import { browser, dev } from "$app/environment";

export async function load({ fetch, params }) {
    let { lang, lemma } = params;
    let url = `${env.PUBLIC_API_ENDPOINT}/lookup/${lang}/${lemma}`;
    url = new URL(url);
    url = encodeURI(url);
    let response = await fetch(url, { credentials: "include" });

    if (response.status !== 200) {
        error(response.status, "non-200 when calling api");
    }

    let objs;
    try {
        objs = await response.json();
    } catch (e) {
        error(500, "error when decoding json response body");
    }
    return {
        objs,
    };
}
