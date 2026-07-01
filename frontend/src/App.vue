<template>
  <div class="app-shell">

    <!-- 左侧：会话列表 -->
    <aside class="sidebar">
      <div class="sidebar-top">
        <div class="brand">
          <div class="brand-icon">AI</div>
          <div>
            <div class="brand-name">Model Hub</div>
            <div class="brand-sub">多模型对比</div>
          </div>
        </div>

        <button class="new-chat-btn" @click="createNewChat">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 5v14M5 12h14"/>
          </svg>
          新对话
        </button>
      </div>

      <div class="session-list">
        <div
          v-for="s in sessions"
          :key="s.id"
          class="session-item"
          :class="{ active: currentSessionId === s.id }"
          @click="switchSession(s.id)"
        >
          <svg class="session-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
          <span class="session-title">{{ s.title || '新对话' }}</span>
          <button
            class="session-delete"
            title="删除对话"
            @click="deleteSession(s.id, $event)"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div v-if="sessions.length === 0" class="session-empty">
          暂无对话，点击上方创建
        </div>
      </div>

      <div class="sidebar-footer">
        <span class="ws-dot" :class="{ online: wsReady }"></span>
        {{ wsReady ? '已连接' : '连接中...' }}
      </div>
    </aside>

    <!-- 中间：聊天主区域 -->
    <main class="chat-main">
      <header class="chat-header">
        <h2>{{ currentSession?.title || 'AI Model Hub' }}</h2>
        <span v-if="currentSession?.dbSessionId" class="session-badge">
          #{{ currentSession.dbSessionId }}
        </span>
      </header>

      <div class="chat-scroll" ref="chatBox">
        <div v-if="!currentChatList.length" class="welcome">
          <div class="welcome-icon">✦</div>
          <h3>开始一段新对话</h3>
          <p>输入问题，同时将获得 GLM、DeepSeek、Kimi、Qwen 四个模型的回答对比</p>
        </div>

        <div
          v-for="chat in currentChatList"
          :key="chat.id"
          class="turn-block fade-in"
        >
          <!-- 用户消息 -->
          <div class="msg-row user-row">
            <div
              class="bubble user-bubble"
              :class="{ selected: activeChatId === chat.id }"
              @click="selectTurn(chat.id)"
            >
              {{ chat.question }}
            </div>
          </div>

          <!-- 助手摘要 -->
          <div
            class="msg-row assistant-row"
            :class="{ active: activeChatId === chat.id }"
            @click="selectTurn(chat.id)"
          >
            <div class="avatar">AI</div>
            <div class="bubble assistant-bubble">
              <div v-if="isTurnLoading(chat)" class="typing-indicator">
                <span></span><span></span><span></span>
              </div>
              <div v-else class="assistant-preview">
                {{ getTurnPreview(chat) }}
                <span class="view-hint">→ 查看右侧模型对比</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="input-area">
        <div class="input-wrapper">
          <textarea
            ref="inputRef"
            v-model="message"
            class="chat-input"
            placeholder="输入消息… Enter 发送，Shift+Enter 换行"
            rows="1"
            @keydown="handleKeydown"
            @input="autoResize"
          ></textarea>
          <button
            class="send-btn"
            :class="{ 'stop-btn': isGenerating }"
            :disabled="!isGenerating && !canSend"
            @click="handleAction"
          >
            <svg v-if="!isGenerating" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
            </svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <rect x="6" y="6" width="12" height="12" rx="1"/>
            </svg>
            <span class="btn-label">{{ isGenerating ? '停止生成' : '发送' }}</span>
          </button>
        </div>
        <p class="input-hint">四模型并行 · 流式输出 · 多轮记忆</p>
      </div>
    </main>

    <!-- 右侧：模型对比面板 -->
    <aside class="model-panel">
      <div class="panel-header">
        <h3>模型对比</h3>
        <span v-if="activeChat" class="panel-sub">第 {{ activeChatIndex + 1 }} 轮</span>
      </div>

      <div v-if="!activeChat" class="panel-empty">
        <p>发送消息后，这里将展示四个模型的回答</p>
      </div>

      <div v-else class="model-list">
        <div
          v-for="m in MODELS"
          :key="m.key"
          class="model-card fade-in"
          :class="{
            loading: activeChat.answers[m.key].loading,
            error: !activeChat.answers[m.key].loading && activeChat.answers[m.key].status === 'error'
          }"
        >
          <div class="model-card-header">
            <div class="model-info">
              <span
                class="model-dot"
                :style="{ background: activeChat.answers[m.key].status === 'error' && !activeChat.answers[m.key].loading ? '#6b7280' : m.color }"
              ></span>
              <span class="model-name">{{ m.label }}</span>
            </div>
            <span v-if="activeChat.answers[m.key].loading" class="status loading-status">
              <span class="typing-indicator small"><span></span><span></span><span></span></span>
            </span>
            <span v-else-if="activeChat.answers[m.key].status === 'error'" class="status error-status">不可用</span>
            <span v-else class="status done-status">完成</span>
          </div>

          <div class="model-body">
            <div
              v-if="activeChat.answers[m.key].loading && !activeChat.answers[m.key].data"
              class="model-placeholder"
            >
              思考中<span class="dot-anim">...</span>
            </div>
            <div
              v-else-if="activeChat.answers[m.key].loading"
              class="model-streaming"
            >{{ activeChat.answers[m.key].data }}<span class="stream-cursor">▍</span></div>
            <div
              v-else-if="activeChat.answers[m.key].status === 'error'"
              class="model-error-text"
            >{{ activeChat.answers[m.key].data }}</div>
            <div
              v-else
              class="markdown-body"
              v-html="renderMd(activeChat.answers[m.key].data)"
            ></div>
          </div>
        </div>
      </div>
    </aside>

  </div>
