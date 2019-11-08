// package: remix_debug
// file: services/remix-debug.proto

var services_remix_debug_pb = require("../services/remix-debug_pb");
var grpc = require("@improbable-eng/grpc-web").grpc;

var RemixDebugService = (function () {
  function RemixDebugService() {}
  RemixDebugService.serviceName = "remix_debug.RemixDebugService";
  return RemixDebugService;
}());

RemixDebugService.RunDebug = {
  methodName: "RunDebug",
  service: RemixDebugService,
  requestStream: false,
  responseStream: true,
  requestType: services_remix_debug_pb.DebugRequest,
  responseType: services_remix_debug_pb.DebugResponse
};

exports.RemixDebugService = RemixDebugService;

function RemixDebugServiceClient(serviceHost, options) {
  this.serviceHost = serviceHost;
  this.options = options || {};
}

RemixDebugServiceClient.prototype.runDebug = function runDebug(requestMessage, metadata) {
  var listeners = {
    data: [],
    end: [],
    status: []
  };
  var client = grpc.invoke(RemixDebugService.RunDebug, {
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

exports.RemixDebugServiceClient = RemixDebugServiceClient;

