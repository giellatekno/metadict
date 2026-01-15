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

    const b64_decoded = atob(input);

    // the input is utf-8 encoded, so we want to take all bytes, and decode them
    // as utf-8. TextDecoder.decode() requires a byte array (such as Uint8Array),
    // so first we must copy the b64_decoded string into the array, byte for byte
    const char_codes = new Uint8Array(b64_decoded.length);
    for (let i = 0; i < b64_decoded.length; i++) {
        char_codes[i] = b64_decoded.charCodeAt(i);
    }

    const decoder = new TextDecoder("utf-8");
    let utf8_decoded = decoder.decode(char_codes);

    return utf8_decoded;
}

/* from some stackoverflow post, unneeded
function fromBinary(encoded: any) {
  const binary = atob(encoded);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < bytes.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return String.fromCharCode(...new Uint16Array(bytes.buffer));
}
*/

const jwtHandle: Handle = async ({ event, resolve }) => {
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

export const handle = sequence(jwtHandle, handleParaglide);
// https://stackoverflow.com/questions/5234581/base64url-decoding-via-javascript
// Replace non-url compatible chars with base64 standard chars
// Pad out with standard base64 required padding characters
