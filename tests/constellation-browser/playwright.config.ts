import {defineConfig} from '@playwright/test';
export default defineConfig({
  testDir: '.', testMatch: '*.spec.ts', workers: 1, reporter: 'list',
  outputDir: '../../test-results/constellation',
  use: {baseURL: 'http://127.0.0.1:4180', viewport: {width:1600,height:1000}, reducedMotion:'reduce',
    launchOptions:{channel:process.env.PLAYWRIGHT_CHROMIUM_CHANNEL ?? 'chrome'}},
  webServer:{command:'python3 -m http.server 4180 --bind 127.0.0.1',
    cwd:'../..',url:'http://127.0.0.1:4180',reuseExistingServer:true,timeout:15000}
});
