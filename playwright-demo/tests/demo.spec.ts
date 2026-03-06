import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example Domain/);
});

test('can click link', async ({ page }) => {
  await page.goto('https://example.com');
  await page.click('text=More information');
  await expect(page).toHaveURL(/example\.org/);
});

test('fill form', async ({ page }) => {
  await page.goto('https://example.com');
  const text = await page.textContent('h1');
  expect(text).toContain('Example Domain');
});
