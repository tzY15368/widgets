import cv2
import time
import datetime
import win32gui, win32ui, win32con, win32api
def getposBgr(event, x, y, flags, param):
    if event==cv2.EVENT_LBUTTONDOWN:
        print('(y,x)=',y,x)
        rgb_arr = [img[y,x][2],img[y,x][1],img[y,x][0]]
        #print("Bgr is", img[y, x],type(img[y,x]),img[y,x][1])
        print('rgb array:\n','R:',rgb_arr[0],'G:',rgb_arr[1],'B:',rgb_arr[2])
        rgb_str = str(str(rgb_arr[0])+','+str(rgb_arr[1])+','+str(rgb_arr[2]))
        return RGB_to_Hex(rgb_str)


def RGB_to_Hex(tmp):
    rgb = tmp.split(',')  # 将RGB格式划分开来
    strs = '#'
    for i in rgb:
        num = int(i)  # 将str转int
        # 将R、G、B分别转化为16进制拼接转换并大写
        strs += str(hex(num))[-2:].replace('x', '0').upper()
    print(strs)
    print('----------------------------------------------------')


def window_capture(filename):
    hwnd = 0 # 窗口的编号，0号表示当前活跃窗口
  # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
  # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
  # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
  # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
  # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
  # print w,h　　　#图片大小
  # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
  # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
  # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)

  
path = input('pull in image as path or s for screenshot in 3 seconds\t路径不得包含中文\n')
if path=='s':
    time.sleep(1)
    now = int(time.time()) 
    #转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S" 
    timeStruct = time.localtime(now) 
    strTime = time.strftime("%Y-%m-%d-%H-%M-%S", timeStruct) 
    name = strTime
    path = 'D:\\1utils\\screenshots\\'+name+'.jpg'
    #path = 'D:\\1utils\\screenshots\\123123.jpg'
    print(path)
    time.sleep(1)
    try:
        window_capture(path)
    except Exception as e:
        print('error:')
        print(e)
        input('enter to quit')
        exit(0)
    
img = cv2.imread(path,cv2.IMREAD_UNCHANGED)
if img is None:
    input('wrong path,enter to quit:可能有中文路径？')
    exit('wrong path')
height, width = img.shape[:2]
new_size = input('(height,width) ='+str(height)+','+str(width)+'\nresize?\nresized height or any other key\n')
if new_size != '':
    try:
        new_size = int(new_size)
        size = (int(width*(new_size/height)),new_size)
        img = cv2.resize(img,size,interpolation=cv2.INTER_AREA)
    except Exception as e:
        print(e)
        input('enter to quit')
        exit('wrong input')




cv2.imshow('image',img)
cv2.setMouseCallback('image',getposBgr)
cv2.waitKey(0)
cv2.destroyAllWindows()
