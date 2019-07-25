'''
用于对当前文件夹中的mp4格式的视频，指定时间段和截取次数获取截图
'''
import os
import re
import cv2

# 根据输入的开始和结束根据时间间隔截取图片，参数分别为视频路径，图片存储路径、开始时间、结束时间、截图的次数
def cut_img(video_name, start, end, cut_time):
    vidcap = cv2.VideoCapture(video_name)
    now = start*1000

    one = re.findall(r'(.*?).mp4',video_name)[0]
    wrong = []

    for i in range(cut_time):
        vidcap.set(cv2.CAP_PROP_POS_MSEC, now) #第二个参数为以毫秒为单位
        success, image = vidcap.read()
        try:
            if success:
                cv2.imencode('.png', image)[1].tofile("{0}.png".format(one+str(i)))
                #cv2.imwrite("{0}/{1}.png".format(img_dir,i), image)，识别不出中文路径的图片
                print(one+str(i))
            now = now+(end-start+1)/cut_time*1000
        except:
            wrong.append(one)
    return wrong

if __name__ == '__main__':
    files = os.listdir('./') #当前文件夹中的文件
    for file in files:
        if file[-1]=='4':
            cut_img(file, 18, 19, 10)