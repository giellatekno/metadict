<script lang="ts">
    import { t } from "svelte-intl-precompile";
</script>

<div class="card w-1/2 flex flex-col my-2 px-2">
    <span class="my-2">
        <h3 class="h3">{$t("howto-search-title")}</h3>
        <p>{$t("howto-search-body")}</p>
    </span>
    <span class="my-2">
        <h3 class="h3">{$t("howto-access-title")}</h3>
        <p>{$t("howto-access-body")}</p>
    </span>

</div>