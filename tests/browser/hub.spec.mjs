import { expect, test } from "@playwright/test";

const textTokens = ["ink", "muted", "accent", "accent-deep", "pass", "prov", "prov-deep", "block", "block-deep", "info", "info-deep", "unres", "unres-ink"];

function luminance(hex) {
  const channels = [1, 3, 5].map((index) => parseInt(hex.slice(index, index + 2), 16) / 255);
  const linear = channels.map((value) => value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4);
  return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
}

function contrast(a, b) {
  const [lighter, darker] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (lighter + 0.05) / (darker + 0.05);
}

async function expectRenderedContrast(page, theme) {
  const values = await page.locator("body").evaluate((body, names) => {
    const style = getComputedStyle(body);
    return Object.fromEntries(["sheet", ...names].map((name) => [name, style.getPropertyValue(`--dt-${name}`).trim()]));
  }, textTokens);
  for (const token of textTokens) {
    expect(values[token], `${theme} --dt-${token} must be a six-digit hex color`).toMatch(/^#[0-9a-f]{6}$/i);
    expect(contrast(values[token], values.sheet), `${theme} --dt-${token} on --dt-sheet`).toBeGreaterThanOrEqual(4.5);
  }
}

test("Hub exposes its priorities and changes through the accessibility tree", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle("Right now | The Drafting Table");
  await expect(page.locator("html")).toHaveAttribute("lang", "en");
  await expect(page.getByRole("heading", { level: 1 })).toHaveCount(1);
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Right now");
  await expect(page.getByRole("banner")).toHaveCount(1);
  await expect(page.getByRole("main")).toHaveCount(1);
  await expect(page.getByRole("contentinfo")).toHaveCount(1);
  await expect(page.locator("#priority-list")).toHaveAttribute("aria-busy", "false");
  await expect(page.getByRole("status")).toContainText("Village priorities loaded");
  await expectRenderedContrast(page, "paper");
  await expect(page).toMatchAriaSnapshot({ name: "hub-initial.aria.yml" });

  await page.getByRole("button", { name: "Mark Recheck the Christmas tree's base done" }).click();
  await expect(page.getByRole("status")).toContainText("marked done in this demo only");
  await expect(page).toMatchAriaSnapshot({ name: "hub-done.aria.yml" });

  await page.getByRole("button", { name: "Blueprint view" }).click();
  await expect(page.getByRole("button", { name: "Paper view" })).toHaveAttribute("aria-pressed", "true");
  await expectRenderedContrast(page, "blueprint");
});

test("fixture load failure is announced", async ({ page }) => {
  await page.route("**/fixture.json", (route) => route.fulfill({ status: 500, body: "Unavailable" }));
  await page.goto("/");
  await expect(page.getByRole("status")).toHaveText("The village priorities could not load.");
  await expect(page.getByRole("main")).toContainText("The village priorities are unavailable.");
});
