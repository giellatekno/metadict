<script lang="ts">
    import { page } from "$app/stores";
    export let data;

    let rendered: string | undefined;
    $: rendered = data.rendered
        // .replaceAll("<br>", "\n")
        // .replaceAll("<", "&lt;")
        // .replaceAll(">", "&gt;")
        // .replaceAll("\n", "<br>");
</script>

{#if rendered}
    {@html rendered}
{/if}
