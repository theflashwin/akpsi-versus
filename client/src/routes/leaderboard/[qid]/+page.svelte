<script>
    import Navbar from '../../../components/Navbar.svelte';
    import { fly } from 'svelte/transition';
  
    export let data;
    const { qid, question, leaderboard } = data;
  
    const DEFAULT_AVATAR =
      'https://ui-avatars.com/api/?name=User&size=128&background=ddd&color=555&rounded=true';

  </script>

<svelte:head>
    <title>Leaderboard - AKPsi Versus</title>
    <meta name="description" content="AKpsi" />
  </svelte:head>
  
  <Navbar />
  
  <main class="relative pt-16 h-[calc(100vh-4rem)] overflow-auto">
    <!-- fixed radial gradient -->
    <div
      class="pointer-events-none fixed inset-0 -z-10 rotate-180
             bg-slate-950
             bg-[radial-gradient(circle_farthest-side,rgba(255,0,182,.15),rgba(255,255,255,0))]"
    ></div>
  
    <div class="max-w-4xl mx-auto p-4">
      <!-- Header -->
      <h1 class="text-5xl sm:text-6xl font-extrabold text-white text-center">
        {question}
      </h1>
  
      <!-- Vertical list, each entry full-width row -->
      <section class="flex flex-col gap-6 mt-6">
        {#each leaderboard as p, i}
          <div
            class="group relative w-full bg-white/10 backdrop-blur-md border border-white/20 
                   rounded-2xl p-4 flex items-center justify-between shadow-lg
                   transform transition-transform duration-300 hover:-translate-y-1 hover:scale-105"
            in:fly={{ y: 30, duration: 500, delay: i * 100 }}
          >
          <div class="flex items-center space-x-2">
            <!-- Rank badge -->
            <div
              class="flex items-center justify-center w-8 h-8 p-4 rounded-full text-white font-bold
                     {i === 0
                       ? 'bg-yellow-400'
                       : i === 1
                       ? 'bg-gray-400'
                       : i === 2
                       ? 'bg-orange-500'
                       : 'bg-none'}"
            >
              {#if i === 0}🥇{:else if i === 1}🥈{:else if i === 2}🥉{:else}{i+1}{/if}
            </div>
          
            <!-- Avatar: fixed 12px square -->
            <!-- <img
              src={p.avatarUrl || DEFAULT_AVATAR}
              alt="{p.first_name} avatar"
              class="w-[12px] h-[12px] rounded-full object-cover flex-shrink-0"
            /> -->
          
            <!-- Name -->
            <span class="text-white font-medium text-lg">
              {p.first_name} {p.last_name}
            </span>
          </div>
  
            <!-- Right: score with larger text -->
            <div class="text-white font-bold text-lg">
              {p.ratings[question] ? parseInt(p.ratings[question]) : 1200} pts
            </div>
          </div>
        {/each}
      </section>
    </div>
  </main>
  
  <style>
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    .animate-spin {
      animation: spin 1s linear infinite;
    }
  </style>
  