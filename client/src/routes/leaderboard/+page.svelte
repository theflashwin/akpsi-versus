<script>
    import { onMount } from "svelte";
    import { fly, fade } from "svelte/transition";
    import Navbar from "../../components/Navbar.svelte";
  
    let questions = [];
    let isLoading = true;
  
    async function fetchQuestions() {
      try {
        const res = await fetch(import.meta.env.VITE_FETCH_QUESTIONS_URL);
        const data = await res.json();
        questions = data.questions || data;
        console.log(data)
      } catch (err) {
        console.error("Failed to fetch questions:", err);
      } finally {
        isLoading = false;
      }
    }
  
    onMount(fetchQuestions);
  </script>

<svelte:head>
  <title>Leaderboard - AKPsi Versus</title>
  <meta name="description" content="AKpsi" />
</svelte:head>
  
  <!-- sticky navbar -->
  <div class="sticky top-0 left-0 w-full h-16 z-50">
    <Navbar />
  </div>
  
  <main class="relative flex flex-col items-center justify-start w-screen h-[calc(100vh-4rem)] pt-16 overflow-auto p-4">
    <!-- fixed background gradient -->
    <div
      class="pointer-events-none fixed inset-0 -z-10 rotate-180
             bg-slate-950
             bg-[radial-gradient(circle_farthest-side,rgba(255,0,182,.15),rgba(255,255,255,0))]"
    ></div>
  
    {#if isLoading}
      <div class="flex flex-col items-center justify-center mt-20">
        <div class="animate-spin rounded-full h-16 w-16 border-4 border-white/70 border-t-transparent mb-4"></div>
        <p class="text-white text-lg">Loading...</p>
      </div>
    {:else}
      <!-- title & description -->
      <div class="w-full max-w-3xl text-center mb-8">
        <h1 class="text-4xl text-white sm:text-5xl font-extrabold">
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-pink-500">Versus</span> Leaderboard
        </h1>
        <p class="mt-2 text-white text-base sm:text-lg">
          Click to see the leaderboard. Let Ashwin know if you want another prompt to be added.
        </p>
      </div>
  
      <!-- Questions Grid -->
      <section
      class="grid
             grid-cols-1 sm:grid-cols-2 lg:grid-cols-4
             gap-8 w-full max-w-6xl
             auto-rows-fr"
    >
      {#each questions as q, i (q.id)}
        <a
          href={`/leaderboard/${q.id}`}
          sveltekit:prefetch
          class="group block h-full"
        >
          <div
            class="relative h-full flex items-center justify-center
                   bg-white/20 backdrop-blur-lg border border-white/30
                   rounded-2xl p-6 shadow-lg
                   transform transition-transform duration-300
                   hover:-translate-y-1 hover:scale-105"
            in:fly={{ y: 30, duration: 600, delay: i * 100 }}
          >
            <div
              class="pointer-events-none absolute inset-0
                     bg-gradient-to-br from-sky-400/40 via-indigo-500/40 to-fuchsia-500/40
                     rounded-2xl
                     opacity-0 group-hover:opacity-30
                     transition-opacity duration-300"
            ></div>
    
            <p class="relative text-white text-center text-base sm:text-lg font-semibold">
              {q.value}
            </p>
          </div>
        </a>
      {/each}
    </section>
    
    {/if}
  </main>
  

  <style>
    /* hide scrollbars on our main container */
    :global(main) {
      -ms-overflow-style: none;  /* IE & Edge */
      scrollbar-width: none;     /* Firefox */
    }
    :global(main::-webkit-scrollbar) {
      display: none;             /* Chrome, Safari, Opera */
    }
  
    @keyframes spin { to { transform: rotate(360deg); } }
    .animate-spin { animation: spin 1s linear infinite; }
  </style>
  