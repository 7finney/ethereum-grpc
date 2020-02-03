FROM golang

WORKDIR /usr/src/app

# COPY ./server/services/ .

COPY ./server/main .

# Build the Go app
# RUN go build -o main .

EXPOSE 4040

CMD [ "./main" ]