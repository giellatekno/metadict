<script lang="ts">
    import { resolve } from "$app/paths";
    import { m } from "$lib/paraglide/messages";

    const examples = [
        { query: "%laš", text: m.wildcard_example_1 },
        { query: "ráhkis%", text: m.wildcard_example_2 },
        { query: "muit%hit", text: m.wildcard_example_3 },
        { query: "jie_na", text: m.wildcard_example_4 },
    ];
</script>

<div
    class="card preset-filled-tertiary-50-950 flex w-full max-w-360 flex-col gap-4 overflow-auto p-4 shadow-lg"
>
    <div class="flex flex-col gap-2">
        <h3 class="h3">{m.about_metadict_title()}</h3>
        <p>{m.about_metadict_body()}</p>
    </div>
    <div class="flex flex-col gap-2">
        <h3 class="h3">{m.searching_title()}</h3>
        <p>{m.searching_body()}</p>
    </div>
    <div class="flex flex-col gap-2">
        <div class="flex flex-col gap-2">
            <h3 class="h3">{m.advanced_search_title()}</h3>
            <span>
                {m.advanced_search_body_1()}
                <code class="code">%</code>
                {m.advanced_search_body_2()}
                <code class="code">_</code>
                {m.advanced_search_body_3()}
            </span>
        </div>
        <div class="flex flex-col">
            <h5 class="h5">{m.wildcard_example_title()}</h5>
            <ul class="ml-5 list-outside list-disc">
                {#each examples as { query, text }}
                    <li class="py-1">
                        <span>{m.wildcard_example_start()}</span>

                        <span class="inline-flex items-baseline">
                            {m.open_quote()}
                            <a
                                href={resolve(
                                    `/search/all/${encodeURIComponent(query)}`,
                                )}
                                class="decoration-primary-500 underline decoration-2 underline-offset-6"
                            >
                                {query}
                            </a>
                            {m.close_quote()}
                        </span>

                        <span>{text()}</span>
                    </li>
                {/each}
            </ul>
        </div>
    </div>
    <div class="flex flex-col gap-2">
        <h3 class="h3">{m.howto_access_title()}</h3>
        <p>{m.howto_access_body()}</p>
    </div>
</div>
