const API_ENDPOINT = "http://localhost:3000";

export async function load({ fetch, params }) {
    let { article_id } = params;

    let url = API_ENDPOINT + `/article/${article_id}`;
    url = encodeURI(url);

    let resp = await fetch(url);
    let objs = await resp.json();
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
