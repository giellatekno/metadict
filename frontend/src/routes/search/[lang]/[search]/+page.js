const API_ENDPOINT = "http://localhost:3000";

export async function load({ fetch, params }) {
    console.log("[lang]/[search]+page.js: load()");
    let { lang, search } = params;

    console.log("search term", search);

    let url = API_ENDPOINT + `/search/${lang}/${search}`;
    console.log("original url", url);
    url = encodeURI(url);
    console.log("encoded url", url);
    let resp = await fetch(url);

    let objs = await resp.json();
    return {
        objs,
    };
}
