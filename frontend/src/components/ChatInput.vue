<template>
  <div class="input-box">
    <input
      :value="message"
      @input="$emit('update:message', $event.target.value)"
      @keyup.enter="$emit('send')"
      placeholder="请输入你的问题..."
    />

    <button @click="$emit('send')">
      发送
    </button>
  </div>
</template>

<script>
export default {
  name: "ChatInput",

  props: {
    message: {
      type: String,
      default: ""
    }
  },

  emits: [
    "update:message",
    "send"
  ]
}
</script>

<style scoped>
.input-box{
    display:flex;
    gap:12px;
    margin:20px 0;
}

input{
    flex:1;
    padding:12px;
    border-radius:10px;
    border:1px solid #444;
    background:#202123;
    color:white;
}

button{
    width:90px;
    border:none;
    border-radius:10px;
    background:#10a37f;
    color:white;
    cursor:pointer;
}
</style>