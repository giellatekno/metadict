<script lang="ts">
    import { goto } from "$app/navigation";
    import WordInput from "$lib/components/WordInput.svelte";
    import Profile from "$lib/components/Profile.svelte";
    import LocaleSelector from "$lib/components/LocaleSelector.svelte";
    import { page } from "$app/stores";
    import { base } from "$app/paths";
    import { t, locale } from "svelte-intl-precompile";
    import { langname } from "$lib/langname";
    import { env } from "$env/dynamic/public";

    let search_lang = "sme";

    let redirect_uri = env.PUBLIC_API_ENDPOINT;
    if (redirect_uri === undefined) {
        console.warn("routes/+layout.svelte: env.PUBLIC_API_ENDPOINT is undefined, using default value of 'http://localhost:3000'");
        redirect_uri = "http://localhost:3000";
    }
    redirect_uri = encodeURIComponent(redirect_uri + "/auth/callback");

    type User = {
        gh_fullname: string,
        gh_avatar_url: string,
        restricted_dicts: boolean,
    };
    let user: User | undefined;
    $: user = $page.data?.user;
    async function on_new_value({ detail }: { detail: string }) {
        const search_term = encodeURIComponent(detail);
        let url = `${base}/search/${search_lang}/${search_term}`;
        // fix for seemingly working in dev but not prod:
        // on dev base="", so the url starts with a "/", but on
        // prod, we have a base, starting with NOT a "/", so we need
        // to add it here, so that we don't go to a relative url
        if (!url.startsWith("/")) url = `/${url}`;
        await goto(url);
    }
</script>

<svelte:head>
    <title>{$t("page-title")}</title>
</svelte:head>

<div class="wrapper">
    <div>
        <LocaleSelector />
    </div>
    <header>
        <a class="big" href="{base}/">{$t("page-title")}</a>
        <span style="margin-left: auto; display:inline-flex;align-items:flex-end;">
            {#if user}
                <Profile user={user} />
            {:else}
                <a class="small" href="https://github.com/login/oauth/authorize?scope=read:user%20read:repo&client_id=Iv1.f208b6793cca35ec&redirect_uri={redirect_uri}">
                {$t("login")}
                </a>
            {/if}
        </span>
    </header>
    <div class="line"></div>
</div>

<div class="search-wrapper">
    <p class="search-info">
        {$t("dictionary-form")} (%):
    </p>
    <span>
        <WordInput 
            on:new-value={on_new_value}
        />
    </span>
    <span>
        <label for="search-lang-selector">{$t("search-language")}</label>
        <select class="search-lang-selector"
            bind:value={search_lang}>
            <option value="sme">{langname("sme", $locale)}</option>
            <option value="nob">{langname("nob", $locale)}</option>
            <option value="fin">{langname("fin", $locale)}</option>
        </select>
    </span>
</div>

<slot></slot>

<style>
    div.wrapper {
        margin: 8px;
        width: calc(100vw - 16px);
    }

    div.line {
        border-bottom: 1px solid silver;
        width: calc(100vw - 16px);
    }

    div.search-wrapper {
        display: inline-flex;
        margin: 10px 0 0 30px;
    }

    header {
        display: flex;
        padding-bottom: 8px;
        margin: 5px 0 0 20px;
    }

    a.big {
        color: black;
        text-decoration: none;
        font-family: verdana;
        font-size: 26px;
        font-weight: 100;
    }

    a.small {
        font-size: 16px;
        margin-left: 16px;
    }

    label {
        font-size: 0.8rem;
        display: block;
        margin-left: 8px;
    }

    select.search-lang-selector {
        margin-left: 8px;
    }
    
    p.search-info {
        margin: 10px 8px 0 0 
    }

</style>
