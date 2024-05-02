export async function load({ url }) {
    const searchParams = url.searchParams;
    const description = searchParams.get("description") ?? "(no description)";
    const message = searchParams.get("message") ?? "(no message)";
    return { description, message };
}
