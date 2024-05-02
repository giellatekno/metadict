const API_ENDPOINT = "http://localhost:3000";

export async function load({ fetch, params }) {
    let { lang, search } = params;

    let url = API_ENDPOINT + `/search/${lang}/${search}`;
    url = encodeURI(url);

    let resp = await fetch(url, { credentials: "include" });

    let objs = await resp.json();
    return {
        objs,
    };
}
