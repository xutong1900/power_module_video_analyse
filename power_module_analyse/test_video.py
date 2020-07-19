
# -*- coding:utf-8 -*-
import cv2
import numpy as np
import os
import time
import queue
import threading

record_time = 0
# # camera = cv2.VideoCapture(0) # 参数0表示第一个摄像头
# # camera = cv2.VideoCapture("test_video.mp4") # 从文件读取视频
# # print('Input the video path:')
def init_basic():
    global record_time
    print('输入视频绝对路径：1 = rtsp://admin:beijingsiasun@192.168.191.1:554/stream1  2 = 自定义（xx:/yy/zz.mp4）')
    # print('输入摄像头序号')

    global paths, on_yz_1, on_yz_2, on_time_yz_1
    paths_option = input()
    if int(paths_option) == 1:
        paths = 'rtsp://admin:beijingsiasun@192.168.191.1:554/stream1'
        print('默认路径')
        # paths = 'E:\pycharm\power_date_analyse\Test_video.mp4'
    else:
        print('请输入自定义路径：xx:/yy/zz.mp4')
        paths = input()
        print('自定义路径')
        print(paths)


    # print('you input ', paths)

    print('选择设置：1=默认，2=自定义')
    select = input()
    # select = 1
    if int(select) == 1:
        on_yz_1 = 5000
        on_yz_2 = 5000
        on_time_yz_1 = 2000
    else:
        print('输入开阈值1：推荐5000，可自行调节。。')
        on_yz_1 = input()
        print('you input ', on_yz_1)

        print('输入开阈值2：推荐5000，可自行调节。。')
        on_yz_2 = input()
        print('you input ', on_yz_2)

        print('输入时长阈值1：推荐2000，可自行调节。。')
        on_time_yz_1 = input()
        print('you input ', on_time_yz_1)

    print('请输入监控时长：xx小时')

    record_time = int(input())
    if record_time > 100 or record_time < 0:
        record_time = 21
    print(record_time)


