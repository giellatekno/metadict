<script lang="ts">
    import { t, locale } from "svelte-intl-precompile";
    import { langname } from "$lib/langname";
    import { onMount } from "svelte";
    import { SearchIcon } from "lucide-svelte";

    interface Props {
        search_lang?: string;
        on_new_value: Function;
    }

    let { search_lang = $bindable("sme"), on_new_value }: Props = $props();

    let value = $state("");

    let search_input: HTMLInputElement;

    const extra_letters: { [id: string]: Array<string> } = {
        sme: ["á", "č", "đ", "ŋ", "š", "ŧ", "ž"],
        fin: ["ä", "ö", "å"],
        nob: ["æ", "ø", "å"],
    };

    function on_enter_keydown(event: KeyboardEvent) {
        if (event.key !== "Enter" || value === "") return;
        on_new_value(value);
    }

    function on_searchbutton_click() {
        if (value === "") return;
        on_new_value(value);
    }

    onMount(() => {
        search_input.focus();
    });

    function on_extra_letter(letter: string) {
        value += letter;
        search_input.focus();
    }
</script>

<div class="flex flex-col">
    <div
        class="input-group grid-cols-[auto_1fr_auto] w-full md:w-2xl h-12 md:h-16 preset-filled-tertiary-50-950"
    >
        <button class="ig-cell" onclick={on_searchbutton_click}>
            <SearchIcon class="size-6" />
        </button>
        <input
            class="ig-input"
            bind:this={search_input}
            type="search"
            placeholder={$t("search-placeholder")}
            bind:value
            onkeydown={on_enter_keydown}
        />
        <select
            class="ig-select"
            name="searchlang"
            id="searchlang"
            bind:value={search_lang}
        >
            <option value="sme">{langname("sme", $locale)}</option>
            <option value="nob">{langname("nob", $locale)}</option>
            <option value="fin">{langname("fin", $locale)}</option>
        </select>
    </div>
    <div class="ml-[3.8rem] mt-4 w-fit grid grid-cols-7 gap-1.5">
        {#each extra_letters[search_lang] as letter}
            <button
                class="btn btn-sm md:btn-base preset-outlined-primary-400-600"
                onclick={() => on_extra_letter(letter)}
            >
                {letter}
            </button>
        {/each}
    </div>
</div>
