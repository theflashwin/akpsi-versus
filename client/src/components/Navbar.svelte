<script lang="ts">
  export let links: { label: string; href: string }[] = [
    { label: "Home", href: "/" },
    { label: "Leaderboard", href: "/leaderboard" },
  ];

  let isOpen = false;
  function toggle() {
    isOpen = !isOpen;
  }
</script>

<nav
class="fixed top-0 inset-x-0 z-200 h-14
       flex items-center justify-between
       px-6 sm:px-10
       bg-white/5 backdrop-blur-md
       ring-1 ring-white/10 shadow-sm shadow-sky-500/5"
>
  <!-- brand -->
  <a href="/" class="text-xl font-bold tracking-tight text-white">
    AKPsi <span class="text-pink-400">Versus</span>
  </a>

  <!-- desktop links -->
  <ul class="hidden md:flex gap-8 text-sm font-medium">
    {#each links as { label, href }}
      <li>
        <a
          href={href}
          class="text-slate-300 hover:text-white transition-colors"
          >{label}</a
        >
      </li>
    {/each}
  </ul>

  <!-- mobile burger -->
  <button
    on:click={toggle}
    class="md:hidden inline-flex items-center justify-center
           text-slate-300 hover:text-white transition-colors focus:outline-none"
    aria-label="Toggle menu"
    aria-expanded={isOpen}
  >
    <svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M4 6h16M4 12h16M4 18h16"
      />
    </svg>
  </button>
</nav>

{#if isOpen}
  <!-- mobile dropdown -->
  <div
    class="md:hidden absolute top-14 inset-x-0 z-40
           bg-white/5 backdrop-blur-md
           ring-1 ring-white/10 shadow-sm shadow-sky-500/5"
  >
    <ul class="flex flex-col p-4 gap-4">
      {#each links as { label, href }}
        <li>
          <a
            href={href}
            class="block text-slate-300 hover:text-white transition-colors"
            on:click={() => (isOpen = false)}
            >{label}</a
          >
        </li>
      {/each}
    </ul>
  </div>
{/if}
