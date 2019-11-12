FROM node:10

WORKDIR /usr/src/app

COPY package*.json ./

COPY tsconfig.json ./

COPY . .

RUN npm install

RUN npm run build

EXPOSE 50051

CMD [ "node", "build/index.js" ]