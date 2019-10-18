require('module-alias/register')
var PROTO_PATH = './services/greet.proto'
import * as grpc from 'grpc'
import * as protoLoader from '@grpc/proto-loader'

import { GreetResponse } from "generated/services/greet_pb";

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
})
var protoDescriptor = grpc.loadPackageDefinition(packageDefinition) as any;

var greetpb = protoDescriptor.greet

var greetServer = new grpc.Server();
greetServer.addService(greetpb.GreetService.service, {
    Greet: greet,
});
greetServer.bind('0.0.0.0:50051', grpc.ServerCredentials.createInsecure());
console.log('Server running at 0.0.0.0:50051')
greetServer.start();

function greet(call: any, callback: Function) {
    console.log("Request :", call.request.greeting.first_name)
    var result = new GreetResponse()
    result.setResult("Greetings " + call.request.greeting.first_name)
    callback(null, {
        result
    });
}
