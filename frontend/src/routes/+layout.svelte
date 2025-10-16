<script lang="ts">
    import "../app.css";
    import { goto } from "$app/navigation";
    import { page } from "$app/state";
    import { resolve } from "$app/paths";
    import { t } from "svelte-intl-precompile";
    import { env } from "$env/dynamic/public";
    import Searchbar from "$lib/components/Searchbar.svelte";
    import AppBar from "$lib/components/AppBar.svelte";

    let { children } = $props();

    let search_lang = $state("sme");

    let redirect_uri = (() => {
        if (env.PUBLIC_API_ENDPOINT === undefined) {
            console.warn(
                "routes/+layout.svelte: env.PUBLIC_API_ENDPOINT is undefined, using default value of 'http://localhost:3000'",
            );
            return encodeURIComponent("http://localhost:3000/auth/callback");
        }
        return encodeURIComponent(env.PUBLIC_API_ENDPOINT + "/auth/callback");
    })();

    type User = {
        gh_fullname: string;
        gh_avatar_url: string;
        restricted_dicts: boolean;
    };
    let user: User | undefined = $derived(page.data?.user);

    async function on_new_value(detail: string) {
        const search_term = encodeURIComponent(detail);
        let url = resolve(`/search/${search_lang}/${search_term}`);
        // fix for seemingly working in dev but not prod:
        // on dev base="", so the url starts with a "/", but on
        // prod, we have a base, starting with NOT a "/", so we need
        // to add it here, so that we don't go to a relative url
        // if (!url.startsWith("/")) url = `/${url}`;
        console.log(url);
        await goto(url);
    }
</script>

<svelte:head>
    <title>{$t("page-title")}</title>
</svelte:head>

<AppBar {user} {redirect_uri} />

<div class="p-6">
    <Searchbar {on_new_value} bind:search_lang></Searchbar>
    <hr class="hr my-6" />
    {@render children?.()}
</div>
