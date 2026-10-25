const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

// 순수 Node.js로 단색/도형 PNG 생성 유틸리티
function createPng(width, height, drawPixel) {
  const bytesPerPixel = 4; // RGBA
  const scanlineLength = width * bytesPerPixel;
  const rawData = Buffer.alloc(height * (1 + scanlineLength));

  let offset = 0;
  for (let y = 0; y < height; y++) {
    rawData[offset++] = 0; // Filter type 0 (None)
    for (let x = 0; x < width; x++) {
      const [r, g, b, a] = drawPixel(x, y, width, height);
      rawData[offset++] = r;
      rawData[offset++] = g;
      rawData[offset++] = b;
      rawData[offset++] = a;
    }
  }

  const compressed = zlib.deflateSync(rawData);

  // PNG Signature
  const signature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);

  // IHDR
  const ihdrData = Buffer.alloc(13);
  ihdrData.writeUInt32BE(width, 0);
  ihdrData.writeUInt32BE(height, 4);
  ihdrData[8] = 8; // bit depth
  ihdrData[9] = 6; // RGBA
  ihdrData[10] = 0; // compression
  ihdrData[11] = 0; // filter
  ihdrData[12] = 0; // interlace
  const ihdrChunk = makeChunk('IHDR', ihdrData);

  // IDAT
  const idatChunk = makeChunk('IDAT', compressed);

  // IEND
  const iendChunk = makeChunk('IEND', Buffer.alloc(0));

  return Buffer.concat([signature, ihdrChunk, idatChunk, iendChunk]);
}

function makeChunk(type, data) {
  const length = data.length;
  const header = Buffer.alloc(4);
  header.writeUInt32BE(length, 0);

  const typeBuf = Buffer.from(type, 'ascii');
  const crcData = Buffer.concat([typeBuf, data]);

  const crc = crc32(crcData);
  const crcBuf = Buffer.alloc(4);
  crcBuf.writeUInt32BE(crc, 0);

  return Buffer.concat([header, typeBuf, data, crcBuf]);
}

// CRC32 table & calc
const crcTable = new Uint32Array(256);
for (let n = 0; n < 256; n++) {
  let c = n;
  for (let k = 0; k < 8; k++) {
    c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
  }
  crcTable[n] = c;
}

function crc32(buf) {
  let crc = 0xffffffff;
  for (let i = 0; i < buf.length; i++) {
    crc = crcTable[(crc ^ buf[i]) & 0xff] ^ (crc >>> 8);
  }
  return (crc ^ 0xffffffff) >>> 0;
}

// 아이콘 디자인: 깊은 와인색 바탕(#70283F) + 금빛 십자가 심볼
function drawIconPixel(x, y, w, h) {
  const wine = [0x70, 0x28, 0x3f, 255]; // #70283F
  const gold = [0xf7, 0xf1, 0xe7, 255]; // #F7F1E7 (따뜻한 미색)

  const cx = w / 2;
  const cy = h / 2;

  // 십자가 규격
  const vWidth = Math.max(2, Math.round(w * 0.1));
  const vHeight = Math.round(h * 0.6);
  const hWidth = Math.round(w * 0.44);
  const hHeight = Math.max(2, Math.round(h * 0.1));
  const crossCenterY = cy - Math.round(h * 0.04);

  const inVertical = Math.abs(x - cx) <= vWidth / 2 && Math.abs(y - crossCenterY) <= vHeight / 2;
  const inHorizontal = Math.abs(x - cx) <= hWidth / 2 && Math.abs(y - (crossCenterY - vHeight * 0.12)) <= hHeight / 2;

  if (inVertical || inHorizontal) {
    return gold;
  }
  return wine;
}

const root = path.resolve(__dirname, '..');
const icon180 = createPng(180, 180, drawIconPixel);
const icon512 = createPng(512, 512, drawIconPixel);

fs.writeFileSync(path.join(root, 'prototype', 'apple-touch-icon.png'), icon180);
fs.writeFileSync(path.join(root, 'prototype', 'icon-192.png'), icon180);
fs.writeFileSync(path.join(root, 'prototype', 'icon-512.png'), icon512);

console.log('✅ iOS PWA 홈 화면용 아이콘 생성 완료 (apple-touch-icon.png, icon-192.png, icon-512.png)');
