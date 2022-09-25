# 如何使用Typora文本编辑器(详细教程)
## 1、标题

一级标题：#+空格+标题+回车

二级标题：##+空格+标题+回车

三级标题：###+空格+标题+回车

四级标题：####+空格+标题+回车

五级标题：#####+空格+标题+回车

六级标题：######+空格+标题+回车

目前只支持到六级标题！

## 2、字体
加粗： 在字体两边分别+两个*号。**Hello,World！**

*斜体*：在字体两边分别只+一个*号。 *Hello,World！*

***粗体+斜体***： 在字体两边分别+三个*号。 ***Hello,World！***

~~删除线~~： 在字体两边分别+两个 ~（波浪）线。 ~~Hello,World！~~

==高亮==：在字体两边分别+两个=号。 ==Hello，world！==

## 3、引用
在起始位置添加一个大于符号（>）+空格，表示引用

(>>+空格)二级

>  引用别人文章字句时可以使用

> > 第二级

## 4、分割线

可以用三个杠（—）+空格

___

也可以用三个星号（*）+空格（这个分割线占全屏）

***

## 5、图片
样式（英文状态下的感叹号 加 中括号 加 小括号（ !+[ ]+()），加号去掉，中括号里面放图片的名字，小括号放图片的地址（图片可以是本地的图片也可以是网上的图片））。

（1）本地图片：

（2）网上图片(西部开源-秦疆老师博客中的图片)：

![网图](https://imgconvert.csdnimg.cn/aHR0cHM6Ly9pbWcyMDIwLmNuYmxvZ3MuY29tL290aGVyLzI2ODIyNC8yMDIwMDgvMjY4MjI0LTIwMjAwODI0MTA1MDM4MDcyLTE5OTg0NzA0MzQuanBn?x-oss-process=image/format,png)

## 6、超链接

### 6.1 文本链接

样式：（英文状态下的中括号 + 小括号（[ ]+( )）,中括号放超链接的名字，小括号放超链接的地址）

[如何使用Typora文本编辑器(详细教程)](https://blog.csdn.net/weixin_47848436/article/details/108196525?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522161533873616780264024819%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=161533873616780264024819&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-108196525.pc_search_result_before_js&utm_term=%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8Typora)

### 6.2 地址链接

样式：<>

<https://blog.csdn.net/qq_46138160/article/details/111028442?ops_request_misc=&request_id=&biz_id=102&utm_term=%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8Typora&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-6-111028442.pc_search_result_before_js>

## 7、列表

### 7.1 有序列表：

样式（1+.号+空格）

1. A

2. B

3. C

### 7.2 无序列表：

样式（- 号+ 空格）

- A
- B
- C

### 7.3 任务列表：

样式（- [ ] 任务名）

- [ ] 吃饭

## 8、表格

1.可以直接右键插入表格

2.手打样式：

|名字|性别|生日|

|:--|:--:|--:|

|张三|男|1999.1.1|（然后用鼠标点页面最底部的</>启用源代码符号，把手打内容之间的空行删掉，然后回到内容页面并==回车==，表格就出来了）

| 名字 | 性别 | 生日     |
| ---- | ---- | -------- |
| 张三 | 男   | 1999.1.1 |

## 9、代码
样式：三个英文状态下的 `或者~，后面+你要写的代码类型（java、JavaScript等）。

```java
public
```

行内代码`printf()`

``` 
`printf()`
```

## 10、标注

样式：

``` 
概念A[^1]
[^1]:解释语
```

概念A[^1]

## 11、 下标

```text
H~2~O
```

H~2~O

## 12、 上标

```text
x^2^
```

X^2^

## 13、数学公式

“$$”+回车。
$$
x=y
$$




[^1]: 解释语