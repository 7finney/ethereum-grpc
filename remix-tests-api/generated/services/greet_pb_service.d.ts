// package: remix_tests
// file: services/greet.proto

import * as services_greet_pb from "../services/greet_pb";
import {grpc} from "@improbable-eng/grpc-web";

type RemixTestsServiceRunTests = {
  readonly methodName: string;
  readonly service: typeof RemixTestsService;
  readonly requestStream: false;
  readonly responseStream: true;
  readonly requestType: typeof services_greet_pb.TestRequest;
  readonly responseType: typeof services_greet_pb.TestResponse;
};

export class RemixTestsService {
  static readonly serviceName: string;
  static readonly RunTests: RemixTestsServiceRunTests;
}

export type ServiceError = { message: string, code: number; metadata: grpc.Metadata }
export type Status = { details: string, code: number; metadata: grpc.Metadata }

interface UnaryResponse {
  cancel(): void;
}
interface ResponseStream<T> {
  cancel(): void;
  on(type: 'data', handler: (message: T) => void): ResponseStream<T>;
  on(type: 'end', handler: (status?: Status) => void): ResponseStream<T>;
  on(type: 'status', handler: (status: Status) => void): ResponseStream<T>;
}
interface RequestStream<T> {
  write(message: T): RequestStream<T>;
  end(): void;
  cancel(): void;
  on(type: 'end', handler: (status?: Status) => void): RequestStream<T>;
  on(type: 'status', handler: (status: Status) => void): RequestStream<T>;
}
interface BidirectionalStream<ReqT, ResT> {
  write(message: ReqT): BidirectionalStream<ReqT, ResT>;
  end(): void;
  cancel(): void;
  on(type: 'data', handler: (message: ResT) => void): BidirectionalStream<ReqT, ResT>;
  on(type: 'end', handler: (status?: Status) => void): BidirectionalStream<ReqT, ResT>;
  on(type: 'status', handler: (status: Status) => void): BidirectionalStream<ReqT, ResT>;
}

export class RemixTestsServiceClient {
  readonly serviceHost: string;

  constructor(serviceHost: string, options?: grpc.RpcOptions);
  runTests(requestMessage: services_greet_pb.TestRequest, metadata?: grpc.Metadata): ResponseStream<services_greet_pb.TestResponse>;
}

