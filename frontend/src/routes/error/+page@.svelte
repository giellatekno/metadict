<script lang="ts">
    let { description, message } = $props();
</script>

<div class="card p-5 w-fit">
    <h2 class="h2 text-error-500 font-medium">An error occured!</h2>
    <br />
    <h4 class="h4">Description:</h4>
    <p>{description}</p>
    <br />
    <h4 class="h4">Message:</h4>
    <p>{message}</p>
</div>
