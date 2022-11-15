1. 声明式渲染：

   ```vue
   <script>
   export default {
     data() {
       return {
         message: 'Hello World!',
         counter: {
           count: 0
         }
       }
     }
   }
   </script>
   
   <template>
     <h1>{{ message }}</h1>
     <p>Count is: {{ counter.count }}</p>
   </template>
   ```

2. `v-bind`：为 attribute 绑定一个动态值，可省略成 `:`

   ```vue
   <script>
   export default {
     data() {
       return {
         titleClass: 'title'
       }
     }
   }
   </script>
   
   <template>
     <h1 :class="titleClass">Make me red</h1>
   </template>
   
   <style>
   .title {
     color: red;
   }
   </style>
   ```

3. `v-on`：监听 DOM 事件，可省略成 `@`

   ```vue
   <script>
   export default {
     data() {
       return {
         count: 0
       }
     },
     methods: {
       increment() {
         this.count++
       }
     }
   }
   </script>
   
   <template>
     <button @click="increment">count is: {{ count }}</button>
   </template>
   ```

4. `v-model`：表单绑定，将被绑定的值与输入框中 `<input>` 的值自动同步。不仅支持文本输入框，也支持诸如多选框、单选框、下拉框之类的输入类型。

   ```vue
   <script>
   export default {
     data() {
       return {
         text: ''
       }
     }
   }
   </script>
   
   <template>
     <input v-model="text" placeholder="Type here">
     <p>{{ text }}</p>
   </template>
   ```

5. `v-if、v-else、v-else-if`：条件渲染，当**v-if**绑定的值为真时，所在标签被渲染

   ```vue
   <script>
   export default {
     data() {
       return {
         awesome: true
       }
     },
     methods: {
       toggle() {
         this.awesome = !this.awesome
       }
     }
   }
   </script>
   
   <template>
     <button @click="toggle">toggle</button>
     <h1 v-if="awesome">Vue is awesome!</h1>
     <h1 v-else>Oh no 😢</h1>
   </template>
   ```

6. `v-for`：渲染一个基于源数组的列表，(下方“:key”采用v-bind省略写法)

   ```vue
   <script>
   // 给每个 todo 对象一个唯一的 id
   let id = 0
   
   export default {
     data() {
       return {
         newTodo: '',
         todos: [
           { id: id++, text: 'Learn HTML' },
           { id: id++, text: 'Learn JavaScript' },
           { id: id++, text: 'Learn Vue' }
         ]
       }
     },
     methods: {
       addTodo() {
         this.todos.push({ id: id++, text: this.newTodo })
         this.newTodo = ''
       },
       removeTodo(todo) {
         this.todos = this.todos.filter((t) => t !== todo)
       }
     }
   }
   </script>
   
   <template>
     <form @submit.prevent="addTodo">
       <input v-model="newTodo">
       <button>Add Todo</button>    
     </form>
     <ul>
       <li v-for="todo in todos" :key="todo.id">
         {{ todo.text }}
         <button @click="removeTodo(todo)">X</button>
       </li>
     </ul>
   </template>
   ```

7. `computed: {}`：计算属性，可以使用 `computed` 选项声明一个响应式的==属性==，它的值由其他属性计算而来.

   ```vue
   <script>
   let id = 0
   
   export default {
     data() {
       return {
         newTodo: '',
         hideCompleted: false,
         todos: [
           { id: id++, text: 'Learn HTML', done: true },
           { id: id++, text: 'Learn JavaScript', done: true },
           { id: id++, text: 'Learn Vue', done: false }
         ]
       }
     },
     computed: {
       filteredTodos() {
         return this.hideCompleted
           ? this.todos.filter((t) => !t.done)
           : this.todos
       }
     },
     methods: {
       addTodo() {
         this.todos.push({ id: id++, text: this.newTodo, done: false })
         this.newTodo = ''
       },
       removeTodo(todo) {
         this.todos = this.todos.filter((t) => t !== todo)
       }
     }
   }
   </script>
   
   <template>
     <form @submit.prevent="addTodo">
       <input v-model="newTodo">
       <button>Add Todo</button>
     </form>
     <ul>
       <li v-for="todo in filteredTodos" :key="todo.id">
         <input type="checkbox" v-model="todo.done">
         <span :class="{ done: todo.done }">{{ todo.text }}</span>
         <button @click="removeTodo(todo)">X</button>
       </li>
     </ul>
     <button @click="hideCompleted = !hideCompleted">
       {{ hideCompleted ? 'Show all' : 'Hide completed' }}
     </button>
   </template>
   
   <style>
   .done {
     text-decoration: line-through;
   }
   </style>
   ```

8. **生命周期钩子**，允许我们注册一个在组件的**特定生命周期**调用的回调函数.

   - `mounted() {}`：挂载钩子，在组件完成初始渲染并创建 DOM 节点后执行。

     - 在组件挂载后，可以使用 `ref` 这个特殊的 attribute 实现**模板引用**——操作模板中一个 DOM 元素，通过 `this.$refs.元素` 访问。


     > 在模板渲染成`html`后调用，通常是初始化页面完成后，再对`html`的`dom`节点进行一些操作。


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

   - `created() {}`:

     > 在模板渲染成`html`前调用，即通常初始化某些属性值，然后再渲染成视图。

9. `watch: {}`：侦听器，使用 `watch` 选项来侦听 `count` 属性的变化。当 `count` 改变时，侦听回调将被调用，并且==接收新值作为参数==。

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

10. `components: {}`：组件，父组件可以在模板中渲染另一个组件作为子组件

    ```vue
    <script>
    //导入子组件
    import ChildComp from './ChildComp.vue'
    
    export default {
      components: {
        // 注册子组件
        ChildComp
      }
    }
    </scripts>
    <template>
      <!-- 渲染子组件 -->
      <ChildComp />
    </template>
    ```

11. `props`：子组件可以通过 `props` 从父组件接受动态数据。

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

    父组件可以像声明 HTML attributes 一样传递 `props`。若要传递动态值，也可以使用 `v-bind` 语法：

    ```vue
    // 在父组件中
    <script>
    import ChildComp from './ChildComp.vue'
    
    export default {
      components: {
        ChildComp
      },
      data() {
        return {
          greeting: 'Hello from parent'
        }
      }
    }
    </script>
    
    <template>
      <ChildComp :msg="greeting" />
    </template>
    ```

12. `Emits`：事件，子组件可以向父组件触发事件。

    `this.$emit()` 的第一个参数是事件的名称。其他所有参数都将传递给事件监听器。

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

    父组件可以使用 `v-on` 监听子组件触发的事件——这里的处理函数接收了子组件触发事件时的**额外参数**并将它赋值给了本地状态：

    ```vue
    // 在父组件中
    <template>
      <ChildComp @response="(msg) => childMsg = msg" />
    </template>
    ```

13. **插槽**：除了通过 `props` 传递数据外，父组件还可以通过**插槽** (slots) 将模板片段传递给子组件：

    ```vue
    <ChildComp>
      This is some slot content!
    </ChildComp>
    ```

    在子组件中，可以使用 `<slot>` 元素作为插槽出口 (slot outlet) 渲染父组件中的插槽内容 (slot content)：

    ```vue
    <!-- 在子组件的模板中 -->
    <slot/>
    <!-- 也可使用如下形式，设定父组件没有传递插槽内容时的默认值 -->
    <slot>Fallback content</slot>
    ```
