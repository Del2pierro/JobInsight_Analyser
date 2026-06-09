# --- Étape 1 : Build ---
FROM node:20-alpine AS builder
WORKDIR /app

# Définir l'URL de l'API au moment du build (Next.js en a besoin pour le client)
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# --- Étape 2 : Runtime ---
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# On ne copie que le nécessaire du build pour une image légère
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000
CMD ["npm", "start"]
