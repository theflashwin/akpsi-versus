<script>

  import BrotherCard from "../components/BrotherCard.svelte";
  import Navbar from "../components/Navbar.svelte";
  import { fly } from "svelte/transition";
  import { cubicOut } from "svelte/easing";
  import { onMount } from "svelte";
  
  let isLoading = true;
  let isSubmitting = false;
  let question = "";
  let players = [];
  let selectedWinner = null;
  let fadeOutDone = false;
  let showTitle = false;
  
  const FETCH_URL =
    import.meta.env.VITE_FETCH_QUESTION_AND_PLAYERS_URL;
  const POST_URL =
    import.meta.env.VITE_POST_RESULT_URL;
  
  async function fetchMatchup() {
    try {
      const res = await fetch(FETCH_URL);
      const data = await res.json();
      question = data.question.value;
      players = data.players;
    } catch (err) {
      console.error("Failed to fetch matchup:", err);
    } finally {
      isLoading = false;
      setTimeout(() => {
        showTitle = true;
      }, 50);
    }
  }
  
  onMount(fetchMatchup);
  
  async function submitResultAfterFly() {
    isSubmitting = true;
  
    const body = {
      category: question,
      winner_id: selectedWinner.id,
      loser_ids: players
        .filter((p) => p.id !== selectedWinner.id)
        .map((p) => p.id),
    };
  
    try {
      const res = await fetch(POST_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
  
      if (!res.ok) {
        console.error("Failed to post result:", await res.text());
        return;
      }
  
      await res.json();
      await fetchMatchup();
    } catch (err) {
      console.error("Error submitting result:", err);
    } finally {
      isSubmitting = false;
      selectedWinner = null;
      fadeOutDone = false;
    }
  }
  
  function handleCardClick(player) {
    selectedWinner = player;
    fadeOutDone = false;
  }
</script>

<svelte:head>
  <title>Home - AKPsi Versus</title>
  <meta name="description" content="AKpsi" />
</svelte:head>
  
<Navbar />

<main
  class="relative flex flex-col items-center justify-start pt-24
         min-h-screen w-screen m-0 overflow-auto"
>
  <div
    class="pointer-events-none absolute inset-0 -z-10 rotate-180
           bg-slate-950
           bg-[radial-gradient(circle_farthest-side,rgba(255,0,182,.15),rgba(255,255,255,0))]"
  ></div>

  {#if isLoading || isSubmitting}
    <div class="flex flex-col items-center justify-center h-full">
      <div
        class="animate-spin rounded-full h-16 w-16 border-4 border-white border-t-transparent mb-4"
      ></div>
      <p class="text-white text-lg">Loading...</p>
    </div>
  {:else}
    {#if showTitle && (!selectedWinner || fadeOutDone)}
      <h1
        in:fly={{ y: -100, duration: 700, easing: cubicOut }}
        out:fly={{ y: -100, duration: 500, easing: cubicOut }}
        class="mb-8 text-3xl sm:text-4xl md:text-5xl font-bold
               text-white drop-shadow-lg text-center px-4 lg:mt-28"
      >
        {question}
      </h1>
    {/if}

    <section
      class="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4
             gap-6 w-full max-w-6xl px-4 mb-12"
    >
      {#each players as p (p.id)}
        {#if !selectedWinner || fadeOutDone}
          <div
            on:click={() => handleCardClick(p)}
            class="cursor-pointer w-full"
            out:fly={{ y: 100, duration: 500, easing: cubicOut }}
            on:outroend={() => {
              if (selectedWinner && !fadeOutDone) {
                fadeOutDone = true;
                submitResultAfterFly();
              }
            }}
          >
            <BrotherCard
              name={p.first_name + " " + p.last_name}
              major={p.major}
              firstName={p.first_name}
              lastName={p.last_name}
            />
          </div>
        {/if}
      {/each}
    </section>
  {/if}
</main>

<style>
  @keyframes fade-in {
    from {
      opacity: 0;
      transform: scale(0.9);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
  .animate-fade-in {
    animation: fade-in 0.5s ease-out;
  }
</style>
