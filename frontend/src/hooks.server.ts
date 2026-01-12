import { sequence } from "@sveltejs/kit/hooks";
import { paraglideMiddleware } from "$lib/paraglide/server";
import type { Handle } from "@sveltejs/kit";

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

const originalHandle: Handle = async ({ event, resolve }) => {
    const jwt = event.cookies.get("metadict-creds");

    if (jwt !== undefined) {
        const [_header, content, _signature] = jwt.split(".");
        const decoded_content = base64urldecode(content);
        const user = JSON.parse(decoded_content);

        event.locals.user = user;
    }

    const response = await resolve(event);

    return response;
};

const handleParaglide: Handle = ({ event, resolve }) =>
    paraglideMiddleware(event.request, ({ request, locale }) => {
        event.request = request;

        return resolve(event, {
            transformPageChunk: ({ html }) =>
                html.replace("%paraglide.lang%", locale),
        });
    });

export const handle = sequence(originalHandle, handleParaglide);
// https://stackoverflow.com/questions/5234581/base64url-decoding-via-javascript
// Replace non-url compatible chars with base64 standard chars
// Pad out with standard base64 required padding characters
