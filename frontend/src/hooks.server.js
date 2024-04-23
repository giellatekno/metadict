import { redirect } from "@sveltejs/kit";

export async function handle({ event, resolve }) {
    const jwt = event.cookies.get("metadict-creds");
    console.log(jwt);
    if (jwt !== undefined) {
        const [header, content, signature] = jwt.split(".");
        const decoded_content = atob(content);
        const user = JSON.parse(decoded_content);
        event.locals.user = user;
    }
    const response = await resolve(event);
    return response;
}
