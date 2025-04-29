<script lang="ts">
  export let name: string = "Anonymous";
  export let major: string = "Undeclared";
  export let firstName: string = "anonymous";
  export let lastName: string = "user";

  const defaultImage = "https://placehold.co/400x400/png?text=Profile";
  const imagePath = `brother-pictures/${firstName.toLowerCase()}-${lastName.toLowerCase()}.jpg`;

  let image = imagePath;

  function handleImageError() {
    image = defaultImage;
  }
</script>

<div
  class="relative w-full max-w-full sm:max-w-xs
         overflow-hidden rounded-3xl
         bg-white/10 backdrop-blur-md
         shadow-lg shadow-sky-500/10
         transition-transform duration-300 group hover:-translate-y-1"
>
  <div
    class="pointer-events-none absolute inset-0 bg-gradient-to-br
           from-sky-400/40 via-indigo-500/40 to-fuchsia-500/40
           opacity-0 group-hover:opacity-30 transition-opacity duration-300"
  ></div>

  <img
    src={image}
    alt={name}
    on:error={handleImageError}
    class="w-full aspect-[4/3] sm:aspect-square object-cover rounded-t-3xl"
  />

  <div class="p-4 sm:p-5 text-center relative z-10">
    <h2 class="text-base sm:text-lg font-semibold text-white tracking-tight">
      {name}
    </h2>
    <p class="mt-1 text-xs sm:text-sm text-slate-300">
      {major}
    </p>
  </div>
</div>
