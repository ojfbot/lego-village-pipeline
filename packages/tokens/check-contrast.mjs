import { readFileSync } from "node:fs";

const source = readFileSync(new URL("../../docs/design/H-01-R1/dt/tokens.css", import.meta.url), "utf8");
const override = readFileSync(new URL("./tokens.css", import.meta.url), "utf8");
const textTokens = ["ink", "muted", "accent", "accent-deep", "pass", "prov", "prov-deep", "block", "block-deep", "info", "info-deep", "unres", "unres-ink"];

function declarations(css, selector) {
  const escaped = selector.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = css.match(new RegExp(`${escaped}\\s*\\{([^}]*)\\}`));
  if (!match) return {};
  return Object.fromEntries([...match[1].matchAll(/--dt-([\w-]+)\s*:\s*(#[0-9a-f]{6})\b/gi)].map((entry) => [entry[1], entry[2]]));
}

function luminance(hex) {
  const channels = [1, 3, 5].map((index) => parseInt(hex.slice(index, index + 2), 16) / 255);
  const linear = channels.map((value) => value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4);
  return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
}

function contrast(a, b) {
  const [lighter, darker] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (lighter + 0.05) / (darker + 0.05);
}

if (!override.includes('@import url("/design-tokens.css")')) throw new Error("App tokens must import the pinned H-01 design cut.");
let failures = 0;
for (const [theme, selector] of [["paper", ":root"], ["blueprint", "body.dt-blueprint"]]) {
  const values = { ...declarations(source, selector), ...declarations(override, selector) };
  if (!values.sheet) throw new Error(`${theme} sheet token missing`);
  for (const token of textTokens) {
    if (!values[token]) throw new Error(`${theme} text token --dt-${token} missing`);
    const ratio = contrast(values[token], values.sheet);
    const pass = ratio >= 4.5;
    if (!pass) failures++;
    console.log(`${pass ? "pass" : "FAIL"} ${theme} --dt-${token} ${values[token]} on ${values.sheet} = ${ratio.toFixed(2)}:1`);
  }
}
if (failures) process.exitCode = 1;
