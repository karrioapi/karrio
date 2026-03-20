import { test as setup } from "@playwright/test";
import path from "path";
import { loginToDashboard } from "../helpers/auth";

const AUTH_STATE = path.join(__dirname, "..", "playwright", ".auth", "user.json");

setup("authenticate", async ({ page }) => {
  await loginToDashboard(page);
  await page.context().storageState({ path: AUTH_STATE });
});
