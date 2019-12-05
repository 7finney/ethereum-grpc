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
const web3 = new Web3('http://ganache:8545');
const ethdebugger = new EthDebugger({ web3 });
function debug(call: any) {
    let result = new DebugResponse();
    console.log(call.request);
    const txHash: string = call.request.debugInterface.payload;
    web3.eth.getTransaction(txHash, (error: Error, tx: any) => {
        if (error)
            throw error;
        console.log(tx);
        ethdebugger.event.register('newTraceLoaded', (trace: any) => {
            console.log(trace);
            call.write({ result: JSON.stringify(trace) });
        });
        ethdebugger.debug(tx);
    })
}