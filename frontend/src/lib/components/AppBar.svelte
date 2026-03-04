<script lang="ts">
    import { AppBar } from "@skeletonlabs/skeleton-svelte";
    import Profile from "./Profile.svelte";
    import SelectLocale from "./SelectLocale.svelte";
    import { m } from "$lib/paraglide/messages.js";
    import { resolve } from "$app/paths";
    import { Info, LogInIcon } from "lucide-svelte";
    import type { UserType } from "$lib/utils";

    interface Props {
        user?: UserType;
        redirect_uri: string;
    }

    let { user, redirect_uri }: Props = $props();
</script>

<AppBar class="preset-filled-surface-800-200">
    <AppBar.Toolbar class="mx-auto w-full grid-cols-[auto_auto] px-6">
        <AppBar.Headline>
            <a
                class="h2 text-surface-50-950 font-[Noto_Serif] font-medium"
                href={resolve("/")}
            >
                {m.page_title()}
            </a>
        </AppBar.Headline>
        <AppBar.Trail>
            <div class="flex items-center gap-10">
                <SelectLocale />

                <a href={resolve("/about")} class="btn text-lg hover:underline">
                    <Info />
                    {m.info()}
                </a>
                {#if user}
                    <Profile {user}></Profile>
                {:else}
                    <a
                        class="btn text-lg hover:underline"
                        href="https://github.com/login/oauth/authorize?scope=read:user%20read:repo&client_id=Iv1.f208b6793cca35ec&redirect_uri={redirect_uri}"
                    >
                        <LogInIcon />
                        {m.login()}
                    </a>
                {/if}
            </div>
        </AppBar.Trail>
    </AppBar.Toolbar>
</AppBar>
