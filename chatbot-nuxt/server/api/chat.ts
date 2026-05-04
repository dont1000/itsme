export default defineEventHandler(async (event) => {
  interface ChatRequest {
    message: string;
  }
  try {
    const body: ChatRequest = await readBody(event);
    const { message } = body;

    const { backendUrl } = useRuntimeConfig();
    const response = await fetch(`${backendUrl}/chat`, {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify({ message, history: [] }),
    });

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }

    const text = await response.text();
    return { text };

  } catch (error) {
    console.error("Error in /api/chat server:", error);
    event.res.statusCode = 500;
    return { text: "Es tut mir leid, etwas ist schiefgelaufen." };
  }
});