</template>

<script>
import { renderMarkdown } from "./utils/markdown.js";

const MODELS = [
  { key: "glm", label: "GLM", color: "#3b82f6" },
  { key: "deepseek", label: "DeepSeek", color: "#10b981" },
  { key: "kimi", label: "Kimi", color: "#f59e0b" },
  { key: "qwen", label: "Qwen", color: "#a855f7" },
];

export default {
  data() {
    return {
      MODELS,
      ws: null,
      wsReady: false,
      pendingMessages: [],
      message: "",
      sessions: [],
      currentSessionId: null,
      activeChatId: null,
      isGenerating: false,
      stopFlag: false,
    };
  },

  computed: {
    currentSession() {
      return this.sessions.find((s) => s.id === this.currentSessionId);
    },

    currentChatList() {
      return this.currentSession ? this.currentSession.chatList : [];
    },

    activeChat() {
      if (!this.currentChatList.length) return null;
      return (
        this.currentChatList.find((c) => c.id === this.activeChatId) ||
        this.currentChatList[this.currentChatList.length - 1]
      );
    },

    activeChatIndex() {
      if (!this.activeChat) return -1;
      return this.currentChatList.findIndex((c) => c.id === this.activeChat.id);
    },

    canSend() {
      return this.message.trim().length > 0;
    },

    isCurrentTurnLoading() {
      const last = this.currentChatList[this.currentChatList.length - 1];
      if (!last) return false;
      return Object.values(last.answers).some((a) => a.loading);
    },
  },

  watch: {
    currentSessionId() {
      const list = this.currentChatList;
      this.activeChatId = list.length ? list[list.length - 1].id : null;
    },
  },

  mounted() {
    this.loadLocal();
    if (this.currentChatList.length) {
      this.activeChatId = this.currentChatList[this.currentChatList.length - 1].id;
    }
    this.connect();
  },

  beforeUnmount() {
    if (this.ws) {
      this.ws.onclose = null;
      this.ws.close();
    }
  },

  methods: {
    renderMd(text) {
      return renderMarkdown(text);
    },

    isTurnLoading(chat) {
      return Object.values(chat.answers).some((a) => a.loading);
    },

    getTurnPreview(chat) {
      const success = MODELS.find(
        (m) => chat.answers[m.key].data && chat.answers[m.key].status !== "error"
      );
      if (success) {
        const text = chat.answers[success.key].data;
        return text.length > 80 ? text.slice(0, 80) + "…" : text;
      }
      if (this.isTurnLoading(chat)) {
        return "正在生成回答…";
      }
      return "部分模型暂不可用";
    },

    selectTurn(id) {
      this.activeChatId = id;
    },

    connect() {
      if (this.ws && this.ws.readyState <= WebSocket.OPEN) {
        return;
      }

      this.wsReady = false;
      this.ws = new WebSocket("ws://127.0.0.1:8000/ws/compare");

      this.ws.onopen = () => {
        console.log("WebSocket 已连接");
        this.wsReady = true;
        this.flushPendingMessages();
      };

      this.ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);

        if (msg.type === "session") {
          const session = this.currentSession;
          if (session) {
            session.dbSessionId = msg.session_id;
            this.saveLocal();
            if (this.stopFlag) {
              this.sendPayload(
                JSON.stringify({
                  type: "stop",
                  session_id: msg.session_id,
                })
              );
            }
          }
          return;
        }

        if (msg.type === "stop") {
          return;
        }

        if (msg.model === "error") {
          console.error("服务端错误:", msg.data);
          return;
        }

        const session = this.currentSession;
        if (!session) return;

        const last = session.chatList[session.chatList.length - 1];
        if (!last) return;

        const target = last.answers[msg.model];
        if (!target) return;

        target.data = msg.data;
        target.loading = !msg.done;

        if (msg.done) {
          target.status = msg.status || "success";
        }

        if (!this.activeChatId || this.activeChatId === last.id) {
          this.activeChatId = last.id;
        }

        this.saveLocal();

        if (msg.done) {
          this.scrollToBottom();
          this.checkGenerationComplete();
        }
      };

      this.ws.onerror = (err) => {
        console.error("WebSocket 错误", err);
      };

      this.ws.onclose = () => {
        console.log("WebSocket 断开，2 秒后重连...");
        this.wsReady = false;
        this.ws = null;
        setTimeout(() => this.connect(), 2000);
      };
    },

    flushPendingMessages() {
      while (this.pendingMessages.length > 0) {
        const payload = this.pendingMessages.shift();
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(payload);
        }
      }
    },

    sendPayload(payload) {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(payload);
        return;
      }

      this.pendingMessages.push(payload);

      if (!this.ws || this.ws.readyState === WebSocket.CLOSED) {
        this.connect();
      }
    },

    createNewChat() {
      const session = {
        id: Date.now(),
        dbSessionId: null,
        title: "新对话",
        chatList: [],
      };

      this.sessions.unshift(session);
      this.currentSessionId = session.id;
      this.activeChatId = null;
      this.saveLocal();
    },

    switchSession(id) {
      this.currentSessionId = id;
      const list = this.currentChatList;
      this.activeChatId = list.length ? list[list.length - 1].id : null;
      this.saveLocal();
      this.$nextTick(() => this.scrollToBottom());
    },

    deleteSession(id, event) {
      event.stopPropagation();
      const idx = this.sessions.findIndex((s) => s.id === id);
      if (idx === -1) return;

      this.sessions.splice(idx, 1);

      if (this.currentSessionId === id) {
        this.currentSessionId = this.sessions[0]?.id || null;
        const list = this.currentChatList;
        this.activeChatId = list.length ? list[list.length - 1].id : null;
      }

      this.saveLocal();
    },

    handleKeydown(e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        if (this.isGenerating) return;
        this.send();
      }
    },

    handleAction() {
      if (this.isGenerating) {
        this.stopGenerate();
      } else {
        this.send();
      }
    },

    checkGenerationComplete() {
      if (this.stopFlag) return;

      const last = this.currentChatList[this.currentChatList.length - 1];
      if (!last) {
        this.isGenerating = false;
        return;
      }

      const allDone = Object.values(last.answers).every((a) => !a.loading);
      if (allDone) {
        this.isGenerating = false;
      }
    },

    stopGenerate() {
      this.stopFlag = true;
      this.isGenerating = false;

      const session = this.currentSession;
      if (session?.dbSessionId) {
        this.sendPayload(
          JSON.stringify({
            type: "stop",
            session_id: session.dbSessionId,
          })
        );
      }

      const last = session?.chatList[session.chatList.length - 1];
      if (last) {
        for (const key of Object.keys(last.answers)) {
          if (last.answers[key].loading) {
            last.answers[key].loading = false;
            if (!last.answers[key].data) {
              last.answers[key].data = "已停止生成";
            }
          }
        }
        this.saveLocal();
      }
    },

    autoResize() {
      const el = this.$refs.inputRef;
      if (!el) return;
      el.style.height = "auto";
      el.style.height = Math.min(el.scrollHeight, 160) + "px";
    },

    send() {
      if (!this.canSend || this.isGenerating) return;

      if (!this.currentSession) {
        this.createNewChat();
      }

      const session = this.currentSession;
      const question = this.message.trim();

      const last = session.chatList[session.chatList.length - 1];
      if (last && Object.values(last.answers).some((a) => a.loading)) {
        return;
      }

      this.isGenerating = true;
      this.stopFlag = false;

      const chatItem = {
        id: Date.now(),
        question,
        answers: {
          glm: { data: "", loading: true, status: "success" },
          deepseek: { data: "", loading: true, status: "success" },
          kimi: { data: "", loading: true, status: "success" },
          qwen: { data: "", loading: true, status: "success" },
        },
      };

      session.chatList.push(chatItem);
      this.activeChatId = chatItem.id;

      if (session.chatList.length === 1) {
        session.title = question.slice(0, 24);
      }

      this.message = "";
      this.$nextTick(() => {
        const el = this.$refs.inputRef;
        if (el) el.style.height = "auto";
      });

      this.sendPayload(
        JSON.stringify({
          type: "chat",
          session_id: session.dbSessionId,
          message: question,
        })
      );

      this.saveLocal();
      this.scrollToBottom();
    },

    saveLocal() {
      localStorage.setItem("sessions", JSON.stringify(this.sessions));
      localStorage.setItem("currentSessionId", this.currentSessionId);
    },

    loadLocal() {
      const s = localStorage.getItem("sessions");
      const id = localStorage.getItem("currentSessionId");

      if (s) this.sessions = JSON.parse(s);
      if (id) this.currentSessionId = Number(id);
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const el = this.$refs.chatBox;
        if (el) el.scrollTop = el.scrollHeight;
      });
    },
  },
};
</script>

