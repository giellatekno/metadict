<script lang="ts">
    import { AppBar } from "@skeletonlabs/skeleton-svelte";
    import Profile from "./Profile.svelte";
    import SelectLocale from "./SelectLocale.svelte";
    import { m } from "$lib/paraglide/messages.js";
    import { resolve } from "$app/paths";
    import { BookOpenText, Info, LogInIcon } from "@lucide/svelte";
    import type { UserType } from "$lib/utils";
    import { env } from "$env/dynamic/public";

    interface Props {
        user?: UserType;
    }

    let { user }: Props = $props();
    let redirect_uri = encodeURIComponent(
        env.PUBLIC_ORIGIN + resolve("/api/auth/callback"),
    );
</script>

<AppBar class="preset-filled-surface-800-200">
    <AppBar.Toolbar class="mx-auto w-full grid-cols-[auto_auto] sm:px-6">
        <AppBar.Headline>
            <a
                class="h2 text-surface-50-950 flex gap-2 font-[Noto_Serif] font-medium"
                href={resolve("/")}
            >
                <div
                    class="preset-filled-surface-800-200 border-surface-contrast-800-200 flex size-12 shrink-0 items-center justify-center rounded-full border-2"
                >
                    <BookOpenText class="size-8" />
                </div>
                <span class="hidden sm:inline">{m.page_title()}</span>
            </a>
        </AppBar.Headline>
        <AppBar.Trail>
            <div class="flex items-center gap-2 md:gap-10">
                <SelectLocale />

                <a href={resolve("/about")} class="btn text-lg hover:underline">
                    <Info />
                    <span class="hidden sm:inline">{m.info()}</span>
                </a>
                {#if user}
                    <Profile {user}></Profile>
                {:else}
                    <a
                        class="btn text-lg hover:underline"
                        href="https://github.com/login/oauth/authorize?scope=read:user%20read:repo&client_id=Iv1.f208b6793cca35ec&redirect_uri={redirect_uri}"
                    >
                        <LogInIcon />
                        <span class="hidden sm:inline">{m.login()}</span>
                    </a>
                {/if}
            </div>
        </AppBar.Trail>
    </AppBar.Toolbar>
</AppBar>
