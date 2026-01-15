<script lang="ts">
    import { getLocale } from "$lib/paraglide/runtime.js";
    import { m } from "$lib/paraglide/messages.js";
    import { langname } from "$lib/langname";
    import { onMount } from "svelte";
    import { SearchIcon } from "lucide-svelte";
    import { goto } from "$app/navigation";
    import { resolve } from "$app/paths";

    let value = $state("");
    let search_lang = $state("sme");

    let search_input: HTMLInputElement;

    const extra_letters: Record<string, string[]> = {
        sme: ["á", "č", "đ", "ŋ", "š", "ŧ", "ž"],
        fin: ["ä", "ö", "å"],
        nob: ["æ", "ø", "å"],
    };

    async function on_new_value(input: string) {
        await goto(
            resolve(`/search/${search_lang}/${encodeURIComponent(input)}`),
            { keepFocus: true },
        );
    }

    function on_enter_keydown(event: KeyboardEvent) {
        if (event.key !== "Enter" || value === "") return;
        on_new_value(value);
        search_input.focus();
    }

    function on_searchbutton_click() {
        if (value === "") return;
        on_new_value(value);
        search_input.focus();
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
    <div class="mb-2 ml-[3.8rem] grid w-fit grid-cols-7 gap-1.5">
        {#each extra_letters[search_lang] as letter}
            <button
                class="btn btn-sm md:btn-base preset-outlined-primary-400-600 w-4 md:w-8"
                onclick={() => on_extra_letter(letter)}
            >
                {letter}
            </button>
        {/each}
    </div>
    <div
        class="input-group preset-filled-tertiary-50-950 h-12 w-full grid-cols-[auto_1fr_auto] md:h-16 md:w-2xl"
    >
        <button class="ig-cell" onclick={on_searchbutton_click}>
            <SearchIcon class="size-6" />
        </button>
        <input
            class="ig-input"
            bind:this={search_input}
            type="search"
            placeholder={m.search_placeholder()}
            bind:value
            onkeydown={on_enter_keydown}
        />
        <select
            class="ig-select"
            name="searchlang"
            id="searchlang"
            bind:value={search_lang}
        >
            <option value="sme">{langname("sme", getLocale())}</option>
            <option value="nob">{langname("nob", getLocale())}</option>
            <option value="fin">{langname("fin", getLocale())}</option>
        </select>
    </div>
</div>