<style scoped>
/* ===== 布局 ===== */
.app-shell {
  display: flex;
  height: 100vh;
  background: #0d0d0d;
  color: #ececec;
  overflow: hidden;
}

/* ===== 左侧栏 ===== */
.sidebar {
  width: 260px;
  min-width: 260px;
  background: #111111;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #1e1e1e;
}

.sidebar-top {
  padding: 16px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.brand-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: #fff;
}

.brand-name {
  font-size: 15px;
  font-weight: 600;
  color: #f3f4f6;
}

.brand-sub {
  font-size: 11px;
  color: #6b7280;
  margin-top: 2px;
}

.new-chat-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  background: transparent;
  border: 1px solid #2a2a2a;
  border-radius: 10px;
  color: #e5e7eb;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.new-chat-btn:hover {
  background: #1a1a1a;
  border-color: #3b82f6;
  transform: translateY(-1px);
}

.session-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 8px 8px;
}

.session-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 2px;
  transition: all 0.15s ease;
  position: relative;
}

.session-item:hover {
  background: #1a1a1a;
  transform: translateY(-1px);
}

.session-item.active {
  background: #1e293b;
}

.session-icon {
  flex-shrink: 0;
  color: #6b7280;
}

.session-item.active .session-icon {
  color: #3b82f6;
}

