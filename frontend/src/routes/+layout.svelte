<script lang="ts">
    import "../app.css";
    import { goto } from "$app/navigation";
    import { page } from "$app/state";
    import { resolve } from "$app/paths";
    import { t } from "svelte-intl-precompile";
    import { PUBLIC_API_ENDPOINT } from "$env/static/public";
    import { env } from "$env/dynamic/public";
    import Searchbar from "$lib/components/Searchbar.svelte";
    import AppBar from "$lib/components/AppBar.svelte";

    let { children } = $props();

    let search_lang = $state("sme");

    //let redirect_uri = encodeURIComponent(PUBLIC_API_ENDPOINT + "/api/auth/callback");
    let redirect_uri = encodeURIComponent(env.PUBLIC_ORIGIN + resolve("/api/auth/callback"));

    type User = {
        gh_fullname: string;
        gh_avatar_url: string;
        restricted_dicts: boolean;
    };
    let user: User | undefined = $derived(page.data?.user);

    async function on_new_value(input: string) {
        await goto(resolve(`/search/${search_lang}/${encodeURIComponent(input)}`));
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
