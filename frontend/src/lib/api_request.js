import { error } from "@sveltejs/kit";
import { env } from "$env/dynamic/public";
import { browser, dev } from "$app/environment";

export async function api_request(path) {
    console.debug("lib/api_request.js :: api_request()");
    console.debug(`env.PUBLIC_API_ENDPOINT = ${env.PUBLIC_API_ENDPOINT}`);
    let url = new URL(`${env.PUBLIC_API_ENDPOINT}/${path}`);
    console.debug(`url = ${url}`);

    if (browser && !dev && url.hostname === "host.containers.internal") {
        // client-side, in production, the url cannot be
        // "host.containers.internal". We know that the only config that
        // has this, is anders' "local gtweb setup", so just change the
        // hostname to "localhost".
        console.debug("changing hostname of request from host.containers.internal to localhost");
        url.hostname = "localhost";
        url.pathname = "/metadict-api" + url.pathname;
        url.port = "80";
        console.debug(`(after changing) url = ${url}`);
    }

    let response;
    try {
        response = await fetch(url, { credentials: "include" });
    } catch (err) {
        error(500, `fetch() to api (${url}) failed`);
    }

    if (response.status !== 200) {
        error(500, `non-200 from api (actual code: ${response.status})`);
    }

    if (response.headers.get("Content-Type") !== "application/json") {
        error(500, "api response content-type was not 'application/json'");
    }

    let objs;
    try {
        objs = await response.json();
    } catch (err) {
        error(500, "error when decoding json response body");
    }

    console.debug("returning result from api_request()");
    return objs;
}
