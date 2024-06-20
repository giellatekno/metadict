import { env } from "$env/dynamic/public";
import { redirect } from "@sveltejs/kit";

export async function handle({ event, resolve }) {
    const jwt = event.cookies.get("metadict-creds");
    if (jwt !== undefined) {
        const [header, content, signature] = jwt.split(".");
        const decoded_content = base64urldecode(content);
        const user = JSON.parse(decoded_content);
        event.locals.user = user;
    }
    const response = await resolve(event);
    return response;
}

export async function handleFetch({ event, request, fetch }) {
    // Make sure to send cookies when we fetch from our api
	if (request.url.startsWith(env.PUBLIC_API_ENDPOINT)) {
        const creds = event.request.headers.get('metadict-creds');
		request.headers.set('metadict-creds', creds);
	}

	return fetch(request);
}

// https://stackoverflow.com/questions/5234581/base64url-decoding-via-javascript
function base64urldecode(input) {
    // Replace non-url compatible chars with base64 standard chars
    input = input.replace(/-/g, '+').replace(/_/g, '/');

    // Pad out with standard base64 required padding characters
    var pad = input.length % 4;
    if (pad) {
      if(pad === 1) {
        throw new Error('InvalidLengthError: Input base64url string is the wrong length to determine padding');
      }
      input += new Array(5-pad).join('=');
    }

    return atob(input);
}
