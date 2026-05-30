# =============================================================================
# AI English Coach — Frontend Dockerfile (Multi-stage)
# =============================================================================

# ---- Base ----
FROM node:20-alpine as base
WORKDIR /app
RUN apk add --no-cache libc6-compat

# ---- Dependencies ----
FROM base as dependencies
COPY package*.json ./
RUN npm ci

# ---- Development ----
FROM dependencies as development
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

# ---- Build ----
FROM dependencies as build
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# ---- Production ----
FROM base as production
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs
COPY --from=build /app/public ./public
COPY --from=build --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=build --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
