import { env } from "$env/dynamic/public";
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
    const request = event.request;
    const { pathname } = event.url;

    if (pathname.startsWith("/api/")) {
        const api_endpoint = new URL(env.PUBLIC_API_ENDPOINT);
        const api_url = new URL(event.request.url);
        // anders: on server internal calls, it doesn't use https, right?
        //api_url.protocol = "http:";
        api_url.hostname = api_endpoint.host;
        api_url.port = api_endpoint.port;
        api_url.pathname = pathname.replace(/^\/api\//, "");

        const headers = new Headers(event.request.headers);
        //headers.set("host", env.PUBLIC_API_ENDPOINT);
        //headers.set('accept-encoding', '');
        const cookie = event.request.headers.get("Cookie");
        if (cookie !== null) {
            request.headers.set("Cookie", cookie);
        }
        
        const client_ip = event.request.headers.get("x-forwarded-for") || event.getClientAddress();
        if (client_ip) {
            headers.set("x-forwarded-for", client_ip);
        }

        const response = await fetch(api_url, {
            method: event.request.method,
            headers,
            body: event.request.body,
            //duplex: "half",
        });

        return response;
    }

    const jwt = event.cookies.get("metadict-creds");
    if (jwt !== undefined) {
        const [_header, content, _signature] = jwt.split(".");
        const decoded_content = base64urldecode(content);
        const user = JSON.parse(decoded_content);
        event.locals.user = user;
    }
    const response = await resolve(event);
    return response;
}

/*
export async function handleFetch({ event, request, fetch }) {
    // Make sure to send cookies when we fetch from our api
	if (request.url.startsWith(env.PUBLIC_API_ENDPOINT)) {
        const cookie = event.request.headers.get("Cookie");
        request.headers.set("Cookie", cookie);
	}

	return fetch(request, { credentials: "include" });
}
*/

// https://stackoverflow.com/questions/5234581/base64url-decoding-via-javascript
function base64urldecode(input: string) {
    // Replace non-url compatible chars with base64 standard chars
    input = input.replace(/-/g, "+").replace(/_/g, "/");

    // Pad out with standard base64 required padding characters
    var pad = input.length % 4;
    if (pad) {
        if (pad === 1) {
            throw new Error(
                "InvalidLengthError: Input base64url string is the wrong length to determine padding",
            );
        }
        input += new Array(5 - pad).join("=");
    }

    return atob(input);
}
