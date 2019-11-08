// package: remix_debug
// file: services/remix-debug.proto

import * as services_remix_debug_pb from "../services/remix-debug_pb";
import {grpc} from "@improbable-eng/grpc-web";

type RemixDebugServiceRunDebug = {
  readonly methodName: string;
  readonly service: typeof RemixDebugService;
  readonly requestStream: false;
  readonly responseStream: true;
  readonly requestType: typeof services_remix_debug_pb.DebugRequest;
  readonly responseType: typeof services_remix_debug_pb.DebugResponse;
};

export class RemixDebugService {
  static readonly serviceName: string;
  static readonly RunDebug: RemixDebugServiceRunDebug;
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

export class RemixDebugServiceClient {
  readonly serviceHost: string;

  constructor(serviceHost: string, options?: grpc.RpcOptions);
  runDebug(requestMessage: services_remix_debug_pb.DebugRequest, metadata?: grpc.Metadata): ResponseStream<services_remix_debug_pb.DebugResponse>;
}

