FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --omit=dev

COPY . .

HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
  CMD node healthcheck.js

CMD ["npm", "start"]