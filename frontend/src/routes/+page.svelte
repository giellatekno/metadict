<script lang="ts">
    import WordInput from "$lib/components/WordInput.svelte";
    import LocaleSelector from "$lib/components/LocaleSelector.svelte";
    import { t } from "svelte-intl-precompile";

    let results: Array<string> = [];
    const base = "";
    const CHARS = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
        "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
        "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g",
        "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
        "s", "t", "u", "v", "w", "x", "y", "z",
    ];

    function random_string(length: number) {
        let out = [];
        for (let i = 0; i < length; i++) {
            const index = Math.ceil(Math.random() * CHARS.length);
            out.push(CHARS[index]);
        }

        return out.join("");
    }

    function random_list() {
        let res = [];
        for (let i = 0; i < 100; i++) {
            res.push(random_string(10));
        }
        return res;
    }

    function on_new_value() {
        results = random_list();
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
    <main>
        <div class="content">
            <slot></slot>
        </div>
    </main>
</div>

<main class="results">
    <div class="search-wrapper">
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

    <div class="left">
        <ul>
            {#each results as string, index}
                <li>Item: {string} ({index})</li>
            {/each}
        </ul>
    </div>

    <div class="right">
        ARTIKKEL HER
    </div>
</main>

<style>
    main.results {
        width: 100vw;
        display: grid;
        grid-template-areas:
            'search search search'
            'left right right';
    }

    div.search-wrapper {
        width: 100vw;
        grid-area: search;
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        justify-items: center;
        align-items: center;
    }

    div.search-wrapper > span:nth-child(1) {
        grid-column-start: 3;
        margin-left: auto;
    }

    div.left {
        grid-area: left;
        border: 2px solid red;
        overflow-y: scroll;
        height: 60vh;
    }

    div.right {
        grid-area: right;
        border: 2px solid blue;
        overflow-y: scroll;
    }

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
