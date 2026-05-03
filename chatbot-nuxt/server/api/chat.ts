export default defineEventHandler(async (event) => {
  interface ChatRequest {
    message: string;
  }
  try {
    // Parse the incoming request
    const body: ChatRequest = await readBody(event);
    console.log("body",body)
    let {message} = body
 
    const response = await fetch(
      "https://flowise-ob32.onrender.com/api/v1/prediction/1aa94af1-e393-46b0-b816-00d2551eac44",
      {
          headers: {
               Authorization: `Bearer ${process.env.FLOWWISE_API_KEY}`,
              "Content-Type": "application/json"
          },
          method: "POST",
          body: JSON.stringify({"question":message})
      }
    );

    const result = await response.json();
   
    return result;
 
  } catch (error) {
    console.error("Error in /api/chat server:", error);
    event.res.statusCode = 500;
    return { reply: "I'm sorry, something went wrong on the server." };
  }
});