# print('Open0')
# # camera = cv2.VideoCapture('%s'%paths) # 从文件读取视频
# # camera = cv2.VideoCapture('rtsp://admin:beijingsiasun@192.168.191.1:554/stream1') # 从网络摄像头读取视频   IPC
# camera = cv2.VideoCapture('rtsp://admin:beijingsiasun@192.168.191.1/stream1') # 从网络摄像头读取视频 NVR
# # camera = cv2.VideoCapture('E:\pycharm\power_date_analyse\Test_video.mp4') # 从文件读取视频
# # camera = cv2.VideoCapture(int(paths)) # 从文件读取视频
# # camera = cv2.VideoCapture(r'E:\\Testvideo.mp4') # 从文件读取视频
# # camera = cv2.VideoCapture("1.mp4") # 从文件读取视频
# print('Open1')
# c = 0
# # 判断视频是否打开
# if (camera.isOpened()):
#     print('Open')
# else:
#     print('Fail to open!')
#
# #------------------------------------------------------------------------------------
# # 选择视频的第一帧图像，并保存，作为后续框选识别区域的模板
# #------------------------------------------------------------------------------------
# vc = camera
# while c < 1:
#     rval, frame = vc.read()
#     # cv2.imwrite('E:\pycharm\power_date_analyse\select_area.jpg', frame)
#     # cv2.imwrite(r'E:\\selectarea.jpg', frame)
#     cv2.imwrite('selectarea.jpg', frame)
#     c = c + 1
#     # print(c)
#     k = cv2.waitKey(1)
#     if k == ord('s'):  # wait for 's' key to save and exit
#         print('you input "s",the picture with select area will be saved')
#         cv2.destroyAllWindows()
#         break
#     else:
#         cv2.destroyAllWindows()
# #------------------------------------------------------------------------------------
# #划定识别区域，使用之前保存的第一帧图像
# #------------------------------------------------------------------------------------
# k = 0
# num = 0
# point_list = []
#
# # img = cv2.imread("E:\pycharm\power_date_analyse\select_area.jpg")
# # img = cv2.imread(r'E:\\selectarea.jpg')
# img = cv2.imread('selectarea.jpg')
# while(k != ord('q')):
#     num += 1
#     # img = imutils.resize(img, width=500)
#     print('绘制蓝色矩形框，并按下回车确认，矩形框变为红色;')
#
#     roi = cv2.selectROI(windowName="roi", img=img, showCrosshair=True, fromCenter=False)
#     x, y, w, h = roi
#
#     cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2)
#     point_list.append(((x, y), (x + w, y + h)))
#     # print(num,point_list[num-1])
#     print('第 %d 次的坐标是: ' % num, point_list[num-1])
#     cv2.putText(img, str(num), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
#     cv2.imshow("roi", img)
#     print('保存请按 s ;','继续绘制下一个矩形框，请按回车')
#
#     k = cv2.waitKey(0)   #检测到按键，最后退出
#     if k == ord('s'):  # wait for 's' key to save and exit
#         # print(k)
#         # print(point_list)
#         cv2.imwrite('E:\pycharm\power_date_analyse\modole.png',img)
#         print('you input "s",the picture with select area will be saved')
#         # print((x,y),(x+w,y+h))
#         cv2.destroyAllWindows()
#         break
#     else:
#         cv2.destroyAllWindows()
# # print(point_list[0][0])
#
#
# start_time = time.time()
# # ------------------------------------------------------------------------------------
# #读取视频，按照之前选定的区域，计算选定区域的像素值，并实时判断显示在视频中
# #-------------------------------------------------------------------------------------
# # # 测试用,查看视频size
# # size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
# #        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# # print 'size:'+repr(size)
#
# rectangleCols = 30
# pixel_sum_old = 0
# data_result = []
# for count in range(len(point_list)):
#     data_result.append(list())
# # print(data_result)
# while True:
#     end_time = time.time()
#     print("Cost time: %d 分钟 %d 秒" %((end_time - start_time)/60,(end_time - start_time)%60))
#     # data_result.append(list())
#     m = 0
#     grabbed, frame_lwpCV = camera.read() # 逐帧采集视频流
#     if not grabbed:
#         break
#     if c % 29 == 0: #每29帧读取1帧
#         gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY) # 转灰度图
#         frame_data = np.array(gray_lwpCV)  # 每一帧循环存入数组
#         for point_x_y in point_list:    #point_x_y 包含矩形区域的对角坐标，[0]为左上角xy，[1]为右下角xy
#             box_data = frame_data[point_x_y[0][1]:point_x_y[1][1]] # 取矩形目标区域的竖边，即二维数组的行
#             box_data = box_data[:, point_x_y[0][0]:point_x_y[1][0]] # 取矩形目标区域的宽边，即二维数组的列
#             pixel_sum = np.sum(box_data) # 行求和q
#             data_result[m].append(pixel_sum)
#         #     # print('new: %d,old: %d, new-old: %d' %(pixel_sum, pixel_sum_old, pixel_sum-pixel_sum_old))
#         #     # length = len(gray_lwpCV)
#         #     # length = 30
#         #     # x = range(length)
#         #
#             # 画目标区域
#             lwpCV_box = cv2.rectangle(frame_lwpCV, point_x_y[0], point_x_y[1], (0, 255, 0), 2)
#             # if pixel_sum > pixel_sum_old :
#             #     if pixel_sum - pixel_sum_old >= 5000:
#             cv2.putText(frame_lwpCV, str(pixel_sum), point_x_y[0],cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
#                     # cv2.putText(frame_lwpCV, 'on', point_x_y[0],cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
#             # else:
#             #     cv2.putText(frame_lwpCV, str(pixel_sum), point_x_y[0],cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
#             #     cv2.putText(frame_lwpCV, 'off', point_x_y[0],cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
#             cv2.imshow('lwpCVWindow', frame_lwpCV) # 显示采集到的视频流
#             # pixel_sum_old = pixel_sum
#             # m = m + 1
#             # print(m)
#     c = c + 1
#     # for res in range(len(point_list)):
#     #     print(data_result[res])
#     # print(data_result)
#     key = cv2.waitKey(2) & 0xFF
#     if key == ord('q'):
#         break
# camera.release()
# cv2.destroyAllWindows()


# ------------------------------------------------------------------------------------
# 使用多线程，读取视频，按照之前选定的区域，计算选定区域的像素值，并实时判断显示在视频中
# -------------------------------------------------------------------------------------



q = queue.Queue()
on_yz_1 = 5000
on_yz_2 = 5000
on_time_yz_1 = 2000

