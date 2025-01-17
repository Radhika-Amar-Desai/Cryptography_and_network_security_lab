const net = require("net");
const { decryptText, key } = require("./DES");

const PORT = 5000;

// Create a TCP server
const server = net.createServer((socket) => {
  console.log("Client connected!");

  // Handle incoming data from the client
  socket.on("data", (data) => {
    console.log("Received from client:", data.toString());
    const message = decryptText(data.toString(), key);
    // console.log(message);
    socket.write("Acknowledged: " + message); // Send response back
  });

  // Keep the connection open, optionally handle errors or disconnection
  socket.on("end", () => {
    console.log("Client disconnected!");
  });

  socket.on("error", (err) => {
    console.error("Socket error:", err.message);
  });
});

// Start the server
server.listen(PORT, () => {
  console.log("Server is running on port" + {PORT});
});
