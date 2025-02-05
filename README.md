# WT-RWR-Based-on-Buzzer

整活的作品，基于MicroPython，使用ESP32S3，额外使用的器材有无源蜂鸣器与TFT显示屏(ILI9341)，引脚可以依照自己的需要去改

---

## 实际效果：

<iframe src="https://player.bilibili.com/player.html?isOutside=true&aid=113947428521291&bvid=BV1gmPBeFEem&cid=28219015764&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

---

理论上只要ili9341.py兼容的所有MicroPython开发板都能用，项目迁移应该很简单，就看各位的造化了（

## 简单阐述一下文件结构

```
1.raw		-RWR的告警文本框(敌跟踪)
1S.raw		-RWR的雷达界面(无目标)
2.raw		-RWR的告警文本框(敌导弹)
2S.raw		-RWR的雷达界面(有目标)
3.raw		-RWR的告警文本框(纯黑，用于清空敌导弹标识以达到一种闪烁的效果)
boot.py		-开机后默认执行的第一个程序，用于引导main.py
ili9341.py	-显示器的驱动程序
main.py		-主程序
music.py	-无源蜂鸣器驱动库
```

*(*注意：以上所有raw格式的照片都是为了方便显示器显示被转换为rgb565了的)*

在敌导弹的时候，RWR雷达界面不会闪烁是因为SPI读写太慢，因此直接刷新整个屏幕帧率会很低，就会有一种很奇怪的效果，所以干脆为了视觉效果就不搞成闪烁的

---

## 关于部分代码注解

```python
# 用户可自定义的
rwr(4)
rwrG(5)
rwrD(15)
rwr(3)
rwrG(3)
rwrD(10)
_thread.start_new_thread(t0, ())
```

rwr()函数是进行几次rwr平时雷达扫描的效果

rwrG()就是敌跟踪

rwrD()是敌导弹

三个顺序可以用户自行排列，括号里的参数就是蜂鸣器响几次

#### 另外还有一点，如果程序出现卡死，在保证接线没有问题的情况下，可能是以下原因

`for i in range(0, int(times*0.4), 1):`

times后方的参数有问题，因为rwr敌导弹的时候，蜂鸣器的发声频率和雷达闪烁频率不一样，所以用了多线程的异步处理，times后方的*0.4就是参数修正，以防止蜂鸣器响完了结果雷达还没响完，在下次调display.draw_image()函数时SPI被占用，从而造成卡死

#### 剩下的就是关于引脚定义的代码

```python
midi = music.MIDI(2)	# 蜂鸣器的正极引脚
pin4 = machine.Pin(4, machine.Pin.OUT)	# TFT显示屏的LED引脚

spi = SPI(1, baudrate=60000000, sck=Pin(6), mosi=Pin(7))	# 关于SPI的引脚定义
display = Display(spi, dc=Pin(15), cs=Pin(17), rst=Pin(16))	# 关于TFT显示屏的其他引脚定义
```
