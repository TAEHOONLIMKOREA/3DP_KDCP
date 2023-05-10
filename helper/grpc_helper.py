import os
import sqlite3
import grpc
import cv2
import KDCPgRPC_pb2
import KDCPgRPC_pb2_grpc
from concurrent import futures


def StartServer() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    KDCPgRPC_pb2_grpc.add_KDIP_NetServiceServicer_to_server(KDCPgRPC_NetServiceServicer(), server)
    print("server started!")
    server.add_insecure_port('[::]:50052')
    server.start()
    # server.wait_for_termination()
    while (1):
        user_input = input()
        if (user_input == "stop"):
            server.stop(0)
            return

class KDCPgRPC_NetServiceServicer(KDCPgRPC_pb2_grpc.KDIP_NetServiceServicer):

    def ClientSignalService(self, request, context):
        try:
            # 현재는 채팅 메시지 전송으로 구현
            message = request.UserMessage
            # 현재 상태에서는 기본적으로 Echo메세지 역할을 하고
            # 특정 단어(signal)를 수신받았을 시 동작을 수행한다.
            # response 구조체 생성
            resultMessage = KDCPgRPC_pb2.Message()
            resultMessage.UserID = "Server"
            resultMessage.UserMessage = message
            print(message)
            if (message == "Check Connection"):
                print("Sucess Connection!!")
                resultMessage.UserMessage = "Sucess Connection!!"

            return resultMessage
        except Exception as e:
            print("gRPC-ClientSignalService : " + str(e))

    def VisionDataService(self, request, context):
        try:
            BASE_DIR = os.path.abspath('.')
            TARGET_DIR = os.path.join(BASE_DIR, "HMI")
            TARGET_FILE = 'K3DGConfiguration.db'
            TARGET_FILE_FULL_PATH = os.path.join(TARGET_DIR, TARGET_FILE)
            con = sqlite3.connect(TARGET_FILE_FULL_PATH)
            cur = con.cursor()

            cur.execute("SELECT * FROM ConfigTable")
            rows = cur.fetchall()
            vision_data_dirpath = rows[0][5]
            print(vision_data_dirpath)

            if (not os.path.isdir(vision_data_dirpath)):
                return None

            img_file = request.UserMessage + ".png"
            img = cv2.imread(vision_data_dirpath + "/" + img_file)

            #  불러온 이미지 바이트 변환
            img_byte_cv = cv2.imencode('.PNG', img)[1].tobytes()

            # 반환 패킷 생성
            response_packet = KDCPgRPC_pb2.ImageDataPacket(Name=img_file,
                                                           LayerNum=0,
                                                           Datas=img_byte_cv)
            print("Image file transfer completed")

            # 패킷 전송
            return response_packet

        except Exception as e:
            print("gRPC-VisionDataService : " + str(e))

