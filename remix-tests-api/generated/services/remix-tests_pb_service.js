// package: remix_tests
// file: services/remix-tests.proto

var services_remix_tests_pb = require("../services/remix-tests_pb");
var grpc = require("@improbable-eng/grpc-web").grpc;

var RemixTestsService = (function () {
  function RemixTestsService() {}
  RemixTestsService.serviceName = "remix_tests.RemixTestsService";
  return RemixTestsService;
}());

RemixTestsService.RunTests = {
  methodName: "RunTests",
  service: RemixTestsService,
  requestStream: false,
  responseStream: true,
  requestType: services_remix_tests_pb.TestRequest,
  responseType: services_remix_tests_pb.TestResponse
};

exports.RemixTestsService = RemixTestsService;

function RemixTestsServiceClient(serviceHost, options) {
  this.serviceHost = serviceHost;
  this.options = options || {};
}

RemixTestsServiceClient.prototype.runTests = function runTests(requestMessage, metadata) {
  var listeners = {
    data: [],
    end: [],
    status: []
  };
  var client = grpc.invoke(RemixTestsService.RunTests, {
    request: requestMessage,
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport,
    debug: this.options.debug,
    onMessage: function (responseMessage) {
      listeners.data.forEach(function (handler) {
        handler(responseMessage);
      });
    },
    onEnd: function (status, statusMessage, trailers) {
      listeners.status.forEach(function (handler) {
        handler({ code: status, details: statusMessage, metadata: trailers });
      });
      listeners.end.forEach(function (handler) {
        handler({ code: status, details: statusMessage, metadata: trailers });
      });
      listeners = null;
    }
  });
  return {
    on: function (type, handler) {
      listeners[type].push(handler);
      return this;
    },
    cancel: function () {
      listeners = null;
      client.close();
    }
  };
};

exports.RemixTestsServiceClient = RemixTestsServiceClient;

