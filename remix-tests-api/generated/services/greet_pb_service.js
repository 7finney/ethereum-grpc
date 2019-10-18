// package: greet
// file: services/greet.proto

var services_greet_pb = require("../services/greet_pb");
var grpc = require("@improbable-eng/grpc-web").grpc;

var GreetService = (function () {
  function GreetService() {}
  GreetService.serviceName = "greet.GreetService";
  return GreetService;
}());

GreetService.Greet = {
  methodName: "Greet",
  service: GreetService,
  requestStream: false,
  responseStream: false,
  requestType: services_greet_pb.GreetRequest,
  responseType: services_greet_pb.GreetResponse
};

exports.GreetService = GreetService;

function GreetServiceClient(serviceHost, options) {
  this.serviceHost = serviceHost;
  this.options = options || {};
}

GreetServiceClient.prototype.greet = function greet(requestMessage, metadata, callback) {
  if (arguments.length === 2) {
    callback = arguments[1];
  }
  var client = grpc.unary(GreetService.Greet, {
    request: requestMessage,
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport,
    debug: this.options.debug,
    onEnd: function (response) {
      if (callback) {
        if (response.status !== grpc.Code.OK) {
          var err = new Error(response.statusMessage);
          err.code = response.status;
          err.metadata = response.trailers;
          callback(err, null);
        } else {
          callback(null, response.message);
        }
      }
    }
  });
  return {
    cancel: function () {
      callback = null;
      client.close();
    }
  };
};

exports.GreetServiceClient = GreetServiceClient;

