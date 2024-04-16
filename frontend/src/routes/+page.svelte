<script lang="ts">
    import WordInput from "$lib/components/WordInput.svelte";
    import LocaleSelector from "$lib/components/LocaleSelector.svelte";
    import { t } from "svelte-intl-precompile";

    const base = "";
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
    <main>
        <div class="content">
            <slot></slot>
        </div>
    </main>
</div>

<div class="centered">
    <WordInput />
</div>


<style>
    div.centered {
        width: 100vw;
        height: 40vh;
        display: grid;
        place-items: center center;
    }

    div.wrapper {
        width: calc(100vw - 6vw);
    }

    div.line {
        border-bottom: 1px solid silver;
        width: calc(100vw - 16px);
    }

    header {
        padding-bottom: 8px;
        margin: 5px 0 0 20px;
    }

    a {
        color: black;
        font-family: verdana;
    }

    a.big {
        text-decoration: none;
        font-family: verdana;
        font-size: 26px;
        font-weight: 100;
    }

    a.small {
        font-size: 16px;
        margin-left: 16px;
    }

    main {
        display: flex;
        justify-content: center;
    }

    div.content {
        width: min(max(a, b), c);
        /*width: 50%;*/
    }

</style>
