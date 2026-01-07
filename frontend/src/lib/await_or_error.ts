import { error } from "@sveltejs/kit";

export async function await_or_error<T>(promise: Promise<T>, message: string, code: number = 500) {
    try {
        return await promise;
    } catch (err) {
        error(code, `${message}: ${err}`);
    }
}
