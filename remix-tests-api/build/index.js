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
var remix_tests_1 = require("remix-tests");
var packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
});
var protoDescriptor = grpc.loadPackageDefinition(packageDefinition);
var remix_tests_pb = protoDescriptor.remix_tests;
var greetServer = new grpc.Server();
greetServer.addService(remix_tests_pb.RemixTestsService.service, {
    RunTests: greet,
});
greetServer.bind('0.0.0.0:50051', grpc.ServerCredentials.createInsecure());
console.log('Server running at 0.0.0.0:50051');
greetServer.start();
function greet(call) {
    console.log("Request :", call.request.greeting.first_name);
    var result = new greet_pb_1.GreetResponse();
    var sources = JSON.parse(JSON.stringify({ "string.sol": { "content": "pragma solidity ^0.5.0;\n\ncontract Strings {\n    function get() public view returns (string memory res) {\n        return \"Hello\";\n    }\n}\n" }, "string_test.sol": { "content": "pragma solidity ^0.5.0;\nimport 'string.sol';\n\ncontract StringTest {\n    Strings foo;\n\n    function beforeAll() public {\n        foo = new Strings();\n    }\n\n    function initialValueShouldBeHello() public returns (bool) {\n        return Assert.equal(foo.get(), \"Hello\", \"initial value is correct\");\n    }\n\n    function initialValueShouldNotBeHelloWorld() public returns (bool) {\n        return Assert.notEqual(foo.get(), \"Hello world\", \"initial value is correct\");\n    }\n}\n" } }));
    var _finalCallback = function (err, response) {
        console.log("final : ", response);
        result.setResult(JSON.stringify(response));
        call.write({ result: result });
        call.end();
    };
    var _testCallback = function (response) {
        console.log("test : ", response);
        result.setResult(JSON.stringify(response));
        call.write({ result: result });
    };
    var _resultCallback = function (err, response) {
        console.log("result : ", response);
    };
    var _importFileCb = function (e, result) {
        if (e) {
            console.error(e);
        }
        return;
    };
    remix_tests_1.runTestSources(sources, _testCallback, _resultCallback, _finalCallback, _importFileCb, null);
    // result.setResult("Greetings " + call.request.greeting.first_name)
    // callback(null, {
    //     result
    // });
}