# global point_list, start_time, flag
# global data_result
old_start_time = time.asctime()
point_list = []
# point_list = [((1298, 115), (1319, 136)), ((1328, 118), (1344, 136)), ((1300, 196), (1319, 220)), ((1335, 203), (1351, 225)), ((1300, 292), (1319, 315)), ((1332, 294), (1347, 319)), ((1299, 386), (1320, 411)), ((1330, 386), (1350, 413)), ((1296, 482), (1317, 512)), ((1330, 482), (1351, 511)), ((1291, 580), (1314, 607)), ((1324, 581), (1345, 609)), ((1285, 674), (1306, 702)), ((1320, 679), (1339, 702)), ((1281, 768), (1302, 794)), ((1313, 771), (1332, 796)), ((1274, 856), (1295, 881)), ((1305, 855), (1324, 881)), ((1264, 938), (1284, 966)), ((1299, 943), (1315, 962)), ((757, 94), (778, 114)), ((754, 186), (774, 212)), ((745, 266), (769, 294)), ((738, 367), (757, 396)), ((732, 452), (756, 480)), ((732, 554), (754, 583)), ((732, 643), (756, 670)), ((735, 742), (756, 773)), ((734, 816), (754, 846)), ((733, 910), (755, 935)), ((1061, 86), (1084, 113)), ((1065, 181), (1087, 210)), ((1062, 265), (1086, 295)), ((1061, 371), (1081, 398)), ((1057, 456), (1082, 485)), ((1053, 563), (1076, 591)), ((1048, 653), (1074, 685)), ((1040, 757), (1065, 788)), ((1039, 836), (1066, 867)), ((1036, 934), (1060, 964)), ((1251, 198), (1275, 224)), ((1247, 286), (1273, 319))]
data_result = []
data_result_time = []
count_frame = 0
start_time = time.time()
flag = 0
flag1 = 0


def receive():
    global point_list, start_time, flag
    global data_result
    global count_frame
    global flag, flag1
    print("start Reveive")
    # cap = cv2.VideoCapture('rtsp://admin:beijingsiasun@192.168.191.1/stream1')
    cap = cv2.VideoCapture('%s'%paths)
    ret, frame = cap.read()
    q.put(frame)
    count_frame = 0
    while True:
        ret, frame = cap.read()
        if not (ret):
            flag1 = 2
            # cap = cv2.VideoCapture('rtsp://admin:beijingsiasun@192.168.191.1/stream1')
            cap = cv2.VideoCapture('%s'%paths)
            # cap = cv2.VideoCapture('E:\pycharm\power_date_analyse\Test_video.mp4')
            ret, frame = cap.read()
            continue
        if count_frame % 45 == 0:
            q.put(frame)

        count_frame += 1
        # if count_frame == 30000:
        #     count_frame = 0
        if flag == 2:
            flag = 0
            flag1 = 2
        if flag == 1:
            print('退出线程1.')
            break
        key1 = cv2.waitKey(2) & 0xFF


