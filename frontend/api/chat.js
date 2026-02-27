// Modellen die system messages ondersteunen (primair)
const MODELS_WITH_SYSTEM = [
  'google/gemini-2.0-flash-exp:free',
  'qwen/qwen-2.5-7b-instruct:free',
];

// Modellen waarbij system message omgezet wordt naar user message
const MODELS_NO_SYSTEM = [
  'google/gemma-3-4b-it:free',
];

function mergeSystemIntoUser(messages) {
  const system = messages.find(m => m.role === 'system');
  if (!system) return messages;
  const rest = messages.filter(m => m.role !== 'system');
  const firstUser = rest.findIndex(m => m.role === 'user');
  if (firstUser === -1) return rest;
  const result = [...rest];
  result[firstUser] = { role: 'user', content: `${system.content}\n\n${result[firstUser].content}` };
  return result;
}

async function tryModel(model, messages) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 12000);
  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
        'HTTP-Referer': 'https://botlease.nl',
        'X-Title': 'BotLease'
      },
      body: JSON.stringify({ model, messages, max_tokens: 200 }),
      signal: controller.signal,
    });
    clearTimeout(timeout);
    const data = await response.json();
    const content = data.choices?.[0]?.message?.content;
    if (response.ok && content) return content;
    return null;
  } catch {
    clearTimeout(timeout);
    return null;
  }
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') { res.status(200).end(); return; }
  if (req.method !== 'POST') return res.status(405).end();

  const { messages } = req.body;
  if (!messages) return res.status(400).json({ error: 'Geen berichten' });

  for (const model of MODELS_WITH_SYSTEM) {
    const content = await tryModel(model, messages);
    if (content) return res.status(200).json({ model, choices: [{ message: { role: 'assistant', content } }] });
  }

  const messagesNoSystem = mergeSystemIntoUser(messages);
  for (const model of MODELS_NO_SYSTEM) {
    const content = await tryModel(model, messagesNoSystem);
    if (content) return res.status(200).json({ model, choices: [{ message: { role: 'assistant', content } }] });
  }

  return res.status(503).json({ error: 'Tijdelijk niet beschikbaar' });
}
