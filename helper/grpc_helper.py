import os
import time
import io
import grpc
import cv2
import numpy as np
import KDMPgRPC_pb2
import KDMPgRPC_pb2_grpc
from concurrent import futures


def StartServer() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    KDMPgRPC_pb2_grpc.add_KDIP_NetServiceServicer_to_server(KDMPgRPC_NetServiceServicer(), server)
    print("server started!")
    server.add_insecure_port('[::]:50052')
    server.start()
    # server.wait_for_termination()
    while (1):
        user_input = input()
        if (user_input == "stop"):
            server.stop(0)
            return

class KDMPgRPC_NetServiceServicer(KDMPgRPC_pb2_grpc.KDIP_NetServiceServicer):

    def ClientSignalService(self, request, context):
        # 현재는 채팅 메시지 전송으로 구현
        message = request.UserMessage
        # 현재 상태에서는 기본적으로 Echo메세지 역할을 하고
        # 특정 단어(signal)를 수신받았을 시 동작을 수행한다.
        # response 구조체 생성
        resultMessage = KDMPgRPC_pb2.Message()
        resultMessage.UserID = "Server"
        resultMessage.UserMessage = message
        print(message)
        if (message == "Sucess Connection"):
            print(message + "!!")
        elif (message == "Start Build"):
            print(message + "!!")
        return resultMessage

    def VisionDataService(self, request, context):
        directory = "Test_Image_File"
        if (not os.path.isdir(directory)):
            return None

        img_file = request.UserMessage

        img = cv2.imread(directory + "/" + img_file)
        #  불러온 이미지 바이트 변환
        img_byte_cv = cv2.imencode('.PNG', img)[1].tobytes()

        # 반환 패킷 생성
        response_packet = KDMPgRPC_pb2.ImageDataPacket(Name=img_file,
                                                       LayerNum=0,
                                                       Datas=img_byte_cv)


        print("Image file transfer completed")
        # 패킷 전송
        return response_packet