def Display():
    global point_list, start_time, flag
    global data_result,data_result_time
    global old_start_time
    global record_time
    global flag1

    print("Start Displaying")
    while True:

        if q.empty() != True:
            frame = q.get()
            start_time = time.time()

            for count in range(len(point_list)):
                data_result.append(list())
                data_result_time.append(list())
            # print(data_result)
            # old_start_time = time.asctime()
            old_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            while True:
                end_time = time.time()

                print("Cost time: %d 小时 %d 分钟 %d 秒" % (int((end_time - start_time) / 3600), int((end_time - start_time) % 3600 / 60), (end_time - start_time) % 60))
                print(q.qsize())
                if int((end_time - start_time) / 3600) == record_time:
                # if int((end_time - start_time) % 3600 / 60) == record_time:
                    cv2.destroyAllWindows()
                    # print(int((end_time - start_time) / 3600),record_time)
                    print('退出线程2.1.')
                    # print(data_result)
                    flag1 = 2
                    flag = 1
                    break
                # data_result.append(list())
                # with open(r'source_result_report.txt', 'w') as newfile1:
                #     for ele in data_result:
                #         # print('时间为：第 %d 小时 %d 分钟 %d 秒,时长：%d秒'%(2*res[0]/3600,2*res[0]/60,2*res[0]%60,2*res[1]))
                #         # print(res)
                #         newfile1.write(str(old_start_time))
                #         newfile1.write('---')
                #         newfile1.write(str(time.asctime()))
                #         newfile1.write('    ')
                #         newfile1.write(str(len(ele)))
                #         newfile1.write('个:   ')
                #         newfile1.write(str(ele))
                #         newfile1.write('\n')
                m = 0
                # grabbed, frame_lwpCV = camera.read() # 逐帧采集视频流
                frame_lwpCV = q.get()
                # if not grabbed:
                #     break

                gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)  # 转灰度图
                frame_data = np.array(gray_lwpCV)  # 每一帧循环存入数组
                for point_x_y in point_list:  # point_x_y 包含矩形区域的对角坐标，[0]为左上角xy，[1]为右下角xy
                    box_data = frame_data[point_x_y[0][1]:point_x_y[1][1]]  # 取矩形目标区域的竖边，即二维数组的行
                    box_data = box_data[:, point_x_y[0][0]:point_x_y[1][0]]  # 取矩形目标区域的宽边，即二维数组的列
                    pixel_sum = np.sum(box_data)  # 行求和q
                    data_result[m].append(pixel_sum)
                    data_result_time[m].append((time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),pixel_sum))
                    #     # print('new: %d,old: %d, new-old: %d' %(pixel_sum, pixel_sum_old, pixel_sum-pixel_sum_old))
                    #     # length = len(gray_lwpCV)
                    #     # length = 30
                    #     # x = range(length)
                    #




                    # 画目标区域
                    lwpCV_box = cv2.rectangle(frame_lwpCV, point_x_y[0], point_x_y[1], (0, 255, 0), 2)
                    # if pixel_sum > pixel_sum_old :
                    #     if pixel_sum - pixel_sum_old >= 5000:
                    cv2.putText(frame_lwpCV, str(pixel_sum), point_x_y[0], cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255))
                    # cv2.putText(frame_lwpCV, 'on', point_x_y[0],cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
                    # else:
                    #     cv2.putText(frame_lwpCV, str(pixel_sum), point_x_y[0],cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
                    #     cv2.putText(frame_lwpCV, 'off', point_x_y[0],cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
                    cv2.imshow('lwpCVWindow', frame_lwpCV)  # 显示采集到的视频流
                    # pixel_sum_old = pixel_sum
                    m = m + 1
                    # print(m)
                # for res in range(len(point_list)):
                #     print(data_result[res])
                # print(data_result)
                key = cv2.waitKey(2) & 0xFF
                if key == ord('q'):
                    # cv2.release()
                    cv2.destroyAllWindows()
                    print('退出线程2.')
                    # print(data_result)
                    flag1 = 2
                    flag = 1
                    break
                if key == ord('r'):
                    # cv2.release()
                    cv2.destroyAllWindows()
                    print('开始保存数据.')
                    # print(data_result)
                    flag = 2
                    # break
            date_analyse()
            # cv2.release()
            cv2.destroyAllWindows()
            break

def record_date():
    global old_start_time
    global data_result,data_result_time
    global count_frame
    global flag,flag1
    # count_frame1 = 0
    # while flag != 1:
    while True:

        key = cv2.waitKey(2) & 0xFF
        # count_frame1 += 1
        # if count_frame % 600 == 0:
        # if flag1 == 2 or count_frame % 60 == 0:
        if flag1 == 2:
            flag1 = 0
            # print('保存数据成功。。。')
            # record_date_result = data_result
            # print('3333',record_date_result)
            # print(record_date_result)
            # with open(r'source_result_report.txt', 'w') as newfile1:
            #     for eles in record_date_result:
            #         # print('时间为：第 %d 小时 %d 分钟 %d 秒,时长：%d秒'%(2*res[0]/3600,2*res[0]/60,2*res[0]%60,2*res[1]))
            #         # print(res)
            #         newfile1.write(str(old_start_time))
            #         newfile1.write('---')
            #         newfile1.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            #         newfile1.write('    ')
            #         newfile1.write(str(len(eles)))
            #         newfile1.write('个:   ')
            #         newfile1.write(str(eles))
            #         newfile1.write('\n')
            with open(r'source_result_time_report.txt', 'w') as newfile2:
                for eles2 in data_result_time:
                    # print('时间为：第 %d 小时 %d 分钟 %d 秒,时长：%d秒'%(2*res[0]/3600,2*res[0]/60,2*res[0]%60,2*res[1]))
                    # print(res)
                    newfile2.write(str(old_start_time))
                    newfile2.write('---')
                    newfile2.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                    newfile2.write('    ')
                    newfile2.write(str(len(eles2)))
                    newfile2.write('个:   ')
                    newfile2.write(str(eles2))
                    newfile2.write('\n')
            print('保存数据成功。。。')
        if flag == 1:
            print('退出线程3.')
            break


