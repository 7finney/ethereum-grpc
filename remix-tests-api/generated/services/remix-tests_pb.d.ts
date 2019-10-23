// package: remix_tests
// file: services/remix-tests.proto

import * as jspb from "google-protobuf";

export class TestInterface extends jspb.Message {
  getCommand(): string;
  setCommand(value: string): void;

  getPayload(): string;
  setPayload(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): TestInterface.AsObject;
  static toObject(includeInstance: boolean, msg: TestInterface): TestInterface.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: TestInterface, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): TestInterface;
  static deserializeBinaryFromReader(message: TestInterface, reader: jspb.BinaryReader): TestInterface;
}

export namespace TestInterface {
  export type AsObject = {
    command: string,
    payload: string,
  }
}

export class TestRequest extends jspb.Message {
  hasTestinterface(): boolean;
  clearTestinterface(): void;
  getTestinterface(): TestInterface | undefined;
  setTestinterface(value?: TestInterface): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): TestRequest.AsObject;
  static toObject(includeInstance: boolean, msg: TestRequest): TestRequest.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: TestRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): TestRequest;
  static deserializeBinaryFromReader(message: TestRequest, reader: jspb.BinaryReader): TestRequest;
}

export namespace TestRequest {
  export type AsObject = {
    testinterface?: TestInterface.AsObject,
  }
}

export class TestResponse extends jspb.Message {
  getResult(): string;
  setResult(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): TestResponse.AsObject;
  static toObject(includeInstance: boolean, msg: TestResponse): TestResponse.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: TestResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): TestResponse;
  static deserializeBinaryFromReader(message: TestResponse, reader: jspb.BinaryReader): TestResponse;
}

export namespace TestResponse {
  export type AsObject = {
    result: string,
  }
}

