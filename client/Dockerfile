FROM node:18.15.0

WORKDIR /app

COPY client/package*.json ./

RUN npm install --force

COPY client ./

EXPOSE 3000

CMD ["npm", "start"]
