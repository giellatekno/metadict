<script lang="ts">
    // Data from +page.js load()
    export let data;

    const plural = data.objs.length != 1;
</script>

<p>
    Found {data.objs.length} lemma{plural ? "s" : ""} throughout all
    dictionaries that matched the search.
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
