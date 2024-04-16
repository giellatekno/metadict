<script lang="ts">
    import WordInput from "$lib/components/WordInput.svelte";
    import LocaleSelector from "$lib/components/LocaleSelector.svelte";
    import { t } from "svelte-intl-precompile";

    let results: Array<string> = [];
    let search_results: Array<string> = [];
    let selected_term: string | null = null;
    let saved_search_results: Array<string> = [];

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

    function random_list(n: number) {
        let res = [];
        for (let i = 0; i < n; i++) {
            res.push(random_string(10));
        }
        return res;
    }

    function on_new_value() {
        search_results = random_list(10);
    }

    function on_select_term(term: string) {
        saved_search_results = [...search_results];
        selected_term = term;
        search_results = [selected_term];
    }

    function reexpand() {
        search_results = [...saved_search_results];
        saved_search_results = [];
        selected_term = null;
    }
</script>


<main class="results">
    <div class="search-hits">
        <ul class="clean">
            {#each search_results as res}
                <li>
                    <a href="/sme/{res}">{res}</a>
                </li>
            {/each}
            <span on:click={reexpand}>Reexpand</span>
        </ul>
    </div>

    {#if selected_term}
        <div class="left">
            <h3>{selected_term}</h3>
            <ul>
                {#each results as string, index}
                    <li>Item: {string} ({index})</li>
                {/each}
            </ul>
        </div>

        <div class="right">
            ARTIKKEL HER
        </div>
    {/if}
</main>

<style>
    main.results {
        width: 100vw;
        display: grid;
        grid-template-areas:
            'search search search'
            'results results results'
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

    div.search-hits {
        grid-area: results;
    }

    ul.clean {
        list-style: none;
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

    a {
        font-family: verdana;
    }

    a:visited {
        color: blue;
    }


    main {
        display: flex;
        justify-content: center;
    }
</style>
