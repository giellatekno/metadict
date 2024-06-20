import { env } from "$env/dynamic/public";

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
    let url = `${env.PUBLIC_API_ENDPOINT}/search/${lang}/${search}`;
    url = encodeURI(url);
    const response = await fetch(url, { credentials: "include" });
    const objs = await response.json();

    return {
        objs,
        lang,
    };
}
