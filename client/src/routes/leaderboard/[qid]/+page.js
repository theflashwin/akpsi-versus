import { error } from '@sveltejs/kit';

export async function load({ params, fetch }) {
  const { qid } = params;

  // 1) Fetch the question text
  const questionRes = await fetch(
    import.meta.env.VITE_FETCH_QUESTION_URL,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: qid })
    }
  );

  if (!questionRes.ok) {
    throw error(questionRes.status, `Could not fetch question #${qid}`);
  }

  const questionPayload = await questionRes.json();
  const question = questionPayload.question;

  // 2) Fetch the leaderboard for this question
  const leaderboardRes = await fetch(
    import.meta.env.VITE_FETCH_LEADERBOARD_URL,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category: question })
    }
  );

  if (!leaderboardRes.ok) {
    const errJson = await leaderboardRes.json().catch(() => ({}));
    const msg = errJson.error ?? `Could not fetch leaderboard for question #${qid}`;
    throw error(leaderboardRes.status, msg);
  }

  const leaderboard = await leaderboardRes.json();

  console.log(leaderboard)

  return {
    qid,
    question,
    leaderboard
  };
}
