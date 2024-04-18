<script lang="ts">
    import { goto } from "$app/navigation";
    import WordInput from "$lib/components/WordInput.svelte";
    import LocaleSelector from "$lib/components/LocaleSelector.svelte";
    import { t } from "svelte-intl-precompile";

    let base = "";

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
</style>

