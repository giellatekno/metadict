<script lang="ts">
    import { page } from "$app/stores";
    export let data;

    let rendered: string | undefined;
    $: rendered = data.rendered
</script>

{#if rendered}
    {@html rendered}
{/if}
