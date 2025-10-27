FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
# fallback to npm install if ci can't run (no lockfile)
RUN npm ci --no-audit --fund=false || npm install --no-audit --fund=false
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
