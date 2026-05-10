# Minecraft Bot Controller

A web-based control panel for a Minecraft bot — connect it to any server, monitor its health and position in real time, control its movement, and manage the chat.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 8080)
- `pnpm --filter @workspace/minecraft-bot run dev` — run the frontend (port 23418)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5 + Socket.IO (real-time bot events)
- Bot engine: mineflayer
- Frontend: React + Vite + TailwindCSS + shadcn/ui
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

- `lib/api-spec/openapi.yaml` — API contract (source of truth)
- `artifacts/api-server/src/lib/bot-manager.ts` — mineflayer bot instance + event emitter
- `artifacts/api-server/src/routes/bot.ts` — bot REST API routes
- `artifacts/api-server/src/index.ts` — Express server + Socket.IO setup
- `artifacts/minecraft-bot/src/` — React frontend

## Architecture decisions

- Bot state is held in a singleton `BotManager` class (in-process), not persisted to a database — no DB needed.
- Socket.IO is served on the same Express HTTP server at `/socket.io`, proxied alongside `/api`.
- mineflayer is externalized from the esbuild bundle (too complex to bundle) — runs from `node_modules`.
- Frontend polls `/api/bot/status` every 2 seconds as a fallback alongside Socket.IO for real-time updates.
- All chat messages are kept in-memory (max 200) and broadcast via Socket.IO `chat` event.

## Product

- Connect to any Minecraft server (offline mode) with a custom username and version
- Real-time dashboard: health/food bars, XYZ position, game mode, online players
- Chat terminal: live scrolling chat log with color-coded sources (bot/player/server/system)
- Movement controls: directional pad with hold-to-move behavior
- Quick macro buttons: jump, sprint, sneak, attack, use item
- Slash command input to run any Minecraft command

## User preferences

_Populate as you build — explicit user instructions worth remembering across sessions._

## Gotchas

- After changing `build.mjs` externals, always rebuild manually before restarting the workflow.
- mineflayer must be externalized in `build.mjs` or esbuild will time out.
- `/socket.io` must be listed in the api-server's `artifact.toml` `paths` array for WebSocket proxying to work.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
