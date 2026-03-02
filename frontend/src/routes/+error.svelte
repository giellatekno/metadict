<script lang="ts">
    import { page } from "$app/state";
</script>

<div class="my-8 flex flex-col items-center">
    <div
        class="border-error-500 bg-tertiary-50-950 card flex max-w-xl min-w-sm flex-col items-center gap-2 border-2 p-4 text-center shadow-lg"
    >
        <h3 class="h3 text-error-500 font-bold">
            Error {page.status}
        </h3>
        <h5 class="h5 text-surface-contrast-50-950">{page.error?.message}</h5>
    </div>
</div>
