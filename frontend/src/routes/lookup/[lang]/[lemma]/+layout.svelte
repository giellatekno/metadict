<script lang="ts">
    import { page } from "$app/stores";
    import { t } from "svelte-intl-precompile";
    export let data;

    const { lang, lemma, article_id } = $page.params;
    const n_dicts = data.objs.length;
    const singular = n_dicts === 1;
</script>

<p>
    {$t("lookup-result", { values: { lemma: lemma, count: n_dicts } })}
    <!-- The search key "{lemma}" was found in {n_dicts}
    {singular ? "dictionary" : "dictionaries"}. -->
</p>

<main class="container">
    <div class="k1">
        {#each data.objs as [lemma, dictionary_name, article_id]}
            <span>
                <a href="/lookup/{lang}/{lemma}/{article_id}">
                    {lemma}
                </a>
                ({dictionary_name})
            </span>
        {/each}
    </div>

    <div class="k2">
        <slot></slot>
    </div>
</main>


<style>
    main.container {
        width: 100vw;
        display: grid;
        grid-template-columns: 1fr 2fr;
    }

    div.k1 {
        display: flex;
        flex-direction: column;
    }

    div.k2 {
        display: flex;
    }

    span {
        padding: 6px;
    }

    span > a {
        margin-left: 12px;
    }
</style>
