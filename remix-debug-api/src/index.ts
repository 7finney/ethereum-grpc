require('module-alias/register')
var PROTO_PATH = './services/remix-debug.proto'
import * as grpc from 'grpc'
import * as protoLoader from '@grpc/proto-loader'
import { DebugResponse } from "generated/services/remix-debug_pb"
// @ts-ignore
import { EthDebugger } from 'remix-debug'
import Web3 from 'web3'

// gRPC server
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
})
var protoDescriptor = grpc.loadPackageDefinition(packageDefinition) as any;

var remix_debug_pb = protoDescriptor.remix_debug;

var rxDbgServer = new grpc.Server();
rxDbgServer.addService(remix_debug_pb.RemixDebugService.service, {
    RunDebug: debug,
});
rxDbgServer.bind('0.0.0.0:50052', grpc.ServerCredentials.createInsecure());
console.log('Server running at 0.0.0.0:50052');
rxDbgServer.start();

// remix-debug code
// const web3 = new Web3('http://ganache:8545');
// const goerliWeb3 = new Web3('http://172.26.84.11:7545');

// const web3 = new Web3('http://172.26.84.11:7545');
function debug(call: any) {
    let result = new DebugResponse();
    // console.log(call.request);
    // const txHash: string = call.request.debugInterface.payload;
    const txHash: string = call.request.debugInterface.payload;
    const testnetId: string = call.request.debugInterface.testnetId;
    var url: string = "http://172.26.84.11:754";
    switch (testnetId) {
        case "5":
            url += "5";
            break;
        case "3":
            url += "6";
            break;
        case "4":
            url += "7";
            break;
        case "ganache":
            url = "http://ganache:8545";
            break;
        default:
            url = "http://ganache:8545";
    }
    const web3 = new Web3(url);
    const ethdebugger = new EthDebugger({ web3 });
    web3.eth.getTransaction(txHash).then((tx: any) => {
        console.log("tx",tx);
        ethdebugger.event.register('newTraceLoaded', (trace: any) => {
            console.log("hghjgygj",trace);
            call.write({ result: JSON.stringify(trace) });
        });
        ethdebugger.debug(tx);

    }).catch((error: any) => {
        throw error;
    });
}