// package: greet
// file: services/greet.proto

import * as services_greet_pb from "../services/greet_pb";
import {grpc} from "@improbable-eng/grpc-web";

type GreetServiceGreet = {
  readonly methodName: string;
  readonly service: typeof GreetService;
  readonly requestStream: false;
  readonly responseStream: false;
  readonly requestType: typeof services_greet_pb.GreetRequest;
  readonly responseType: typeof services_greet_pb.GreetResponse;
};

export class GreetService {
  static readonly serviceName: string;
  static readonly Greet: GreetServiceGreet;
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

export class GreetServiceClient {
  readonly serviceHost: string;

  constructor(serviceHost: string, options?: grpc.RpcOptions);
  greet(
    requestMessage: services_greet_pb.GreetRequest,
    metadata: grpc.Metadata,
    callback: (error: ServiceError|null, responseMessage: services_greet_pb.GreetResponse|null) => void
  ): UnaryResponse;
  greet(
    requestMessage: services_greet_pb.GreetRequest,
    callback: (error: ServiceError|null, responseMessage: services_greet_pb.GreetResponse|null) => void
  ): UnaryResponse;
}