.session-title {
  flex: 1;
  font-size: 13px;
  color: #d1d5db;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.session-delete {
  opacity: 0;
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  transition: all 0.15s;
}

.session-item:hover .session-delete {
  opacity: 1;
}

.session-delete:hover {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.session-empty {
  padding: 20px 12px;
  font-size: 12px;
  color: #4b5563;
  text-align: center;
}

.sidebar-footer {
  padding: 12px 16px;
  border-top: 1px solid #1e1e1e;
  font-size: 11px;
  color: #6b7280;
  display: flex;
  align-items: center;
  gap: 6px;
}

.ws-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #ef4444;
  animation: breathe 2s ease-in-out infinite;
}

.ws-dot.online {
  background: #22c55e;
  animation: none;
}

/* ===== 中间聊天区 ===== */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: #0d0d0d;
}

.chat-header {
  padding: 16px 24px;
  border-bottom: 1px solid #1a1a1a;
  display: flex;
  align-items: center;
  gap: 10px;
}

.chat-header h2 {
  margin: 0;
  font-size: 15px;
  font-weight: 500;
  color: #f3f4f6;
}

.session-badge {
  font-size: 11px;
  color: #6b7280;
  background: #1a1a1a;
  padding: 2px 8px;
  border-radius: 10px;
}

