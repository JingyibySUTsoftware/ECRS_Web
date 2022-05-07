package as;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.StatusRuntimeException;
import item_info.ItemInfoOuterClass;
import user_info.UserInfoOuterClass;

import java.util.List;
import java.util.concurrent.TimeUnit;

/**
 * @author jingyi
        * @Classname Client
        * @description TODO
        * @date 2022/5/6 15:30
        */
public class Client {

    private final ManagedChannel channel;
    private final ASServiceGrpc.ASServiceBlockingStub blockingStub;

    /**
     * Construct client connecting to HelloWorld server at {@code host:port}.
     */
    public Client(String host, int port) {

        channel = ManagedChannelBuilder.forAddress(host, port)
                .usePlaintext()
                .build();
        blockingStub = ASServiceGrpc.newBlockingStub(channel);
    }

    public void shutdown() throws InterruptedException {
        channel.shutdown().awaitTermination(5, TimeUnit.SECONDS);
    }

    /**
     * Say hello to server.
     */
    public void ApplicationServer(String uid) {
        As.ASRequest  request = As.ASRequest.newBuilder().setUserId(uid).build();
        As.ASResponse response;
        try {
            response = blockingStub.asCall(request);
        } catch (StatusRuntimeException e) {
            System.out.println("RPC failed: {0}"+ e.getStatus());
            return;
        }
        System.out.println("Application服务结果为：");
        System.out.println(response.getError());
        List<ItemInfoOuterClass.ItemInfo> list = response.getItemInfosList();
        for (ItemInfoOuterClass.ItemInfo item:list){
            System.out.println(item);
        }
    }

    public void ApplicationServer(String uid,String age,String sex,String city_level,String province,String city,String country) {
        UserInfoOuterClass.UserInfo.Builder builder = UserInfoOuterClass.UserInfo.newBuilder().setUserId(uid).setAge(age).setSex(sex).setCityLevel(city_level).setProvince(province).setCity(city).setCountry(country);
        As.ASRequest  request = As.ASRequest.newBuilder().setUserInfo(builder).build();
        As.ASResponse response;
        try {
            response = blockingStub.asCall(request);
        } catch (StatusRuntimeException e) {
            System.out.println("RPC failed: {0}"+ e.getStatus());
            return;
        }
        System.out.println("Application服务结果为：");
        System.out.println(response.getError());
        List<ItemInfoOuterClass.ItemInfo> list = response.getItemInfosList();
        for (ItemInfoOuterClass.ItemInfo item:list){
            System.out.println(item);
        }
    }

    /**
     * Greet server. If provided, the first element of {@code args} is the name to use in the
     * greeting.
     */
    public static void main(String[] args) throws Exception {
        Client client = new Client("127.0.0.1", 8930);
        try {
            client.ApplicationServer(String.valueOf(0),String.valueOf(1),String.valueOf(0),String.valueOf(2),String.valueOf(2),String.valueOf(348),String.valueOf(741));
            //client.ApplicationServer(String.valueOf(1));
        } finally {
            client.shutdown();
        }
    }

}