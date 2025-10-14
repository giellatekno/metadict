<script lang="ts">
    import { locale } from "$lib/locale.js";
    import { popup, ListBox, ListBoxItem } from "@skeletonlabs/skeleton";
    import type { PopupSettings } from "@skeletonlabs/skeleton";
    import languageIcon from "$assets/language.svg";
    import { langname } from "$lib/langname";

    const LOCALES = [
        { iso: "nob", display: "Norsk Bokmål" },
        { iso: "eng", display: "English" },
        { iso: "sme", display: "Davvisámegiella" },
    ];

    const langPopupClick: PopupSettings = {
        event: "click",
        target: "langPopupClick",
        placement: "bottom",
    };
</script>

<button class="btn variant-filled-tertiary" use:popup={langPopupClick}>
    <img alt="Innholdspråk" src={languageIcon} height="22" />
    <span>{langname($locale, $locale)}</span>
</button>

<div
    class="card p-4 w-fit shadow-xl variant-filled-tertiary"
    data-popup="langPopupClick"
>
    <ListBox>
        {#each LOCALES as { iso, display }}
            <ListBoxItem bind:group={$locale} name="lang" value={iso}>
                {display}
            </ListBoxItem>
        {/each}
    </ListBox>
    <div class="arrow variant-filled-tertiary"></div>
</div>
