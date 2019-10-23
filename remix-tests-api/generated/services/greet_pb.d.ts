// package: remix_tests
// file: services/greet.proto

import * as jspb from "google-protobuf";

export class Greeting extends jspb.Message {
  getFirstName(): string;
  setFirstName(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Greeting.AsObject;
  static toObject(includeInstance: boolean, msg: Greeting): Greeting.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Greeting, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Greeting;
  static deserializeBinaryFromReader(message: Greeting, reader: jspb.BinaryReader): Greeting;
}

export namespace Greeting {
  export type AsObject = {
    firstName: string,
  }
}

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

export class GreetRequest extends jspb.Message {
  hasGreeting(): boolean;
  clearGreeting(): void;
  getGreeting(): Greeting | undefined;
  setGreeting(value?: Greeting): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): GreetRequest.AsObject;
  static toObject(includeInstance: boolean, msg: GreetRequest): GreetRequest.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: GreetRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): GreetRequest;
  static deserializeBinaryFromReader(message: GreetRequest, reader: jspb.BinaryReader): GreetRequest;
}

export namespace GreetRequest {
  export type AsObject = {
    greeting?: Greeting.AsObject,
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

export class GreetResponse extends jspb.Message {
  getResult(): string;
  setResult(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): GreetResponse.AsObject;
  static toObject(includeInstance: boolean, msg: GreetResponse): GreetResponse.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: GreetResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): GreetResponse;
  static deserializeBinaryFromReader(message: GreetResponse, reader: jspb.BinaryReader): GreetResponse;
}

export namespace GreetResponse {
  export type AsObject = {
    result: string,
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

