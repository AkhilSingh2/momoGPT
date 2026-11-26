// Static demo for GitHub Pages. There is no Flask server or model here, so /chat
// answers with canned replies written in the example persona's style
// (examples/personality.json: short, lowercase, "lol", lots of emoji).
(function () {
  const rules = [
    [/^(hi|hey|hello|yo|good morning|morning|gm)\b/i, ['heyy!! 💕', 'morning!! did you sleep well?', 'hiii 👋']],
    [/hungry|food|eat|lunch|dinner|breakfast|pizza/i, ['sameee', 'omg yes food 😋 what are we getting', 'hungry too lol, pizza?? 🍕']],
    [/study|exam|class|homework/i, ['ugh same, studying all day 📚', 'you got this 💪', 'probably gonna study for a bit lol']],
    [/code|coding|project|work|bug/i, ['ooh the coding one?', 'nice!! you got this 💪', 'lol is it working yet 😂']],
    [/dream|sleep|tired|night/i, ['i had the weirdest dream lol', 'go sleep!! 😴', 'same i\'m so tired lol']],
    [/beach|trip|travel|weekend/i, ['we should find one 🏖️', 'yesss let\'s go 😍', 'weekend plans?? 👀']],
    [/how (does|do) (this|you) work|are you real|bot|ai/i, ['lol i\'m the demo version 😅 no model here, just canned replies. run it locally to train on a real chat']],
    [/lol|haha|😂/i, ['hahaha right!!', 'lol', 'so random 😂']],
    [/\?$/, ['hmm maybe? 🤔', 'idk lol, you?', 'yess']],
  ];
  const fallback = ['lol', 'nice!!', 'hahaha right!!', 'omg same', 'tell me more 👀', 'so random 😂'];
  const pick = (items) => items[Math.floor(Math.random() * items.length)];

  function reply(message) {
    for (const [pattern, answers] of rules) if (pattern.test(message)) return pick(answers);
    return pick(fallback);
  }

  const json = (body) => new Response(JSON.stringify(body), { headers: { 'Content-Type': 'application/json' } });
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const original = window.fetch.bind(window);

  window.fetch = async function (input, init) {
    const url = new URL(typeof input === 'string' ? input : input.url, window.location.href);
    if (url.pathname.endsWith('/chat')) {
      const { message } = JSON.parse((init && init.body) || '{}');
      if (!message || !message.trim()) return json({ error: 'Empty message', success: false });
      await sleep(500 + Math.random() * 700);
      return json({ response: reply(message), success: true });
    }
    if (url.pathname.endsWith('/reset')) return json({ success: true });
    if (url.pathname.endsWith('/history')) return json({ history: [], success: true });
    return original(input, init);
  };
})();
