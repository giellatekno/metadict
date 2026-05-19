<script lang="ts">
    import "../app.css";
    import { page } from "$app/state";
    import { resolve } from "$app/paths";
    import { m } from "$lib/paraglide/messages.js";
    import { env } from "$env/dynamic/public";
    import Searchbar from "$lib/components/Searchbar.svelte";
    import AppBar from "$lib/components/AppBar.svelte";
    import { User } from "$lib/utils";
    import Footer from "$lib/components/Footer.svelte";

    let { children } = $props();

    let redirect_uri = encodeURIComponent(
        env.PUBLIC_ORIGIN + resolve("/api/auth/callback"),
    );

    let user = $derived.by(() => {
        if (!page.data?.user) return undefined;
        return User.parse(page.data.user);
    });
</script>

<svelte:head>
    <title>{m.page_title()}</title>
</svelte:head>

<div class="app flex h-full min-h-screen w-full flex-col items-center">
    <AppBar {user} {redirect_uri} />

    <div
        class="flex h-fit w-full flex-1 flex-col items-center gap-6 p-2 pb-16 sm:p-6"
    >
        <Searchbar />
        <hr class="hr" />
        <div class="flex w-full max-w-480 flex-col items-center">
            {@render children?.()}
        </div>
    </div>

    <Footer />
</div>
