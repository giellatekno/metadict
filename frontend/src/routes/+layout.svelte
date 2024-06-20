<script lang="ts">
    import { goto } from "$app/navigation";
    import WordInput from "$lib/components/WordInput.svelte";
    import Profile from "$lib/components/Profile.svelte";
    import LocaleSelector from "$lib/components/LocaleSelector.svelte";
    import { page } from "$app/stores";
    import { base } from "$app/paths";
    import { t, locale } from "svelte-intl-precompile";
    import { langname } from "$lib/langname";

    let search_lang = "sme"

    type User = {
        gh_fullname: string,
        gh_avatar_url: string,
        restricted_dicts: boolean,
    };
    let user: User | undefined;
    $: user = $page.data?.user;
    // $: console.log(user);
    async function on_new_value({ detail }: { detail: string }) {
        const search_term = encodeURIComponent(detail);
        await goto(`${base}/search/${search_lang}/${search_term}`);
    }
</script>

<svelte:head>
    <title>{$t("title")}</title>
</svelte:head>

<div class="wrapper">
    <div>
        <LocaleSelector />
    </div>
    <header>
        <a class="big" href="{base}/">{$t("title")}</a>
        <span style="margin-left: auto; display:inline-flex;align-items:flex-end;">
            {#if user}
                <Profile user={user} />
            {:else}
                <a class="small" href="https://github.com/login/oauth/authorize?scope=read:user%20read:repo&client_id=Iv1.f208b6793cca35ec">
                {$t("login")}
                </a>
            {/if}
        </span>
    </header>
    <div class="line"></div>
</div>

<div class="search-wrapper">
    {$t("dictionaryform")} (%):
    <span>
        <WordInput 
            on:new-value={on_new_value}
        />
    </span>
    <span>
        <select
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

    span.user {
    }

</style>

