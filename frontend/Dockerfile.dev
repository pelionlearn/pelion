FROM node:22-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]