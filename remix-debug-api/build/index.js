"use strict";
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
require('module-alias/register');
var PROTO_PATH = './services/remix-debug.proto';
var grpc = __importStar(require("grpc"));
var protoLoader = __importStar(require("@grpc/proto-loader"));
var remix_debug_pb_1 = require("generated/services/remix-debug_pb");
// @ts-ignore
var remix_debug_1 = require("remix-debug");
var web3_1 = __importDefault(require("web3"));
// gRPC server
var packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
});
var protoDescriptor = grpc.loadPackageDefinition(packageDefinition);
var remix_debug_pb = protoDescriptor.remix_debug;
var rxDbgServer = new grpc.Server();
rxDbgServer.addService(remix_debug_pb.RemixDebugService.service, {
    RunDebug: debug,
});
rxDbgServer.bind('0.0.0.0:50052', grpc.ServerCredentials.createInsecure());
console.log('Server running at 0.0.0.0:50052');
rxDbgServer.start();
// remix-debug code
var web3 = new web3_1.default('http://localhost:8545');
var ethdebugger = new remix_debug_1.EthDebugger({ web3: web3 });
function debug(call) {
    var result = new remix_debug_pb_1.DebugResponse();
    console.log(call.request);
    var txHash = call.request.debugInterface.payload;
    web3.eth.getTransaction(txHash, function (error, tx) {
        if (error)
            throw error;
        console.log(tx);
        ethdebugger.event.register('newTraceLoaded', function (trace) {
            console.log(trace);
            call.write({ result: JSON.stringify(trace) });
        });
        ethdebugger.debug(tx);
    });
}
