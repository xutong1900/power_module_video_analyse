# -*- coding:utf-8- -*-
import matplotlib.pyplot as plt

#-------------------------------------------
#从文件中读取数据
#-------------------------------------------

def date_receive(file_paths):
    record_list = []
    line_count = 0
    date_position_e = 0
    start_position = 0
    paths = file_paths
    with open(str(paths),'r') as file_c:
        for line_c in file_c:
            record_list.append(list())
            line_number = len(record_list)

    with open(str(paths),'r') as file_1:
        for line in file_1: #读取一行数据，每一行数据记录着一个监测点在整个过程中的所有数据，需要从中提取出对应的时间和灰度和

            if start_position < date_position_e:
                start_position = date_position_e + 3
                print('start_position', start_position)
            else:
                start_position = line.index('[') + 1
                print('start_position [ ', start_position)
            # while line[date_position_e + 1] != ']':
            while True:

                print(date_position_e,line[date_position_e + 1],start_position)
                line_s = line[start_position:]
                print('start_position',start_position)
                print('共 %d 个，正在处理第 %d 个。'%(line_number,line_count+1))
                # print(line_s)
                for eles_s in line_s:

                    if eles_s == '(':
                        time_position_s = line_s.index(eles_s)+2
                        # print(time_position_s)
                        for eles_m in line_s:
                            if eles_m == ',':
                                time_position_e = line_s.index(eles_m)-1
                                date_position_s = time_position_e + 3
                                for eles_e in line_s:
                                    if eles_e == ')':
                                        date_position_e = line_s.index(eles_e)
                                        start_position += date_position_e + 3
                                        print('ssss',start_position)

                                        break
                                break
                    break

                record_list[line_count].append((line_s[time_position_s:time_position_e],line_s[date_position_s:date_position_e]))

                print('date_position_e',date_position_e)
                if start_position >= len(line):
                    print('break',str(line[date_position_e+1]))
                    break
            line_count += 1

    for colum in range(len(record_list)):
        date_plot_list = []
        date_plot_num = []
        date_plot_time = []
        plt.figure(figsize=(20,10))
        for date_plot in range(len(record_list[colum])):
        # for date_plot in range(200):
            date_plot_list.append(int(record_list[colum][date_plot][1])/100)

            date_plot_num.append(date_plot)
            if date_plot % 100 == 0:
                plt.annotate(record_list[colum][date_plot][0], xy=(date_plot, int(record_list[colum][date_plot][1])/100),xytext=(date_plot,int(record_list[colum][date_plot][1])/100+20),fontsize=8,arrowprops=dict(facecolor='black',shrink=0.01))

        print(len(date_plot_list),len(date_plot_num))

        plt.plot(date_plot_num, date_plot_list)

        plt.savefig(str(colum)+'.png')
        # plt.close()
    plt.show()

if __name__ == '__main__':
    date_receive('source_result_time_report.txt')
