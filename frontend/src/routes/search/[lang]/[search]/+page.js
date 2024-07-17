import { error } from "@sveltejs/kit";
import { env } from "$env/dynamic/public";
import { browser, dev } from "$app/environment";

// argument to load() is an object:
// {  url: URL {
//     href: 'http://localhost:5173/search/sme/viessu',
//     origin: 'http://localhost:5173',
//     protocol: 'http:',
//     username: '',
//     password: '',
//     host: 'localhost:5173',
//     hostname: 'localhost',
//     port: '5173',
//     pathname: '/search/sme/viessu',
//     search: '',
//     searchParams: URLSearchParams {},
//     hash: ''
//   },
//   params: { lang: 'sme', search: 'viessu' },
//   data: null,
//   route: { id: '/search/[lang]/[search]' },
//   fetch: [Function (anonymous)],
//   setHeaders: [Function: setHeaders],
//   depends: [Function: depends],
//   parent: [AsyncFunction: parent],
//   untrack: [Function: untrack]
// }

export async function load(obj) {
    const { fetch, params, cookies } = obj;
    let { lang, search } = params;

    console.debug(`src/routes/search/[lang]/[search]/+page.js : load()`);
    console.debug(`env.PUBLIC_API_ENDPOINT = ${env.PUBLIC_API_ENDPOINT}`);
    let url = `${env.PUBLIC_API_ENDPOINT}/search/${lang}/${search}`;
    console.debug(`url = ${url}`);
    url = new URL(url);
    url = encodeURI(url);
    console.debug(`after encoding: url = ${url}`);
    const response = await fetch(url, { credentials: "include" });

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
        lang,
    };
}