.chat-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  scroll-behavior: smooth;
}

.welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  color: #6b7280;
  animation: fadeIn 0.5s ease;
}

.welcome-icon {
  font-size: 40px;
  color: #3b82f6;
  margin-bottom: 16px;
}

.welcome h3 {
  margin: 0 0 8px;
  color: #e5e7eb;
  font-size: 20px;
  font-weight: 500;
}

.welcome p {
  margin: 0;
  font-size: 14px;
  max-width: 360px;
  line-height: 1.6;
}

.turn-block {
  margin-bottom: 32px;
}

.msg-row {
  display: flex;
  margin-bottom: 12px;
}

.user-row {
  justify-content: flex-end;
}

.assistant-row {
  justify-content: flex-start;
  align-items: flex-start;
  gap: 10px;
  cursor: pointer;
  border-radius: 12px;
  padding: 4px;
  margin-left: -4px;
  transition: background 0.15s;
}

.assistant-row.active {
  background: rgba(59, 130, 246, 0.06);
}

.avatar {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: #1e293b;
  color: #3b82f6;
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 4px;
}

.bubble {
  max-width: 75%;
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.65;
  word-break: break-word;
}

.user-bubble {
  background: #2563eb;
  color: #fff;
  border-bottom-right-radius: 4px;
  cursor: pointer;
  transition: opacity 0.15s;
}

.user-bubble.selected {
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.4);
}

.assistant-bubble {
  background: #1a1a1a;
  color: #d1d5db;
  border-bottom-left-radius: 4px;
  max-width: 85%;
}

.assistant-preview {
  font-size: 13px;
  color: #9ca3af;
}

.view-hint {
  display: block;
  margin-top: 6px;
  font-size: 11px;
  color: #3b82f6;
}

/* ===== 输入区 ===== */
.input-area {
  padding: 16px 24px 20px;
  background: linear-gradient(to top, #0d0d0d 80%, transparent);
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 16px;
  padding: 10px 10px 10px 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
  transition: border-color 0.2s;
}

.input-wrapper:focus-within {
  border-color: #3b82f6;
}

.chat-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #f3f4f6;
  font-size: 14px;
  line-height: 1.5;
  resize: none;
  max-height: 160px;
  font-family: inherit;
}

.chat-input::placeholder {
  color: #4b5563;
}

.send-btn {
  min-width: 36px;
  height: 36px;
  border-radius: 10px;
  border: none;
  background: #2563eb;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  flex-shrink: 0;
  padding: 0 12px;
  transition: all 0.2s;
}

.send-btn.stop-btn {
  background: #374151;
  border: 1px solid #4b5563;
}

.send-btn.stop-btn:hover:not(:disabled) {
  background: #ef4444;
  border-color: #ef4444;
}

.btn-label {
  font-size: 13px;
  font-weight: 500;
}

