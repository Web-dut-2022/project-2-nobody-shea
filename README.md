[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7617012&assignment_repo_type=AssignmentRepo)
# project2-2021

已基本实现上机要求，由于时间关系，Categories部分实现得较为粗糙，仍存在一定问题，Django Admin Interface部分未做具体实现。

### 一些说明：

* 关于创建新Listing时选择图像的URL，最开始的想法是用户上传本地图像文件，在输入框内自动显示绝对路径，但是由于技术原因未能实现，后改为显示文件名，然后在下方生成图像预览。
* 开始把images文件夹放在commerce\auctions\static\auctions下（即与styles.css文件同级）时，图片（静态资源）一直加载不了（试了很多办法都无济于事），后来把images文件夹改到static下（与auctions文件夹同级），又改了相关路径设置，才加载、显示成功。（就为这一点折腾了好久，难顶。。。）
* 上传图片的文件名不能带空格。如果带空格的话，实际存储在images里的文件会自动将空格替换成_（下划线），但是因为上传时的文件名中仍是空格，导致图片路径里也是空格而非下划线，最终无法定位到此图片资源。
  * 也不能带中文标点什么的，会被自动去掉。。。（由于时间关系，这部分未做改进）

*具体细节见代码。*

部分效果截图如下：

![](/部分截图/001.png)

![](/部分截图/002.png)

![](/部分截图/003.png)

![](/部分截图/005.png)

![](/部分截图/006.png)

![](/部分截图/007.png)
