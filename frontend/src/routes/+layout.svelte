<script lang="ts">
    import { goto } from "$app/navigation";
    import WordInput from "$lib/components/WordInput.svelte";
    import LocaleSelector from "$lib/components/LocaleSelector.svelte";
    import { page } from "$app/stores";
    import { t } from "svelte-intl-precompile";

    let base = "";

    type User = {
        gh_fullname: string,
        gh_avatar_url: string,
        restricted_dicts: boolean,
    };
    let user: User | undefined;
    $: user = $page.data?.user;
    $: console.log(user);
    async function on_new_value({ detail }: { detail: string }) {
        const search_term = encodeURIComponent(detail);
        await goto(`/search/sme/${search_term}`);
    }
</script>

<svelte:head>
    <title>Giellatekno Metadictionary</title>
</svelte:head>

<div class="wrapper">
    <div>
        <LocaleSelector />
    </div>
    <header>
        <a class="big" href="{base}/">Giellatekno Metadictionary</a>
        <span style="display:inline-flex;align-items:flex-end;">
            {#if user}
                <span class="user">
                    <img class="gh_avatar" src="{user.gh_avatar_url}" alt="Github user avatar" />
                    <span class="name">{user.gh_fullname}</span>
                    <span style="margin: 0 1em;">{user.restricted_dicts ? "Access" : "No access"}</span>
                    <span><a href="/auth/logout">Logout</a></span>
                </span>
            {:else}
                <a class="small" href="https://github.com/login/oauth/authorize?scope=read:user%20read:repo&client_id=Iv1.f208b6793cca35ec">
                    Login with GitHub
                </a>
            {/if}
        </span>
        <!--<a class="small" href="{base}/all">{$t("dictionaries")}</a>-->
    </header>
    <div class="line"></div>
</div>

<div class="search-wrapper">
    Oppslagsform (bruk % for wildcard):
    <span>
        <WordInput 
            on:new-value={on_new_value}
        />
    </span>
    <span>
        <select>
            <option>Nordsamisk</option>
            <option>Lulesamisk</option>
            <option>Sørsamisk</option>
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

    header {
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

    span.user {
        display: inline-flex;
        align-items: center;
    }

    span.user > span.name {
        padding-left: 0.5em;
    }

    img.gh_avatar {
        border-radius: 50%;
        height: 1.5em;
    }
</style>

