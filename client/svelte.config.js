import vercel from '@sveltejs/adapter-vercel';
export default {
  kit: {
    adapter: vercel(),
    // (keep any prerender settings you need)
  }
};