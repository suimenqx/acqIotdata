from PyQt5 import QtWidgets
from udp_IOTplat import udp_ui
from udp_IOTplat import stopThreading
from udp_IOTplat import sqltry
import socket
import threading
import sys


class UdpLogic(udp_ui.ToolsUi):
    def __init__(self, num):
        super(UdpLogic, self).__init__(num)
        self.udp_socket = None
        self.address = None
        self.sever_th = None
        self.client_socket_list = list()

    def udp_server_start(self):
        """
        开启UDP服务端方法
        :return:
        """
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            port = int(self.lineEdit_port.text())
            address = ('', port)
            self.udp_socket.bind(address)
        except Exception as ret:
            msg = '请检查端口号\n'
            self.signal_write_msg.emit(msg)
        else:
            self.sever_th = threading.Thread(target=self.udp_server_concurrency)
            self.sever_th.start()
            msg = 'UDP服务端正在监听端口:{}\n'.format(port)
            self.signal_write_msg.emit(msg)

    def udp_server_concurrency(self):
        """
        用于创建一个线程持续监听UDP通信
        :return:
        """
        while True:
            recv_msg, recv_addr = self.udp_socket.recvfrom(1024)
            msg = recv_msg.decode('utf-8')
            self.client_socket_list.append((str(recv_addr[0]), 26711))
            self.client_socket_list = list(set(self.client_socket_list))
            # self.client_socket_list.append(recv_addr)
            msg = '来自IP:{}端口:{}:\n{}\n'.format(recv_addr[0], recv_addr[1], msg)
            self.signal_write_msg.emit(msg)

    def udp_client_start(self):
        """
        确认UDP客户端的ip及地址
        :return:
        """
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.address = (str(self.lineEdit_ip_send.text()), int(self.lineEdit_port.text()))
        except Exception as ret:
            msg = '请检查目标IP，目标端口\n'
            self.signal_write_msg.emit(msg)
        else:
            msg = 'UDP客户端已启动\n'
            self.signal_write_msg.emit(msg)

    def udp_send(self):
        """
        功能函数，用于UDP客户端发送消息
        :return: None
        """
        send_msg = str(self.textEdit_send.toPlainText()).split(' ')
        if send_msg[0] == 'show':
            send_msg_min = send_msg[1]
            send_msg_max = send_msg[2]
            self.signal_write_msg.emit('查询结果：\n')
            show_data = sqltry.show_iot_data(send_msg_min, send_msg_max)
            for i in range(len(show_data)):
                self.signal_write_msg.emit(show_data[i] + '\n')
        else:
            if self.link is False:
                msg = '请选择服务，并点击连接网络\n'
                self.signal_write_msg.emit(msg)
            else:
                try:
                    send_msg = (str(self.textEdit_send.toPlainText())).encode('utf-8')
                    if self.comboBox_tcp.currentIndex() == 0:
                        for client_address in self.client_socket_list:
                            # try:
                            #     self.udp_socket.sendto(send_msg, client_address)
                            #     msg = 'UDP IOT Server已发送\n'
                            #     self.signal_write_msg.emit(msg)
                            # except Exception  as ret:
                            #     del self.client_socket_list[0]
                            try:
                                self.udp_client_socket.sendto(send_msg, client_address)
                                msg = 'UDP IOT Server已发送\n'
                                self.signal_write_msg.emit(msg)
                            except Exception as ret:
                                msg = '发送失败\n'
                                self.signal_write_msg.emit(msg)
                    if self.comboBox_tcp.currentIndex() == 1:
                        self.udp_socket.sendto(send_msg, self.address)
                        msg = 'UDP Iot Client已发送\n'
                        self.signal_write_msg.emit(msg)
                except Exception as ret:
                    msg = '发送失败\n'
                    self.signal_write_msg.emit(msg)

    def udp_close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        if self.comboBox_tcp.currentIndex() == 0:
            try:
                self.udp_socket.close()
                if self.link is True:
                    msg = '已断开网络\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                pass
        if self.comboBox_tcp.currentIndex() == 1:
            try:
                self.udp_socket.close()
                if self.link is True:
                    msg = '已断开网络\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                pass
        try:
            stopThreading.stop_thread(self.sever_th)
        except Exception:
            pass
        try:
            stopThreading.stop_thread(self.client_th)
        except Exception:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = UdpLogic(1)
    ui.show()
    sys.exit(app.exec_())
