const net = require("net");
const { encryptText, key } = require("./DES");
const PORT = 5000;
const HOST = "127.0.0.1";

// Create a TCP client
const client = net.createConnection({ host: HOST, port: PORT }, () => {
  console.log("Connected to server!");
  const message = encryptText("Hello Server! Just one message.", key);
  client.write(message);

  setTimeout(() => {
    console.log("Keeping the connection alive...");
  }, 1000);
});

client.on("data", (data) => {
  console.log("Received from server:", data.toString());
  // client.end();
});

client.on("end", () => {
  console.log("Disconnected from server!");
});

client.on("error", (err) => {
  console.error("Client error:", err.message);
});