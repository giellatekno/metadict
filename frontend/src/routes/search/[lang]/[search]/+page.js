import { env } from "$env/dynamic/public";

export async function load({ fetch, params, cookies }) {
    let { lang, search } = params;
    let url = `${env.PUBLIC_API_ENDPOINT}/search/${lang}/${search}`;
    url = encodeURI(url);
    const request = new Request(url, { credentials: "include" });
    console.log("routes/search/[lang]/[search]/+page.js: request:");
    console.log(request);
    console.log("cookies");
    console.log(cookies);
    const response = await fetch(request);
    const objs = await response.json();
    return {
        objs,
    };
}
