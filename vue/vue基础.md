1. `v-bind`：attribute绑定，直接省略成”:"
2. `v-on`：事件监听，直接省略成”@“
3. `v-model`：表单绑定，将被绑定的值与
4. `v-if、v-else、v-else-if`：条件渲染，当**v-if**绑定的值为真时，所在标签被渲染
5. `v-for`：列表渲染，(下方“:key”采用v-bind省略写法)

```vue
<ul>
  <li v-for="todo in todos" :key="todo.id">
    {{ todo.text }}
  </li>
</ul>
```

6. `computed: {}`：计算属性，可以使用 `computed` 选项声明一个响应式的属性，它的值由==其他属性计算==而来.

   假如我们已经有了一个能够切换 `hideCompleted` 状态的按钮，

```vue
<script>
export default {
  // ...
  computed: {
    filteredTodos() {
      	// 根据 `this.hideCompleted` 返回过滤后的 todo 项目
		return this.hideCompleted
        ? this.todos.filter((t) => !t.done)
        : this.todos
    }
  }
}
</script>
```

7. **生命周期钩子**，可以用来在组件完成初始渲染并创建 DOM 节点后运行代码。

   - `mounted() {}`：挂载，钩子可以用来在组件完成初始渲染并创建 DOM 节点后运行代码。使用 `ref` 这个特殊的 attribute 实现**模板引用**，挂载后可通过 `this.$refs.元素` 访问。

     > 在模板渲染成`html`后调用，通常是初始化页面完成后，再对`html`的`dom`节点进行一些操作。

   - `created() {}`:

     >  在模板渲染成`html`前调用，即通常初始化某些属性值，然后再渲染成视图。

```vue
<script>
export default {
  mounted() {
    this.$refs.p.textContent = 'i love you'
  }
}
</script>

<template>
  <p ref="p">hello</p>
</template>
```

8. `watch: {}`：侦听器，使用 `watch` 选项来侦听 `count` 属性的变化。当 `count` 改变时，侦听回调将被调用，并且==接收新值作为参数==。

```vue
<script>
export default {
  // ...
  watch: {
    count(newCount) {
      
    }
  }
}
</script>
```

9. `components: {}`：组件，父组件可以在模板中渲染另一个组件作为子组件

```vue
<script>
import ChildComp from './ChildComp.vue'

export default {
  components: {
    ChildComp
  }
}
</scripts>
<template>
  <!-- 渲染子组件 -->
  <ChildComp />
</template>
```

10. `props`：子组件可以通过 `props` 从父组件接受动态数据。

    ​	

```vue
// 在子组件中
<script>
export default {
  props: {
    msg: String
  }
}
</script>	
```

​		父组件可以像声明 HTML attributes 一样传递 `props`。若要传递动态值，也可以使用 `v-bind` 语法：

```vue
// 在父组件中
<template>
  <ChildComp :msg='greeting'/>
</template>
```

11. `Emits`：事件，子组件可以向父组件触发事件。

​		`this.$emit()` 的第一个参数是事件的名称。其他所有参数都将传递给事件监听器。

```vue
// 在子组件中
<script>
export default {
  // 声明触发的事件
  emits: ['response'],
  created() {
    // 带参数触发
    this.$emit('response', 'hello from child')
  }
}
</script>
```

​		父组件可以使用 `v-on` 监听子组件触发的事件——这里的处理函数接收了子组件触发事件时的**额外参数**并将它赋值给了本地状态：

```vue
// 在父组件中
<template>
  <ChildComp @response="(msg) => childMsg = msg" />
</template>
```

12. **插槽**：除了通过 `props` 传递数据外，父组件还可以通过**插槽** (slots) 将模板片段传递给子组件：

```vue
<ChildComp>
  This is some slot content!
</ChildComp>
```

​		在子组件中，可以使用 `<slot>` 元素作为插槽出口 (slot outlet) 渲染父组件中的插槽内容 (slot content)：

```vue
<!-- 在子组件的模板中 -->
<slot/>
```

​		`<slot>` 插口中的内容将被当作“默认”内容，它会在父组件没有传递任何插槽内容时显示：

```vue
<slot>Fallback content</slot>
```
