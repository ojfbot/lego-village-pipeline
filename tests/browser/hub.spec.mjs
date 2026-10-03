import { expect, test } from "@playwright/test";

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
  await expect(page).toMatchAriaSnapshot({ name: "hub-initial.aria.yml" });

  await page.getByRole("button", { name: "Mark Recheck the Christmas tree's base done" }).click();
  await expect(page.getByRole("status")).toContainText("marked done in this demo only");
  await expect(page).toMatchAriaSnapshot({ name: "hub-done.aria.yml" });

  await page.getByRole("button", { name: "Blueprint view" }).click();
  await expect(page.getByRole("button", { name: "Paper view" })).toHaveAttribute("aria-pressed", "true");
  expect(await page.locator("body").evaluate((body) => getComputedStyle(body).getPropertyValue("--dt-block").trim().toUpperCase())).toBe("#F08B7B");
});