def seclct_ROI():
    # ------------------------------------------------------------------------------------
    # 选择视频的第一帧图像，并保存，作为后续框选识别区域的模板
    # ------------------------------------------------------------------------------------
    # vc = camera
    global point_list, start_time, flag
    global data_result
    c = 0
    cap01 = cv2.VideoCapture('%s'%paths)
    ret, frame = cap01.read()
    # q.put(frame)
    # while ret:
    # ret, frame = cap01.read()
        # if not (ret):
        #     # cap = cv2.VideoCapture('rtsp://admin:beijingsiasun@192.168.191.1/stream1')
        #     cap01 = cv2.VideoCapture('E:\pycharm\power_date_analyse\Test_video.mp4')
        #     ret, frame = cap01.read()
            # continue
        # q.put(frame)
    while c < 1:
        # rval, frame = vc.read()
        # cv2.imwrite('E:\pycharm\power_date_analyse\select_area.jpg', frame)
        # cv2.imwrite(r'E:\\selectarea.jpg', frame)
        cv2.imwrite('selectarea.jpg', frame)
        c = c + 1
        # print(c)
        k = cv2.waitKey(1)
        if k == ord('s'):  # wait for 's' key to save and exit
            print('you input "s",the picture with select area will be saved')
            cv2.destroyAllWindows()
            break
        else:
            cv2.destroyAllWindows()
            # ------------------------------------------------------------------------------------
            # 划定识别区域，使用之前保存的第一帧图像
            # ------------------------------------------------------------------------------------
    k = 0
    num = 0

    # img = cv2.imread("E:\pycharm\power_date_analyse\select_area.jpg")
    # img = cv2.imread(r'E:\\selectarea.jpg')
    img = cv2.imread('selectarea.jpg')
    while (k != ord('q')):
        num += 1
        # img = imutils.resize(img, width=500)
        print('绘制蓝色矩形框，并按下回车确认，矩形框变为红色;')

        roi = cv2.selectROI(windowName="roi", img=img, showCrosshair=True, fromCenter=False)
        x, y, w, h = roi

        cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2)
        point_list.append(((x, y), (x + w, y + h)))
        # print(num,point_list[num-1])
        print('第 %d 次的坐标是: ' % num, point_list[num - 1])
        cv2.putText(img, str(num), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        cv2.imshow("roi", img)
        print('保存请按 s ;', '继续绘制下一个矩形框，请按回车')

        k = cv2.waitKey(0)  # 检测到按键，最后退出
        if k == ord('s'):  # wait for 's' key to save and exit
            # print(k)
            # print(point_list)
            # cv2.imwrite('E:\pycharm\power_date_analyse\modole.png', img)
            cv2.imwrite('modole.png', img)
            print('you input "s",the picture with select area will be saved')
            print(point_list)
            # print((x,y),(x+w,y+h))
            cv2.destroyAllWindows()
            break
        else:
            cv2.destroyAllWindows()
    # print(point_list[0][0])
    print('区域采集完毕，开始监测。')

# ---------------------------------------
# 结果分析
# ---------------------------------------
#
# ---------------------------------------
# 检测关到开
# ---------------------------------------

def date_analyse():
    global point_list, start_time, flag
    global paths, on_yz_1, on_yz_2, on_time_yz_1
    global data_result
    print(on_yz_1, on_yz_2, on_time_yz_1)
    on_num = 0
    on_num_list = []
    for count in range(len(point_list)):
        on_num_list.append(list())
    # print(on_num_list)
    # print(data_result)

    for rectangle_num in range(len(data_result)):
        for mm in range(len(data_result[rectangle_num]) - 2):
            on_flag = 0  # 记录开的第一帧的位置
            on_time = 0  # 记录开的时间
            if int(data_result[rectangle_num][mm + 1]) - int(data_result[rectangle_num][mm]) > int(on_yz_1) and int(
                    data_result[rectangle_num][mm + 2]) - int(data_result[rectangle_num][mm + 1]) < int(on_yz_2):
                # print(int(data_result[rectangle_num][mm + 1]), int(data_result[rectangle_num][mm]))
                ll = []
                on_num += 1
                on_flag = mm + 1
                for on_mm in range(on_flag + 1, len(data_result[rectangle_num]) - 1):
                    if data_result[rectangle_num][on_mm] > data_result[rectangle_num][on_flag] or abs(
                                    int(data_result[rectangle_num][on_mm]) - int(
                                    data_result[rectangle_num][on_flag])) < int(on_time_yz_1) or abs(
                                    int(data_result[rectangle_num][on_mm + 1]) - int(
                                    data_result[rectangle_num][on_flag])) < int(on_time_yz_1):
                        on_time += 1
                    # elif abs(date_result[on_mm+1] - date_result[on_flag]) < 2000:
                    #     on_time += 1
                    else:
                        break
                ll.append(2 * on_flag)
                ll.append(2 * on_time)
                on_num_list[rectangle_num].append(ll)

    # for ele in data_result:
    #     print(ele)


    # print(on_num)
    # with open(r'E:\\pycharm\\power_date_analyse\\result_report.txt', 'w') as newfile:
    # with open(r'source_result_report.txt', 'w') as newfile1:
    #     for ele in data_result:
    #         # print('时间为：第 %d 小时 %d 分钟 %d 秒,时长：%d秒'%(2*res[0]/3600,2*res[0]/60,2*res[0]%60,2*res[1]))
    #         # print(res)
    #         newfile1.write(str(len(ele)))
    #         newfile1.write('个: ')
    #         newfile1.write(str(ele))
    #         newfile1.write('\n')
    # with open(r'E:\\pycharm\\power_date_analyse\\result_report.txt', 'w') as newfile:
    with open(r'result_report.txt', 'w') as newfile2:
        for res in on_num_list:
            newfile2.write(str(len(res)))
            newfile2.write('次: ')
            newfile2.write(str(res))
            newfile2.write('\n')

    end_time = time.time()
    print("Cost time", end_time - start_time)



    # cv2.imshow("frame1", frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break


if __name__ == '__main__':
    init_basic()
    p1 = threading.Thread(target=receive)
    p2 = threading.Thread(target=Display)
    p3 = threading.Thread(target=record_date)

    seclct_ROI()
    print('0001')
    p1.start()
    print('0002')
    p2.start()
    print('0003')
    p3.start()
    print('0004')
    # if flag == 1:
    #     date_analyse()
    #     print(data_result)
    print('0005')





# ----------------------------
# 结果分析
# ----------------------------

# ----------------------------
# 检测关到开
# ----------------------------
#
# on_num = 0
# on_num_list = []
# for count in range(len(point_list)):
#     on_num_list.append(list())
# # print(on_num_list)
#
# for rectangle_num in range(len(data_result)):
#     for mm in range(len(data_result[rectangle_num])-2):
#         on_flag = 0  # 记录开的第一帧的位置
#         on_time = 0  # 记录开的时间
#         if int(data_result[rectangle_num][mm+1])-int(data_result[rectangle_num][mm]) > int(on_yz_1) and int(data_result[rectangle_num][mm+2])-int(data_result[rectangle_num][mm+1]) < int(on_yz_2):
#             print(int(data_result[rectangle_num][mm+1]),int(data_result[rectangle_num][mm]))
#             ll = []
#             on_num += 1
#             on_flag = mm+1
#             for on_mm in range(on_flag+1,len(data_result[rectangle_num])-1):
#                 if data_result[rectangle_num][on_mm] > data_result[rectangle_num][on_flag] or abs(int(data_result[rectangle_num][on_mm]) - int(data_result[rectangle_num][on_flag])) < int(on_time_yz_1) or abs(int(data_result[rectangle_num][on_mm+1]) - int(data_result[rectangle_num][on_flag])) < int(on_time_yz_1):
#                     on_time += 1
#                 # elif abs(date_result[on_mm+1] - date_result[on_flag]) < 2000:
#                 #     on_time += 1
#                 else:
#                     break
#             ll.append(2*on_flag)
#             ll.append(2*on_time)
#             on_num_list[rectangle_num].append(ll)
#
# # for ele in data_result:
# #     print(ele)
#
# # print(on_num)
# # with open(r'E:\\pycharm\\power_date_analyse\\result_report.txt', 'w') as newfile:
# with open(r'source_result_report.txt', 'w') as newfile1:
#     for ele in data_result:
#         # print('时间为：第 %d 小时 %d 分钟 %d 秒,时长：%d秒'%(2*res[0]/3600,2*res[0]/60,2*res[0]%60,2*res[1]))
#         # print(res)
#         newfile1.write(str(len(ele)))
#         newfile1.write('个: ')
#         newfile1.write(str(ele))
#         newfile1.write('\n')
# # with open(r'E:\\pycharm\\power_date_analyse\\result_report.txt', 'w') as newfile:
# with open(r'result_report.txt', 'w') as newfile2:
#     for res in on_num_list:
#         newfile2.write(str(len(res)))
#         newfile2.write('次: ')
#         newfile2.write(str(res))
#         newfile2.write('\n')
#
# end_time = time.time()
# print("Cost time", end_time - start_time)
