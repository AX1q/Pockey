# 认识linux

## 1.认识Linux

> **Linux 提供了一个驱动力，让你去接触和掌握计算机的核心秘密,同时 Linux 是一个安全、稳定、自由的系统.**

#### Linux桌面程序：
   - Xfce 终端：Linux 中控制电脑的窗口，在其中可以用命令来控制一切
   - Firefox 浏览器：浏览器，可以用在需要前端界面的课程里。
   - GVim：一款好用的 Vim 编辑器
   - gedit、Sublime：同样是代码编辑器

(*Linux的命令很多，**不用硬记！***)

## 2. Linux目录操作：
Linux 的目录类似于 Windows 系统中的文件夹。我们看一下刚刚打开的 终端 界面，它的第一行开头是：

~~~bash
shiyanlou:~/ $
~~~

shiyanlou 代表你当前的用户名，如果你的用户名叫 tony，就会显示 tony:~/ $。后面的美元符号是「命令提示符」，提示你：请在它后面输入命令。

-  **查看目录中的内容**：**`ls`**
在 $ 后输入 ls ，可查看当前目录下的文件和目录。
- **进入目录**: **`cd`**
使用 cd 命令可进入其他目录
*(键盘的上下键,可快速选择前面输过的命令)*
   **- 输入 `cd ..` 可以回到上一级目录，类似 Windows 的「向上」**
   **- 输入 `cd -` 表示回到上一次所在的目录，类似 Windows 的「后退」**
   **- 输入 `cd ~` 表示回到当前用户的主目录，类似   Windows 的「回到桌面」**
   **- 输入 `cd /` 表示进入根目录，它是一切目录的父目录**
- **查看目录结构**: **`tree`**
使用 tree 命令，可以列出一个文件夹下的所有子文件夹和文件（以树形结构来进行列出）
- **获取当前目录的绝对路径**: **`pwd`**
- **创建目录**: **`mkdir`**
mkdir mycode 的意思就是新建一个名为 mycode 的目录.
*(还可以在 mkdir 后加入 -p 参数，一次性创建多级目录.)*

## 3.Linux文件操作
-  **新建空白文件**：**`touch`**
使用 touch 命令可以新建文件
（该命令不会覆盖已有同名文件）
- **复制文件到指定目录下**: **`cp`**

例如：

~~~bash
cp hello one/two/
tree one
~~~

  如果要复制目录，需要在 cp 后加上 -r ，然后接上目录名，目标目录名
- **删除文件**：**`rm`**
删除目录要加上 -r 选项

- **移动文件 / 目录与重命名**：**`mv`**

- **将文件中的内容打印到屏幕上**： **`cat`**
使用 cat -n 可以带行号地打印文件内容

- **帮助命令**：**`man`**
例如输入 `man cat` ，可以获取 `cat` 命令的详细的帮助文件。进入到 man 的页面后，按 q 可以退出 man

- **编辑工具**：**`sublime，gedit`**

---

> #### 其余详细信息 可点击[此处](https://blog.csdn.net/m0_46422300/article/details/104645072)

# Git的认识

![alt text](<Screenshot 2024-04-19 192758.png>)

#### 1. `git config`: 对于用户的设置

```bash
git config --global user.name '名字'
git config --global user.email '邮箱'
```

#### 2. `git init`: git初始化,会进入主分支

#### 3. `git status`: 表查看当前分支

#### 4. `git add`: 添加内容

#### 5. `git commit`: 总概况提交修改内容

```bash
git commit -m '内容信息'
```

#### 6. `git log`: 查看前面版本

#### 7. `touch .gitignore`: 隐匿文件 忽略文件

#### 8. `git branch`: 查看分支

```bash
git branch '分支名'    #创建新分支
git branch -d '分支名' #删除分支             -D #非常确定删除
git branch -m '分支名' #把当前分支名改成...  -M #强制性
```

#### 9. `git checkout（switch）`: 切换到分支

```bash
git checkout '分支名'     #切换到分支上
git checkout -b '分支名'  #创建并跳到该分支上
```

#### 10. `git merge`: 把别的分支合并到当前分支上

#### 11. `git remote`: 查看本地所记录的远程仓库地址
