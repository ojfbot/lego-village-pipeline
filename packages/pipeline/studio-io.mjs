import { inflateRawSync } from "node:zlib";

const MAX_ARCHIVE_BYTES = 12 * 1024 * 1024;
const MAX_ENTRY_BYTES = 8 * 1024 * 1024;
const crcTable = Array.from({ length: 256 }, (_, n) => {
  let value = n;
  for (let bit = 0; bit < 8; bit++) value = value & 1 ? (value >>> 1) ^ 0xedb88320 : value >>> 1;
  return value >>> 0;
});
function crc32(bytes) {
  let value = 0xffffffff;
  for (const byte of bytes) value = crcTable[(value ^ byte) & 0xff] ^ (value >>> 8);
  return (value ^ 0xffffffff) >>> 0;
}

export function extractStudioModel(archive) {
  if (!Buffer.isBuffer(archive) || archive.length > MAX_ARCHIVE_BYTES) throw new Error("Studio archive must be under 12 MB.");
  let eocd = -1;
  for (let at = archive.length - 22; at >= Math.max(0, archive.length - 65557); at--) {
    if (archive.readUInt32LE(at) === 0x06054b50) { eocd = at; break; }
  }
  if (eocd < 0) throw new Error("Not a supported Studio ZIP archive.");
  const entries = archive.readUInt16LE(eocd + 10);
  let cursor = archive.readUInt32LE(eocd + 16);
  const selected = new Map();
  for (let index = 0; index < entries; index++) {
    if (cursor + 46 > archive.length || archive.readUInt32LE(cursor) !== 0x02014b50) throw new Error("Broken Studio ZIP directory.");
    const flags = archive.readUInt16LE(cursor + 8);
    const method = archive.readUInt16LE(cursor + 10);
    const expectedCrc = archive.readUInt32LE(cursor + 16);
    const packed = archive.readUInt32LE(cursor + 20);
    const unpacked = archive.readUInt32LE(cursor + 24);
    const nameLength = archive.readUInt16LE(cursor + 28);
    const extraLength = archive.readUInt16LE(cursor + 30);
    const commentLength = archive.readUInt16LE(cursor + 32);
    const localOffset = archive.readUInt32LE(cursor + 42);
    const end = cursor + 46 + nameLength + extraLength + commentLength;
    if (end > archive.length) throw new Error("Broken Studio ZIP directory.");
    const name = archive.toString("utf8", cursor + 46, cursor + 46 + nameLength);
    if (name === "model.ldr" || name === ".info") {
      if (selected.has(name)) throw new Error(`Duplicate ${name} ZIP entry.`);
      selected.set(name, { flags, method, packed, unpacked, localOffset, expectedCrc });
    }
    cursor = end;
  }
  function read(name) {
    const entry = selected.get(name);
    if (!entry) return null;
    if (entry.flags & 1) throw new Error(`${name} is encrypted; this prototype cannot read it.`);
    if (entry.unpacked > MAX_ENTRY_BYTES || entry.packed > MAX_ARCHIVE_BYTES) throw new Error(`${name} is too large.`);
    const at = entry.localOffset;
    if (at + 30 > archive.length || archive.readUInt32LE(at) !== 0x04034b50) throw new Error(`Broken ${name} ZIP entry.`);
    const dataAt = at + 30 + archive.readUInt16LE(at + 26) + archive.readUInt16LE(at + 28);
    if (dataAt + entry.packed > archive.length) throw new Error(`Truncated ${name} ZIP entry.`);
    const packed = archive.subarray(dataAt, dataAt + entry.packed);
    const bytes = entry.method === 0 ? packed : entry.method === 8 ? inflateRawSync(packed, { maxOutputLength: MAX_ENTRY_BYTES }) : null;
    if (!bytes || bytes.length !== entry.unpacked || crc32(bytes) !== entry.expectedCrc) throw new Error(`Unsupported or corrupt ${name} ZIP entry.`);
    return bytes.toString("utf8");
  }
  const model = read("model.ldr");
  if (!model) throw new Error("Studio archive has no model.ldr.");
  let archiveTotalParts = null;
  const info = read(".info");
  if (info) {
    try {
      const total = JSON.parse(info).total_parts;
      if (Number.isSafeInteger(total) && total >= 0) archiveTotalParts = total;
    } catch { /* Old Studio archives may lack readable metadata. */ }
  }
  return { model, archiveTotalParts };
}
