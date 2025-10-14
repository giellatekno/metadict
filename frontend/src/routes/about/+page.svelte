<script lang="ts">
    import { t } from "svelte-intl-precompile";
</script>

<div class="card w-full md:w-[42rem] flex flex-col my-2 px-2 pb-2">
    <span class="my-2">
        <h3 class="h3 pb-1 font-medium">{$t("howto-search-title")}</h3>
        <p>{$t("howto-search-body")}</p>
        <br />
        <ul>
            <li>
                "<b>%</b>laš" {$t("howto-search-example-end", {
                    values: { example: "laš" },
                })}
            </li>
            <li>
                "biila<b>%</b>" {$t("howto-search-example-start", {
                    values: { example: "biila" },
                })}
            </li>
            <li>
                "muit<b>%</b>it" {$t("howto-search-example-middle", {
                    values: { example_start: "muit", example_end: "it" },
                })}
            </li>
        </ul>
        <br />
    </span>
    <span class="my-2">
        <h3 class="h3 pb-1 font-medium">{$t("howto-access-title")}</h3>
        <p>{$t("howto-access-body")}</p>
    </span>
</div>
