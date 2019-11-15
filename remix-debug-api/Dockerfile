FROM node:10

WORKDIR /usr/src/app

COPY package*.json ./

COPY tsconfig.json ./

COPY . .

RUN git submodule update --init --recursive

RUN git submodule foreach 'npm install || :'

RUN npm install

RUN npm run build

EXPOSE 50052

CMD [ "node", "build/index.js" ]