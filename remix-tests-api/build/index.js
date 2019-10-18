"use strict";
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
require('module-alias/register');
var PROTO_PATH = './services/greet.proto';
var grpc = __importStar(require("grpc"));
var protoLoader = __importStar(require("@grpc/proto-loader"));
var greet_pb_1 = require("generated/services/greet_pb");
var packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
});
var protoDescriptor = grpc.loadPackageDefinition(packageDefinition);
var greetpb = protoDescriptor.greet;
var greetServer = new grpc.Server();
greetServer.addService(greetpb.GreetService.service, {
    Greet: greet,
});
greetServer.bind('0.0.0.0:50051', grpc.ServerCredentials.createInsecure());
console.log('Server running at 0.0.0.0:50051');
greetServer.start();
function greet(call, callback) {
    console.log("Request :", call.request.greeting.first_name);
    var result = new greet_pb_1.GreetResponse();
    result.setResult("Greetings " + call.request.greeting.first_name);
    callback(null, {
        result: result
    });
}
