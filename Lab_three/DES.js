function textToBinary(text) {
  return text
    .split("")
    .map((char) => char.charCodeAt(0).toString(2).padStart(8, "0"))
    .join("");
}

function binaryToText(binary) {
  return binary
    .match(/.{1,8}/g)
    .map((byte) => String.fromCharCode(parseInt(byte, 2)))
    .join("");
}

function permute(input, table) {
  return table.map((index) => input[index - 1]).join("");
}

function xor(bin1, bin2) {
  return bin1
    .split("")
    .map((bit, index) => (bit ^ bin2[index]).toString())
    .join("");
}

function leftRotate(bits, shifts) {
  return bits.slice(shifts) + bits.slice(0, shifts);
}

const INITIAL_PERMUTATION = [
  58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38,
  30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1,
  59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39,
  31, 23, 15, 7,
];

const FINAL_PERMUTATION = [
  40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14,
  54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28,
  35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9,
  49, 17, 57, 25,
];

const S_BOX = [
  [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
  ],
  [
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
  ],
  [
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
  ],
  [
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
  ],
  [
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
  ],
  [
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
  ],
  [
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
  ],
  [
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
  ],
];

const EXPANSION_TABLE = [
  32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16,
  17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29,
  28, 29, 30, 31, 32, 1,
];

const P_BOX = [
  16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32,
  27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25,
];

const PC1 = [
  57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35,
  27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38,
  30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4,
];

const PC2 = [
  14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27,
  20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34,
  53, 46, 42, 50, 36, 29, 32,
];

const SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1];

function sBoxSubstitution(input) {
  let output = "";
  for (let i = 0; i < 8; i++) {
    const chunk = input.slice(i * 6, (i + 1) * 6);
    const row = parseInt(chunk[0] + chunk[5], 2);
    const col = parseInt(chunk.slice(1, 5), 2);
    output += S_BOX[i][row][col].toString(2).padStart(4, "0");
  }
  return output;
}

function feistelRound(left, right, key) {
  const expandedRight = permute(right, EXPANSION_TABLE);
  const xored = xor(expandedRight, key);

  let substituted = sBoxSubstitution(xored);

  const permuted = permute(substituted, P_BOX);
  const newRight = xor(left, permuted);
  return [right, newRight];
}

function encryptBlock(block, roundKeys) {
  let permutedBlock = permute(block, INITIAL_PERMUTATION);
  let left = permutedBlock.slice(0, 32);
  let right = permutedBlock.slice(32);

  for (let i = 0; i < roundKeys.length; i++) {
    [left, right] = feistelRound(left, right, roundKeys[i]);
  }

  return permute(right + left, FINAL_PERMUTATION);
}

function decryptBlock(block, roundKeys) {
  let permutedBlock = permute(block, INITIAL_PERMUTATION);
  let left = permutedBlock.slice(0, 32);
  let right = permutedBlock.slice(32);

  for (let i = roundKeys.length - 1; i >= 0; i--) {
    [left, right] = feistelRound(left, right, roundKeys[i]);
  }

  return permute(right + left, FINAL_PERMUTATION);
}

function generateKeys(key) {
  const permutedKey = permute(key, PC1);
  let left = permutedKey.slice(0, 28);
  let right = permutedKey.slice(28);

  const keys = [];
  for (let i = 0; i < 16; i++) {
    left = leftRotate(left, SHIFTS[i]);
    right = leftRotate(right, SHIFTS[i]);
    const combinedKey = left + right;
    keys.push(permute(combinedKey, PC2));
  }
  return keys;
}

function encryptText(text, key) {
  const binaryText = textToBinary(text);
  const binaryKey = textToBinary(key).slice(0, 64);
  const keys = generateKeys(binaryKey);
  const blocks = binaryText.match(/.{1,64}/g) || [];
  const encryptedBlocks = blocks.map((block) =>
    encryptBlock(block.padEnd(64, "0"), keys)
  );
  return encryptedBlocks.join("");
}

function decryptText(encryptedText, key) {
  const binaryKey = textToBinary(key).slice(0, 64);
  const keys = generateKeys(binaryKey);
  const blocks = encryptedText.match(/.{1,64}/g) || [];
  const decryptedBlocks = blocks.map((block) => decryptBlock(block, keys));
  return binaryToText(decryptedBlocks.join(""));
}

const key = "12345678";

// const encryptedMessage = encryptText(message, key);
// console.log("Encrypted Message:", encryptedMessage);

// const decryptedMessage = decryptText(encryptedMessage, key);
// console.log("Decrypted Message:", decryptedMessage);

module.exports = { decryptText, encryptText, key };
