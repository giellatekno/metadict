<script lang="ts">
    import { t } from 'svelte-intl-precompile';
    // Data from +page.js load()
    export let data;
</script>

<p>
    {$t("search-result", { values: { count: data.objs.length } })}
    <!-- Found {data.objs.length} lemma{plural ? "s" : ""} throughout all
    dictionaries that matched the search. -->
</p>

<main>
    {#each data.objs as lemma}
        <span><a href="/lookup/{data.lang}/{lemma}">{lemma}</a></span>
    {/each}
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
    }

    span {
        padding: 6px;
    }

    span > a {
        margin-left: 12px;
    }
</style>
