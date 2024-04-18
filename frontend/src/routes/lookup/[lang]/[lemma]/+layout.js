const API_ENDPOINT = "http://localhost:3000";

export async function load({ fetch, params }) {
    let { lang, lemma } = params;

    let url = API_ENDPOINT + `/lookup/${lang}/${lemma}`;
    url = encodeURI(url);

    let resp = await fetch(url);
    let objs = await resp.json();
    return {
        objs,
    };
}
