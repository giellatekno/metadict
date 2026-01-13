<script lang="ts">
    import "../app.css";
    import { goto } from "$app/navigation";
    import { page } from "$app/state";
    import { resolve } from "$app/paths";
    import { m } from "$lib/paraglide/messages.js";
    import { env } from "$env/dynamic/public";
    import Searchbar from "$lib/components/Searchbar.svelte";
    import AppBar from "$lib/components/AppBar.svelte";
    import type { User } from "$lib/utils";
    import Footer from "$lib/components/Footer.svelte";

    let { children } = $props();
    let search_lang = $state("sme");

    let redirect_uri = encodeURIComponent(
        env.PUBLIC_ORIGIN + resolve("/api/auth/callback"),
    );

    let user: User | undefined = $derived(page.data?.user);

    async function on_new_value(input: string) {
        await goto(
            resolve(`/search/${search_lang}/${encodeURIComponent(input)}`),
        );
    }
</script>

<svelte:head>
    <title>{m.page_title()}</title>
</svelte:head>

<div class="app flex h-full min-h-screen flex-col">
    <AppBar {user} {redirect_uri} />

    <div class="flex h-fit flex-1 flex-col items-center p-6 pb-16">
        <Searchbar {on_new_value} bind:search_lang />
        <hr class="hr my-6" />
        {@render children?.()}
    </div>

    <Footer />
</div>
