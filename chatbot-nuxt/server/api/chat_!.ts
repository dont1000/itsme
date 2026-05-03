export default defineEventHandler(async (event) => {
  interface ChatRequest {
    threadId?: string;
    message: string;
  }
  try {
    // Parse the incoming request
    const body: ChatRequest = await readBody(event);
    let {message, threadId} = body
    let runId:string = "";

    // If no threadId is provided, open a new conversation thread using your assistant ID.
    if (!threadId) {
      console.log("-------- new threadId", threadId);
      const threadResponse = await fetch("https://api.openai.com/v1/threads", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
          "Content-Type": "application/json",
          "OpenAI-Beta": "assistants=v2",
        },
        body: JSON.stringify({}),
      });

      const threadData = await threadResponse.json();
      if (!threadData.id) throw new Error("Failed to create a thread.");
      threadId = threadData.id;
      console.log("threadId", threadId);
    }

    console.log("--------initial thread id", threadId, "   ", message);
     console.log("--------OPENAI_API_KEY", process.env.OPENAI_API_KEY);
    // Now, send the user's message along with the threadId to the ChatGPT API.
    const userMessageResponse = await fetch(
      `https://api.openai.com/v1/threads/${threadId}/messages`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
          "Content-Type": "application/json",
          "OpenAI-Beta": "assistants=v2",
        },
        body: JSON.stringify({
          role: "user",
          content: message, // hard coded to test
        }),
      }
    );
    const userMessageData = await userMessageResponse.json();
    console.log("----userMessage called", userMessageData);

    const responseRun = await fetch(
      `https://api.openai.com/v1/threads/${threadId}/runs`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
          "Content-Type": "application/json",
          "OpenAI-Beta": "assistants=v2",
        },
        body: JSON.stringify({
          assistant_id: "asst_APH6OvDHVyUMY3UobK16wYD5",
          tool_resources: {
            file_search: {
              vector_store_ids: ["vs_67b82aa3c8a08191a2300fecd413ec54"],
            },
          },
        }),
      }
    );
    const responseRunData = await responseRun.json();
    runId = responseRunData.id;
    console.log("---run called", runId);
    let runStatusData
    async function pollRunStatus(
      threadId:string|undefined,
      runId:string,
      delay = 800,
      maxAttempts = 15
    ) {
      let attempts = 0;
      while (attempts < maxAttempts) {
        console.log("pollRunStatus attempts ", attempts);
        const response = await fetch(
          `https://api.openai.com/v1/threads/${threadId}/runs/${runId}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
              "OpenAI-Beta": "assistants=v2",
            },
          }
        );

        runStatusData = await response.json();
        console.log("runStatusData", runStatusData.status);

        // Check if the run status indicates completion.
        if (
          runStatusData.status === "succeeded" ||
          runStatusData.status === "completed"
        ) {
          return runStatusData;
        }

        // Wait before trying again.
       
        await new Promise((resolve) => setTimeout(resolve, delay));
        attempts++;
      }
      throw new Error("Run did not complete within the expected time.");
    }

    await pollRunStatus(threadId, runId);
    console.log("run completed");

    async function pollForAssistantMessage(
      threadId:string,
      delay = 0,
      maxAttempts = 1
    ) {
      let attempts = 0;
      while (attempts < maxAttempts) {
        const response = await fetch(
          `https://api.openai.com/v1/threads/${threadId}/messages?limit=3`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
              "OpenAI-Beta": "assistants=v2",
            },
          }
        );
        const data = await response.json();
        console.log("pollForAssistantMessage", attempts, "-------");

        if (data.data.length > 0 && data.data[0].role === "assistant") {
          console.log("inner loop", data.data[0]);
          return data.data[0];
        }
        // Wait for the specified delay before trying again
        await new Promise((resolve) => setTimeout(resolve, delay));
        attempts++;
      }
      throw new Error(
        "Assistant message not received within the expected time."
      );
    }
    console.log("----------call responseData with thread id", threadId);
    let responseData;
    if (threadId) {responseData = await pollForAssistantMessage(threadId)};

    const reply = responseData.content[0].text.value;
    console.log("----------responsedata-content", reply);
    return { reply, threadId };
  } catch (error) {
    console.error("Error in /api/chat server:", error);
    event.res.statusCode = 500;
    return { reply: "I'm sorry, something went wrong on the server." };
  }
});
