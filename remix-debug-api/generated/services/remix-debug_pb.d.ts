// package: remix_debug
// file: services/remix-debug.proto

import * as jspb from "google-protobuf";

export class DebugInterface extends jspb.Message {
  getCommand(): string;
  setCommand(value: string): void;

  getPayload(): string;
  setPayload(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DebugInterface.AsObject;
  static toObject(includeInstance: boolean, msg: DebugInterface): DebugInterface.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: DebugInterface, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DebugInterface;
  static deserializeBinaryFromReader(message: DebugInterface, reader: jspb.BinaryReader): DebugInterface;
}

export namespace DebugInterface {
  export type AsObject = {
    command: string,
    payload: string,
  }
}

export class DebugRequest extends jspb.Message {
  hasDebuginterface(): boolean;
  clearDebuginterface(): void;
  getDebuginterface(): DebugInterface | undefined;
  setDebuginterface(value?: DebugInterface): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DebugRequest.AsObject;
  static toObject(includeInstance: boolean, msg: DebugRequest): DebugRequest.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: DebugRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DebugRequest;
  static deserializeBinaryFromReader(message: DebugRequest, reader: jspb.BinaryReader): DebugRequest;
}

export namespace DebugRequest {
  export type AsObject = {
    debuginterface?: DebugInterface.AsObject,
  }
}

export class DebugResponse extends jspb.Message {
  getResult(): string;
  setResult(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DebugResponse.AsObject;
  static toObject(includeInstance: boolean, msg: DebugResponse): DebugResponse.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: DebugResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DebugResponse;
  static deserializeBinaryFromReader(message: DebugResponse, reader: jspb.BinaryReader): DebugResponse;
}

export namespace DebugResponse {
  export type AsObject = {
    result: string,
  }
}

