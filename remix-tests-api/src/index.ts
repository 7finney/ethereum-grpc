require('module-alias/register')
var PROTO_PATH = './services/greet.proto'
import * as grpc from 'grpc'
import * as protoLoader from '@grpc/proto-loader'
import { GreetResponse } from "generated/services/greet_pb"
import { runTestSources } from 'remix-tests'

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
})
var protoDescriptor = grpc.loadPackageDefinition(packageDefinition) as any;

var remix_tests_pb = protoDescriptor.remix_tests;

var greetServer = new grpc.Server();
greetServer.addService(remix_tests_pb.RemixTestsService.service, {
    RunTests: greet,
});
greetServer.bind('0.0.0.0:50051', grpc.ServerCredentials.createInsecure());
console.log('Server running at 0.0.0.0:50051')
greetServer.start();

function greet(call: any) {
    let result = new GreetResponse();
    const sources: Object = JSON.parse(JSON.stringify({"string.sol":{"content":"pragma solidity ^0.5.0;\n\ncontract Strings {\n    function get() public view returns (string memory res) {\n        return \"Hello\";\n    }\n}\n"},"string_test.sol":{"content":"pragma solidity ^0.5.0;\nimport 'string.sol';\n\ncontract StringTest {\n    Strings foo;\n\n    function beforeAll() public {\n        foo = new Strings();\n    }\n\n    function initialValueShouldBeHello() public returns (bool) {\n        return Assert.equal(foo.get(), \"Hello\", \"initial value is correct\");\n    }\n\n    function initialValueShouldNotBeHelloWorld() public returns (bool) {\n        return Assert.notEqual(foo.get(), \"Hello world\", \"initial value is correct\");\n    }\n}\n"}}));
    const _finalCallback = function(err: any, response: any) {
        console.log("final : ", response);
        result.setResult(JSON.stringify(response));
        call.write({ result });
        call.end();
    }
    const _testCallback = function(response: any) {
        console.log("test : ", response);
        result.setResult(JSON.stringify(response));
        call.write({ result });
    }
    const _resultCallback = function(err: any, response: any) {
        console.log("result : ", response);
    }
    const _importFileCb = function(e: any, result: any) {
        if(e) {
            console.error(e)
        }
        return;
    }
    runTestSources(sources, _testCallback, _resultCallback, _finalCallback, _importFileCb, null);
}
