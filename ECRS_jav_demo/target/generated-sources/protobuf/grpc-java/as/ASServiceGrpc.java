package as;

import static io.grpc.MethodDescriptor.generateFullMethodName;
import static io.grpc.stub.ClientCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ClientCalls.asyncClientStreamingCall;
import static io.grpc.stub.ClientCalls.asyncServerStreamingCall;
import static io.grpc.stub.ClientCalls.asyncUnaryCall;
import static io.grpc.stub.ClientCalls.blockingServerStreamingCall;
import static io.grpc.stub.ClientCalls.blockingUnaryCall;
import static io.grpc.stub.ClientCalls.futureUnaryCall;
import static io.grpc.stub.ServerCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ServerCalls.asyncClientStreamingCall;
import static io.grpc.stub.ServerCalls.asyncServerStreamingCall;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedStreamingCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.16.1)",
    comments = "Source: as.proto")
public final class ASServiceGrpc {

  private ASServiceGrpc() {}

  public static final String SERVICE_NAME = "as.ASService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<as.As.ASRequest,
      as.As.ASResponse> getAsCallMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "as_call",
      requestType = as.As.ASRequest.class,
      responseType = as.As.ASResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<as.As.ASRequest,
      as.As.ASResponse> getAsCallMethod() {
    io.grpc.MethodDescriptor<as.As.ASRequest, as.As.ASResponse> getAsCallMethod;
    if ((getAsCallMethod = ASServiceGrpc.getAsCallMethod) == null) {
      synchronized (ASServiceGrpc.class) {
        if ((getAsCallMethod = ASServiceGrpc.getAsCallMethod) == null) {
          ASServiceGrpc.getAsCallMethod = getAsCallMethod = 
              io.grpc.MethodDescriptor.<as.As.ASRequest, as.As.ASResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(
                  "as.ASService", "as_call"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  as.As.ASRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  as.As.ASResponse.getDefaultInstance()))
                  .setSchemaDescriptor(new ASServiceMethodDescriptorSupplier("as_call"))
                  .build();
          }
        }
     }
     return getAsCallMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static ASServiceStub newStub(io.grpc.Channel channel) {
    return new ASServiceStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static ASServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new ASServiceBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static ASServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new ASServiceFutureStub(channel);
  }

  /**
   */
  public static abstract class ASServiceImplBase implements io.grpc.BindableService {

    /**
     */
    public void asCall(as.As.ASRequest request,
        io.grpc.stub.StreamObserver<as.As.ASResponse> responseObserver) {
      asyncUnimplementedUnaryCall(getAsCallMethod(), responseObserver);
    }

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            getAsCallMethod(),
            asyncUnaryCall(
              new MethodHandlers<
                as.As.ASRequest,
                as.As.ASResponse>(
                  this, METHODID_AS_CALL)))
          .build();
    }
  }

  /**
   */
  public static final class ASServiceStub extends io.grpc.stub.AbstractStub<ASServiceStub> {
    private ASServiceStub(io.grpc.Channel channel) {
      super(channel);
    }

    private ASServiceStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ASServiceStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new ASServiceStub(channel, callOptions);
    }

    /**
     */
    public void asCall(as.As.ASRequest request,
        io.grpc.stub.StreamObserver<as.As.ASResponse> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(getAsCallMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   */
  public static final class ASServiceBlockingStub extends io.grpc.stub.AbstractStub<ASServiceBlockingStub> {
    private ASServiceBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private ASServiceBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ASServiceBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new ASServiceBlockingStub(channel, callOptions);
    }

    /**
     */
    public as.As.ASResponse asCall(as.As.ASRequest request) {
      return blockingUnaryCall(
          getChannel(), getAsCallMethod(), getCallOptions(), request);
    }
  }

  /**
   */
  public static final class ASServiceFutureStub extends io.grpc.stub.AbstractStub<ASServiceFutureStub> {
    private ASServiceFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private ASServiceFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ASServiceFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new ASServiceFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<as.As.ASResponse> asCall(
        as.As.ASRequest request) {
      return futureUnaryCall(
          getChannel().newCall(getAsCallMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_AS_CALL = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final ASServiceImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(ASServiceImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_AS_CALL:
          serviceImpl.asCall((as.As.ASRequest) request,
              (io.grpc.stub.StreamObserver<as.As.ASResponse>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  private static abstract class ASServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    ASServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return as.As.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("ASService");
    }
  }

  private static final class ASServiceFileDescriptorSupplier
      extends ASServiceBaseDescriptorSupplier {
    ASServiceFileDescriptorSupplier() {}
  }

  private static final class ASServiceMethodDescriptorSupplier
      extends ASServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final String methodName;

    ASServiceMethodDescriptorSupplier(String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (ASServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new ASServiceFileDescriptorSupplier())
              .addMethod(getAsCallMethod())
              .build();
        }
      }
    }
    return result;
  }
}
