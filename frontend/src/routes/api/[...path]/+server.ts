import type { RequestHandler } from './$types';
import { PUBLIC_API_ENDPOINT } from "$env/static/public";
import { base } from "$app/paths";

export const GET: RequestHandler = async ({ request, url, fetch }) => {
    const pathname = url.pathname;

    const api_url = new URL(PUBLIC_API_ENDPOINT);

    api_url.search = url.search;
    // Strip the leading BASE/api from the pathname before we send the query to the API
    // note: the "base" variable (from "$app/paths") is deprecated (for some mystical
    // reason..), hence the warning. It is impossible to silence it.
    api_url.pathname = strip_prefix(`${base}/api`, url.pathname);

    const headers = new Headers(request.headers);
    //headers.set("host", env.PUBLIC_API_ENDPOINT);
    //headers.set('accept-encoding', '');
    const cookie = request.headers.get("Cookie");
    if (cookie !== null) {
        headers.set("Cookie", cookie);
    }
    
    const client_ip = request.headers.get("x-forwarded-for");// || event.getClientAddress();
    if (client_ip) {
        headers.set("x-forwarded-for", client_ip);
    }

    console.debug(`DEBUG: api call (from "${pathname}") to ${api_url}`);
    const response = await fetch(api_url, {
        method: request.method,
        headers,
        body: request.body,
        //duplex: "half",
    });

    return response;
};

function strip_prefix(prefix: string, str: string): string {
    console.assert(str.startsWith(prefix));
    return str.slice(prefix.length);
}