.send-btn:hover:not(:disabled) {
  background: #3b82f6;
  transform: translateY(-1px);
}

.send-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.input-hint {
  margin: 8px 0 0;
  font-size: 11px;
  color: #374151;
  text-align: center;
}

/* ===== 右侧模型面板 ===== */
.model-panel {
  width: 380px;
  min-width: 340px;
  background: #111111;
  border-left: 1px solid #1e1e1e;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  padding: 16px 20px;
  border-bottom: 1px solid #1a1a1a;
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.panel-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #f3f4f6;
}

.panel-sub {
  font-size: 11px;
  color: #6b7280;
}

.panel-empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  text-align: center;
}

.panel-empty p {
  font-size: 13px;
  color: #4b5563;
  line-height: 1.6;
}

.model-list {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.model-card {
  background: #1a1a1a;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.model-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.model-card.loading {
  animation: breathe 2s ease-in-out infinite;
}

.model-card.error {
  opacity: 0.82;
  background: #161616;
}

.model-card.error:hover {
  transform: none;
  box-shadow: none;
}

.model-card.error .model-name {
  color: #9ca3af;
}

.error-status {
  color: #6b7280;
}

.model-error-text {
  color: #6b7280;
  font-size: 13px;
  line-height: 1.6;
}

.model-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-bottom: 1px solid #252525;
}

.model-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.model-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.model-name {
  font-size: 13px;
  font-weight: 600;
  color: #e5e7eb;
}

.status {
  font-size: 11px;
}

.loading-status {
  color: #6b7280;
}

.done-status {
  color: #22c55e;
}

.model-body {
  padding: 12px 14px;
  min-height: 48px;
  font-size: 13px;
  line-height: 1.65;
  color: #d1d5db;
}

.model-placeholder {
  color: #6b7280;
}

.model-streaming {
  white-space: pre-wrap;
  word-break: break-word;
  color: #d1d5db;
}

.stream-cursor {
  color: #3b82f6;
  animation: blink 1s step-end infinite;
}

.dot-anim {
  animation: dotPulse 1.4s infinite;
}

/* ===== Markdown ===== */
.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  margin: 12px 0 8px;
  color: #f3f4f6;
  font-weight: 600;
}

.markdown-body :deep(h1) { font-size: 16px; }
.markdown-body :deep(h2) { font-size: 15px; }
.markdown-body :deep(h3) { font-size: 14px; }

.markdown-body :deep(p) {
  margin: 0 0 8px;
}

.markdown-body :deep(code) {
  background: #252525;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: ui-monospace, monospace;
  font-size: 12px;
  color: #93c5fd;
}

.markdown-body :deep(pre) {
  background: #0d0d0d;
  border-radius: 8px;
  padding: 12px;
  overflow-x: auto;
  margin: 8px 0;
}

.markdown-body :deep(pre code) {
  background: none;
  padding: 0;
  color: #e5e7eb;
}

.markdown-body :deep(ul) {
  margin: 4px 0 8px;
  padding-left: 20px;
}

.markdown-body :deep(a) {
  color: #3b82f6;
  text-decoration: none;
}

.markdown-body :deep(a:hover) {
  text-decoration: underline;
}

.markdown-body :deep(strong) {
  color: #f3f4f6;
}

/* ===== 动画 ===== */
.fade-in {
  animation: fadeIn 0.35s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes breathe {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.85; }
}

@keyframes blink {
  50% { opacity: 0; }
}

@keyframes dotPulse {
  0%, 20% { opacity: 0.2; }
  50% { opacity: 1; }
  100% { opacity: 0.2; }
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 4px 0;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #6b7280;
  animation: typingBounce 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) { animation-delay: 0.16s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.32s; }

.typing-indicator.small span {
  width: 4px;
  height: 4px;
}

@keyframes typingBounce {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-4px); opacity: 1; }
}

/* ===== 响应式 ===== */
@media (max-width: 1100px) {
  .model-panel {
    display: none;
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 220px;
    min-width: 220px;
  }
}
</style>
