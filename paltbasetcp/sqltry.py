import sqlite3


def insert_iot_data(time, ip, insert_type, data, msg):
    conn = sqlite3.connect('../qtGui/test.db')
    cursor = conn.cursor()
    cursor.execute("insert into iot  values (?,?,?,?,?,?)",
                   (None, time, ip, insert_type, data, msg))
    # 通过rowcount获得插入的行数: print('rowcount =', cursor.rowcount)
    cursor.close()
    conn.commit()
    conn.close()


def show_iot_data(low, high):
    conn = sqlite3.connect('../qtGui/test.db')
    cursor = conn.cursor()
    cursor.execute('select id,time,ip,data from iot where id between ? and ? AND data <> 1', (low, high))
    iot_data = cursor.fetchall()
    show_data = ['{} TIME:{} IP:{} DATA:{}'.format(x[0], x[1], x[2], x[3]) for x in iot_data]
    cursor.close()
    conn.close()
    return show_data


if __name__ == '__main__':
    # 测试主函数
    # insert_iot_data('time', 'ip', 'type', 12.0)
    iot_data = show_iot_data(5, 10)
    print(iot_data)
