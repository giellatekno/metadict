import type { RequestHandler } from "./$types";
import { PUBLIC_API_ENDPOINT } from "$env/static/public";

export const GET: RequestHandler = async ({ params, request, url, fetch }) => {
    const pathname = url.pathname;

    const api_url = new URL(PUBLIC_API_ENDPOINT);

    api_url.search = url.search;
    console.debug(params.path);
    api_url.pathname = `/${params.path}`;

    const headers = new Headers(request.headers);
    //headers.set("host", env.PUBLIC_API_ENDPOINT);
    //headers.set('accept-encoding', '');
    const cookie = request.headers.get("Cookie");
    if (cookie !== null) {
        headers.set("Cookie", cookie);
    }

    const client_ip = request.headers.get("x-forwarded-for"); // || event.getClientAddress();
    if (client_ip) {
        headers.set("x-forwarded-for", client_ip);
    }

    console.debug(`DEBUG: api call (from "${pathname}") to ${api_url}`);
    const response = await fetch(api_url, {
        method: request.method,
        headers,
        body: request.body,
        // Don't follow the redirect, but return in from
        // this endpoint instead
        redirect: "manual",
        //duplex: "half",
    });

    return response;
};
