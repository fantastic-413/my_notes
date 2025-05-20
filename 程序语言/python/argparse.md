### argparse 是 python 用于解析命令行参数和选项的标准模块

相关链接：[argparse - 命令行选项与参数解析](http://blog.xiayf.cn/2013/03/30/argparse/)

我们常常可以把 argparse 的使用简化成下面四个步骤:

1. 首先导入该模块。

   ```python
   import argparse
   ```

2. 然后创建一个解析对象。

   ```python
   # prog - 程序的名称(默认: sys.argv[0]，prog猜测是programma的缩写)
   # usage - 描述程序用途的字符串(默认值：从添加到解析器的参数生成)
   # description - 在参数帮助文档之后显示的文本 (默认值:无)
   # prefix_chars - 用于增加可以用于选项命名的字符
   parser = argparse.ArgumentParser()
   ```

   需要理解的是虽然`prefix_chars`包含允许用于开关的字符，但单个参数定义只能使用一种给定的开关语法。这让你可以对使用不同前缀的选项是否是别名（比如独立于平台的命令行语法的情况）或替代选择（例如，使用`+`表明打开一个开发，`-`则为关闭一个开关）进行显式地控制。

3. 然后向该对象中添加你要关注的命令行参数和选项，每一个 add_argument 方法对应一个你要关注的参数或选项。

   ```python
   # name or flags - 一个命名或者一个选项字符串的列表
   # action - 表示该选项要执行的操作
   # default - 当参数未在命令行中出现时使用的值
   # dest - 用来指定参数的位置
   # type - 为参数类型，例如int
   # choices - 用来选择输入参数的范围。例如choice = [1, 5, 10], 表示输入参数只能为1,5 或10
   # help - 用来描述这个选项的作用
   parser.add_argument()
   ```

   `action`内置6种动作可以在解析到一个参数时进行触发：

   - `store` 保存参数值，可能会先将参数值转换成另一个数据类型。若没有显式指定动作，则**默认**为该动作。
   - `store_const` 保存一个被定义为参数规格一部分的值（==搭配`const`参数指定==），而不是一个来自参数解析而来的值。这通常用于实现非布尔值的命令行标记。
   - `store_ture`/`store_false` 保存相应的布尔值。这两个动作被用于实现布尔开关。
   - `append` 将值保存到一个列表中。若参数重复出现，则保存多个值。
   - `append_const` 将一个定义在参数规格中的值（==搭配`const`参数指定==）保存到一个列表中。
   - `version` 打印关于程序的版本信息，然后退出

4. 最后调用 parse_args() 方法进行解析，解析成功之后即可使用。

   ```python
   parser.parse_args()
   ```

   **parse_args()** 的返回值是一个**命名空间**，包含传递给命令的参数。该对象将参数保存其属性，因此如果你的参数 `dest` 是 `"myoption"`，那么你就可以`args.myoption` 来访问该值。