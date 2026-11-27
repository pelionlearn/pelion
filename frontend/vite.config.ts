import { defineConfig } from "vite";
import react, { reactCompilerPreset } from "@vitejs/plugin-react";
import babel from "@rolldown/plugin-babel";
import tailwindcss from "@tailwindcss/vite";

const dockerDev = process.env.DOCKER_DEV === "true";

// https://vite.dev/config/
export default defineConfig({
    plugins: [react(), babel({ presets: [reactCompilerPreset()] }), tailwindcss()],
    server: {
        port: 8080, // TODO: change to 5173 default and change in Caddyfile.dev and docker-compose.dev.yml
        watch: dockerDev ? { usePolling: true, interval: 1000 } : undefined,
    },
});
