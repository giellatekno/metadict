<script lang="ts">
    import { m } from "$lib/paraglide/messages";
</script>

<div class="card w-full md:w-2xl flex flex-col my-2 px-2 pb-2">
    <span class="my-2">
        <h3 class="h3 pb-1 font-medium">{m.howto_search_title()}</h3>
        <p>{m.howto_search_body()}</p>
        <br />
        <ul>
            <li>
                "<b>%</b>laš" {m.howto_search_example_end({ example: "laš" })}
            </li>
            <li>
                "biila<b>%</b>" {m.howto_search_example_start({ example: "biila" })},
            </li>
            <li>
                "muit<b>%</b>it" {m.howto_search_example_middle({ example_start: "muit", example_end: "it" })}
            </li>
        </ul>
        <br />
    </span>
    <span class="my-2">
        <h3 class="h3 pb-1 font-medium">{m.howto_access_title()}</h3>
        <p>{m.howto_access_body()}</p>
    </span>
</div>
