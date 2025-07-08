<script setup>
import {
  NInput, NButton, NCard, NDatePicker, NFormItem,
  NInputNumber, NTabs, NTabPane, NDrawer, NDrawerContent,
  NProgress, NIcon, NTag, NRadioGroup, NRadio, NSpace
} from 'naive-ui'
import { watch, ref, onMounted, computed } from "vue";
import MarkdownIt from 'markdown-it';
import { fetchEventSource, EventStreamContentType } from '@microsoft/fetch-event-source';
import { useStorage } from '@vueuse/core';
import { Solar } from 'lunar-javascript'

import { useIsMobile } from '../utils/composables'
import About from '../components/About.vue'
import { useGlobalState } from '../store'

const { customAISettings, currentSession, resetSession, updateSession, addToConversation } = useGlobalState()
import { DIVINATION_OPTIONS } from "../config/constants";
const isMobile = useIsMobile()

const state_jwt = useStorage('jwt')
const prompt = ref("");
const result = useStorage("result", "");
const tmp_result = ref("");
const prompt_type = useStorage("prompt_type", "tarot");
const menu_type = useStorage("menu_type", "divination");
const lunarBirthday = ref("");
const birthday = useStorage("birthday", "2000-08-17 00:00:00");
const loading = ref(false);
const API_BASE = import.meta.env.VITE_API_BASE || "";
const IS_TAURI = import.meta.env.VITE_IS_TAURI || "";
const md = new MarkdownIt();
const showDrawer = ref(false)
const plum_flower = useStorage("plum_flower", { 
  number: "123456", 
  use_custom_time: false, 
  custom_datetime: "" 
})

// 塔罗牌相关状态
const tarot_draw_mode = useStorage("tarot_draw_mode", "random")
const tarot_numbers = useStorage("tarot_numbers", { first: 1, second: 2, third: 3 })

// 追问相关状态
const followUpQuestion = ref("")
const isFollowUpMode = ref(false)


// 计算属性：检查塔罗牌数字是否完整
const isTarotNumbersComplete = computed(() => {
  if (prompt_type.value !== 'tarot' || tarot_draw_mode.value !== 'numbers') {
    return true;
  }
  const { first, second, third } = tarot_numbers.value;
  return first && second && third && 
         first >= 1 && first <= 78 && 
         second >= 1 && second <= 78 && 
         third >= 1 && third <= 78;
});

// 验证塔罗牌输入
const validateTarotInput = () => {
  if (prompt_type.value !== 'tarot') {
    return true; // 非塔罗牌模式，直接通过
  }
  
  if (tarot_draw_mode.value === 'numbers') {
    // 报数字模式，检查三个数字是否都有效
    const { first, second, third } = tarot_numbers.value;
    if (!first || !second || !third) {
      alert('请填写完整的三个数字（1-78）');
      return false;
    }
    if (first < 1 || first > 78 || second < 1 || second > 78 || third < 1 || third > 78) {
      alert('数字必须在1-78之间');
      return false;
    }
  }
  
  return true;
}

// 梅花易数数字验证和分割函数
const validateNumber = (value) => {
  // 只允许数字
  plum_flower.value.number = value.replace(/[^\d]/g, '');
  
  // 限制长度不超过32位
  if (plum_flower.value.number.length > 32) {
    plum_flower.value.number = plum_flower.value.number.slice(0, 32);
  }
}

const splitNumber = (number) => {
  if (!number) return [];
  // 将数字字符串分割为数字数组
  return number.split('').map(digit => parseInt(digit));
}

const onSubmit = async (isFollowUp) => {
  // 确保 isFollowUp 是布尔值
  isFollowUp = Boolean(isFollowUp);
  
  // 防止重复提交
  if (loading.value) {
    return;
  }
  
  // 验证塔罗牌输入（仅首次占卜时验证）
  if (!isFollowUp && !validateTarotInput()) {
    return;
  }
  
  try {
    loading.value = true;
    
    // 清理临时结果，准备接收新内容
    tmp_result.value = "";
    
    if (!isFollowUp) {
      result.value = "";
      resetSession(); // 重置会话状态
    }
    
    showDrawer.value = true;
    const headers = {
      "Authorization": `Bearer ${state_jwt.value || "xxx"}`,
      "Content-Type": "application/json"
    }
    if (customAISettings.value.enable) {
      headers["x-api-key"] = customAISettings.value.apiKey;
      headers["x-api-url"] = customAISettings.value.baseUrl
      headers["x-api-model"] = customAISettings.value.model
    } else if (IS_TAURI) {
      result.value = "请在设置中配置 API BASE URL 和 API KEY";
      return;
    }
    
    // 构建请求体
    let requestBody = {
      prompt: prompt.value || "我的财务状况如何",
      prompt_type: prompt_type.value,
      birthday: birthday.value,
      plum_flower: prompt_type.value == "plum_flower" ? plum_flower.value : null,
      tarot_draw_mode: prompt_type.value == "tarot" ? tarot_draw_mode.value : null,
      tarot_numbers: prompt_type.value == "tarot" && tarot_draw_mode.value == "numbers" ? tarot_numbers.value : null,
      is_follow_up: isFollowUp,
      session_id: isFollowUp ? currentSession.value.sessionId : null,
      follow_up_question: isFollowUp ? followUpQuestion.value : null
    };
    
    console.log('Request body:', requestBody);
    
    await fetchEventSource(`${API_BASE}/api/divination`, {
      method: "POST",
      body: JSON.stringify(requestBody),
      headers: headers,
      openWhenHidden: true,
      onretry: () => false, // 禁用自动重试
      async onopen(response) {
        if (response.ok && response.headers.get('content-type') === EventStreamContentType) {
          return;
        } else if (response.status >= 400 && response.status < 500) {
          throw new Error(`${response.status} ${await response.text()}`);
        }
      },
      onmessage(msg) {
        if (msg.event === 'FatalError') {
          throw new FatalError(msg.data);
        }
        if (!msg.data) {
          return;
        }
        try {
          const data = JSON.parse(msg.data);
          
          if (typeof data === 'string') {
            // 兼容旧格式
            tmp_result.value += data;
          } else if (data.content) {
            // 新格式：包含会话信息
            tmp_result.value += data.content;
            
            // 更新会话状态
            updateSession(data);
          }
          
          // 只在首次占卜时更新result.value，追问时只更新tmp_result用于对话历史
          if (!isFollowUp) {
            result.value = md.render(tmp_result.value);
          }
        } catch (error) {
          console.error(error);
        }
      },
      onclose() {
        // 如果是追问，清空追问输入框并重置追问模式
        if (isFollowUp) {
          followUpQuestion.value = "";
          isFollowUpMode.value = false;
        }
        
        // 将AI回复添加到对话历史
        if (tmp_result.value && currentSession.value.sessionId) {
          addToConversation(tmp_result.value, false);
        }
      },
      onerror(err) {
        result.value = `占卜失败: ${err.message}`;
        throw new Error(`占卜失败: ${err.message}`);
      }
    });
  } catch (error) {
    console.error(error);
    result.value = error.message || "占卜失败";
  } finally {
    loading.value = false;
  }
};

// 追问相关函数
const submitFollowUp = async () => {
  if (!followUpQuestion.value.trim()) {
    return;
  }
  
  if (!currentSession.value.sessionId) {
    alert("请先进行一次占卜，然后才能追问");
    return;
  }
  
  if (!currentSession.value.canFollowUp) {
    alert("追问次数已达上限(10次)");
    return;
  }
  
  // 设置追问模式
  isFollowUpMode.value = true;
  
  // 将用户追问添加到对话历史
  addToConversation(followUpQuestion.value, true);
  
  // 提交追问
  await onSubmit(true);
};

const startNewDivination = () => {
  resetSession();
  isFollowUpMode.value = false;
  tmp_result.value = "";
  result.value = "";
  followUpQuestion.value = "";
};

// 获取结果类型颜色
const getResultTypeColor = () => {
  const typeColors = {
    'tarot': 'primary',
    'plum_flower': 'success', 
    'birthday': 'warning',
    'dream': 'info'
  };
  return typeColors[prompt_type.value] || 'default';
};

// 获取结果类型名称
const getResultTypeName = () => {
  const typeNames = {
    'tarot': '塔罗占卜',
    'plum_flower': '梅花易数',
    'birthday': '生辰八字',
    'dream': '周公解梦'
  };
  return typeNames[prompt_type.value] || '占卜';
};

const computeLunarBirthday = (newBirthday) => {
  try {
    let date = new Date(newBirthday)
    let solar = Solar.fromYmdHms(
      date.getFullYear(), date.getMonth() + 1, date.getDate(),
      date.getHours(), date.getMinutes(), date.getSeconds());
    lunarBirthday.value = solar.getLunar().toFullString();
  } catch (error) {
    console.error(error)
    lunarBirthday.value = '转换失败'
  }
}

watch(birthday, async (newBirthday, oldBirthday) => {
  computeLunarBirthday(newBirthday)
})

const changeTab = async (delta) => {
  let curIndex = DIVINATION_OPTIONS.findIndex((option) => option.key === prompt_type.value);
  let newIndex = curIndex + delta;
  if (newIndex < 0) {
    newIndex = DIVINATION_OPTIONS.length - 1;
  } else if (newIndex >= DIVINATION_OPTIONS.length) {
    newIndex = 0;
  }
  prompt_type.value = DIVINATION_OPTIONS[newIndex].key;
}

onMounted(async () => {
  computeLunarBirthday(birthday.value)
});
</script>

<template>
  <div>
    <n-tabs v-model:value="prompt_type" type="card" animated placement="top">
      <template v-if="isMobile" #prefix>
        <n-button @click="changeTab(-1)">←</n-button>
      </template>
      <template v-if="isMobile" #suffix>
        <n-button @click="changeTab(1)">→</n-button>
      </template>
      <n-tab-pane v-for="option in DIVINATION_OPTIONS" :name="option.key" :tab="option.label">
        <n-card v-if="prompt_type != 'about'">
          <div v-if="prompt_type == 'tarot'">
            <div style="display: inline-block; text-align: left; width: 100%;">
              <h4>塔罗牌占卜 - 三牌阵</h4>
              <n-form-item label="问题" label-placement="left">
                <n-input v-model:value="prompt" type="textarea" round maxlength="40" :autosize="{ minRows: 2 }"
                  placeholder="我的财务状况如何" />
              </n-form-item>
              
              <n-form-item label="抽牌方式" label-placement="left">
                <n-radio-group v-model:value="tarot_draw_mode" name="tarotMode">
                  <n-space>
                    <n-radio value="random">
                      纯随机抽牌
                    </n-radio>
                    <n-radio value="numbers">
                      报数字抽牌
                    </n-radio>
                  </n-space>
                </n-radio-group>
              </n-form-item>
              
              <div v-if="tarot_draw_mode === 'numbers'" class="number-selection">
                <p style="margin: 10px 0; color: #666; font-size: 14px;">
                  请选择三个数字（1-78），系统将洗牌后按你的数字抽取对应位置的牌
                </p>
                <n-space>
                  <n-form-item label="第一张牌" label-placement="top">
                    <n-input-number v-model:value="tarot_numbers.first" :min="1" :max="78" placeholder="1-78" />
                  </n-form-item>
                  <n-form-item label="第二张牌" label-placement="top">
                    <n-input-number v-model:value="tarot_numbers.second" :min="1" :max="78" placeholder="1-78" />
                  </n-form-item>
                  <n-form-item label="第三张牌" label-placement="top">
                    <n-input-number v-model:value="tarot_numbers.third" :min="1" :max="78" placeholder="1-78" />
                  </n-form-item>
                </n-space>
                <p style="margin: 5px 0; color: #999; font-size: 12px;">
                  💡 提示：三个数字可以相同，代表不同牌位的能量共鸣
                </p>
              </div>
              
              <div v-else class="random-mode">
                <p style="margin: 10px 0; color: #666; font-size: 14px;">
                  🎲 将使用完全随机的方式为你抽取三张塔罗牌
                </p>
                <p style="margin: 5px 0; color: #999; font-size: 12px;">
                  系统将自动洗牌并随机选择三张牌作为你的占卜结果
                </p>
              </div>
              
              <!-- 调试信息（开发时临时显示） -->
              <div v-if="false" style="margin: 10px 0; padding: 10px; background: #f0f0f0; border-radius: 6px; font-size: 12px;">
                <p>当前抽牌模式: {{ tarot_draw_mode }}</p>
                <p>数字值: {{ JSON.stringify(tarot_numbers) }}</p>
                <p>按钮可用性: {{ isTarotNumbersComplete }}</p>
              </div>
            </div>
          </div>
          <div v-if="prompt_type == 'birthday'">
            <div style="display: inline-block; text-align: left;">
              <n-form-item label="生日" label-placement="left">
                <n-date-picker v-model:formatted-value="birthday" value-format="yyyy-MM-dd HH:mm:ss" type="datetime" />
              </n-form-item>
              <n-form-item label="农历" label-placement="left">
                <p>{{ lunarBirthday }}</p>
              </n-form-item>
            </div>
          </div>
          <div v-if="prompt_type == 'dream'">
            <n-input v-model:value="prompt" type="textarea" round maxlength="40" :autosize="{ minRows: 3 }"
              placeholder="请输入你的梦境" />
          </div>
          <div v-if="prompt_type == 'plum_flower'">
            <div style="display: inline-block;">
              <h4>梅花易数 - 专业起卦算法</h4>
              
              <!-- 准确率和使用说明 -->
              <div style="background: linear-gradient(135deg, rgba(24, 160, 88, 0.08), rgba(24, 160, 88, 0.03)); border: 1px solid rgba(24, 160, 88, 0.15); border-radius: 12px; padding: 16px; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                  <n-icon size="18" color="#18a058" style="margin-right: 8px;">
                    <svg viewBox="0 0 24 24">
                      <path fill="currentColor" d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"/>
                    </svg>
                  </n-icon>
                  <span style="font-weight: 600; color: #18a058; font-size: 14px;">算法说明</span>
                </div>
                <p style="margin: 0; color: #555; font-size: 13px; line-height: 1.6;">
                  经过多次回测，该AI解卦程序综合准确率约为<strong>78-82%</strong>。
                  占卜结果仅供参考，请结合个人实际情况理性判断，切勿完全依赖占卜结果做重大决策。
                </p>
              </div>
              
              <n-form-item label="问题" label-placement="left">
                <n-input v-model:value="prompt" type="textarea" round maxlength="40" :autosize="{ minRows: 2 }"
                  placeholder="请输入你想占卜的问题（可选）" />
              </n-form-item>
              <p style="margin: 10px 0; color: #666; font-size: 14px;">
                请输入一个任意数字（少于32位），系统会自动按位数分割后根据梅花易数传统规则起卦
              </p>
              <n-form-item label="起卦数字" label-placement="left">
                <div>
                  <n-input
                    v-model:value="plum_flower.number"
                    placeholder="请输入数字，如: 123456"
                    maxlength="32"
                    @input="validateNumber"
                    style="width: 100%;"
                  />
                  <p style="margin-top: 8px; color: #999; font-size: 12px;">
                    <span v-if="plum_flower.number">
                      将分割为：{{ splitNumber(plum_flower.number) }}
                      ({{ splitNumber(plum_flower.number).length }}位数字
                      {{ splitNumber(plum_flower.number).length % 2 === 0 ? '偶数：平分为二' : '奇数：前少后多' }})
                    </span>
                    <span v-else>
                      输入数字后会显示分割预览
                    </span>
                  </p>
                </div>
              </n-form-item>
              
              <n-form-item label="起卦时间" label-placement="left">
                <div>
                  <n-space vertical>
                    <n-radio-group v-model:value="plum_flower.use_custom_time" name="timeMode">
                      <n-space>
                        <n-radio :value="false">
                          使用当前时间
                        </n-radio>
                        <n-radio :value="true">
                          自定义时间
                        </n-radio>
                      </n-space>
                    </n-radio-group>
                    
                    <div v-if="plum_flower.use_custom_time">
                      <n-date-picker 
                        v-model:formatted-value="plum_flower.custom_datetime" 
                        value-format="yyyy-MM-dd HH:mm:ss" 
                        type="datetime"
                        placeholder="选择起卦时间"
                        style="width: 100%;"
                      />
                      <p style="margin-top: 5px; color: #666; font-size: 12px;">
                        💡 自定义时间会影响时辰计算，进而影响卦气和动爻等关键因素...
                      </p>
                    </div>
                    
                    <div v-else>
                      <p style="color: #666; font-size: 12px;">
                        🕐 将使用当前时间：{{ new Date().toLocaleString('zh-CN') }}
                      </p>
                    </div>
                  </n-space>
                </div>
              </n-form-item>
            </div>
          </div>
          <div v-if="menu_type != 'about'" class="button-container">
            <n-button class="button" @click="showDrawer = !showDrawer" tertiary type="primary">
              {{ loading ? "点击打开占卜结果页面" : "查看占卜结果" }}
            </n-button>
            <n-button class="button" @click="() => onSubmit(false)" type="primary" :disabled="loading || !isTarotNumbersComplete">
              {{ loading ? "正在占卜中..." : "占卜" }}
            </n-button>
            <n-button v-if="currentSession.sessionId" class="button" @click="startNewDivination" tertiary>
              重新占卜
            </n-button>
          </div>
        </n-card>
      </n-tab-pane>
      <n-tab-pane name="about" tab="关于">
        <About />
      </n-tab-pane>
    </n-tabs>
    <n-drawer v-model:show="showDrawer" style="height: 85vh;" placement="bottom" :trap-focus="false"
      :block-scroll="false">
      <n-drawer-content closable>
        <template #header>
          <div class="result-header">
            <div class="result-title">
              <span class="title-text">占卜结果</span>
              <div class="title-meta">
                <n-tag size="small" :type="getResultTypeColor()" round>
                  {{ getResultTypeName() }}
                </n-tag>
                <span class="result-time">{{ new Date().toLocaleString('zh-CN') }}</span>
              </div>
            </div>
          </div>
        </template>
        
        <!-- 算法说明 -->
        <div v-if="prompt_type === 'tarot'" class="tarot-algorithm-notice">
          <n-icon size="16" style="margin-right: 6px; color: #18a058;">
            <svg viewBox="0 0 24 24">
              <path fill="currentColor" d="M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7A1,1 0 0,0 14,8H16A1,1 0 0,0 17,7V5.73C16.4,5.39 16,4.74 16,4A2,2 0 0,1 18,2A2,2 0 0,1 20,4C20,4.74 19.6,5.39 19,5.73V7A3,3 0 0,1 16,10V10.93C17.8,11.35 19,12.86 19,14.5C19,16.43 17.43,18 15.5,18H8.5C6.57,18 5,16.43 5,14.5C5,12.86 6.2,11.35 8,10.93V10A3,3 0 0,1 5,7V5.73C4.4,5.39 4,4.74 4,4A2,2 0 0,1 6,2A2,2 0 0,1 8,4C8,4.74 7.6,5.39 7,5.73V7A1,1 0 0,0 8,8H10A1,1 0 0,0 11,7V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2Z"/>
            </svg>
          </n-icon>
          <span>使用Fisher-Yates算法洗牌 • 真实随机抽牌 • AI负责解读</span>
        </div>
        
        <!-- 梅花易数算法说明和免责声明 -->
        <div v-if="prompt_type === 'plum_flower'" class="plum-flower-disclaimer">
          <n-icon size="16" style="margin-right: 6px; color: #18a058;">
            <svg viewBox="0 0 24 24">
              <path fill="currentColor" d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"/>
            </svg>
          </n-icon>
          <span>遵循传统梅花易数算法 • 综合准确率约80% • 结果仅供参考，请结合实际情况理性判断</span>
        </div>
        
        <!-- 主要结果区域 -->
        <div class="result-container">
          <!-- 对话历史显示 -->
          <div v-if="currentSession.sessionId && currentSession.conversationHistory.length > 0" class="conversation-history">
            <div 
              v-for="(message, index) in currentSession.conversationHistory" 
              :key="index"
              class="message-card"
              :class="{ 'user-message': message.isUser, 'ai-message': !message.isUser }"
            >
              <div class="message-header">
                <div class="message-avatar">
                  <n-icon size="16" :color="message.isUser ? '#2080f0' : '#18a058'">
                    <svg v-if="message.isUser" viewBox="0 0 24 24">
                      <path fill="currentColor" d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"/>
                    </svg>
                    <svg v-else viewBox="0 0 24 24">
                      <path fill="currentColor" d="M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7A1,1 0 0,0 14,8H16A1,1 0 0,0 17,7V5.73C16.4,5.39 16,4.74 16,4A2,2 0 0,1 18,2A2,2 0 0,1 20,4C20,4.74 19.6,5.39 19,5.73V7A3,3 0 0,1 16,10V10.93C17.8,11.35 19,12.86 19,14.5C19,16.43 17.43,18 15.5,18H8.5C6.57,18 5,16.43 5,14.5C5,12.86 6.2,11.35 8,10.93V10A3,3 0 0,1 5,7V5.73C4.4,5.39 4,4.74 4,4A2,2 0 0,1 6,2A2,2 0 0,1 8,4C8,4.74 7.6,5.39 7,5.73V7A1,1 0 0,0 8,8H10A1,1 0 0,0 11,7V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2Z"/>
                    </svg>
                  </n-icon>
                </div>
                <span class="message-role">{{ message.isUser ? '您的提问' : 'AI解答' }}</span>
                <span class="message-time">{{ new Date(message.timestamp).toLocaleTimeString('zh-CN') }}</span>
              </div>
              <div class="message-content">
                <div v-if="message.isUser" class="user-question">
                  {{ message.content }}
                </div>
                <div v-else class="ai-response" v-html="md.render(message.content)"></div>
              </div>
            </div>
          </div>
          
          <!-- 当前占卜内容 -->
          <div class="current-result">
            <div v-if="!currentSession.sessionId || currentSession.conversationHistory.length === 0" class="initial-result">
              <div class="message-card ai-message">
                <div class="message-header">
                  <div class="message-avatar">
                    <n-icon size="16" color="#18a058">
                      <svg viewBox="0 0 24 24">
                        <path fill="currentColor" d="M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7A1,1 0 0,0 14,8H16A1,1 0 0,0 17,7V5.73C16.4,5.39 16,4.74 16,4A2,2 0 0,1 18,2A2,2 0 0,1 20,4C20,4.74 19.6,5.39 19,5.73V7A3,3 0 0,1 16,10V10.93C17.8,11.35 19,12.86 19,14.5C19,16.43 17.43,18 15.5,18H8.5C6.57,18 5,16.43 5,14.5C5,12.86 6.2,11.35 8,10.93V10A3,3 0 0,1 5,7V5.73C4.4,5.39 4,4.74 4,4A2,2 0 0,1 6,2A2,2 0 0,1 8,4C8,4.74 7.6,5.39 7,5.73V7A1,1 0 0,0 8,8H10A1,1 0 0,0 11,7V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2Z"/>
                      </svg>
                    </n-icon>
                  </div>
                  <span class="message-role">AI解答</span>
                  <span class="message-time">{{ new Date().toLocaleTimeString('zh-CN') }}</span>
                </div>
                <div class="message-content">
                  <div class="ai-response" v-html="result"></div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 当前追问回复（流式显示） -->
          <div v-if="loading && isFollowUpMode && tmp_result" class="current-followup-reply">
            <div class="message-card ai-message">
              <div class="message-header">
                <div class="message-avatar">
                  <n-icon size="16" color="#18a058">
                    <svg viewBox="0 0 24 24">
                      <path fill="currentColor" d="M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7A1,1 0 0,0 14,8H16A1,1 0 0,0 17,7V5.73C16.4,5.39 16,4.74 16,4A2,2 0 0,1 18,2A2,2 0 0,1 20,4C20,4.74 19.6,5.39 19,5.73V7A3,3 0 0,1 16,10V10.93C17.8,11.35 19,12.86 19,14.5C19,16.43 17.43,18 15.5,18H8.5C6.57,18 5,16.43 5,14.5C5,12.86 6.2,11.35 8,10.93V10A3,3 0 0,1 5,7V5.73C4.4,5.39 4,4.74 4,4A2,2 0 0,1 6,2A2,2 0 0,1 8,4C8,4.74 7.6,5.39 7,5.73V7A1,1 0 0,0 8,8H10A1,1 0 0,0 11,7V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2Z"/>
                    </svg>
                  </n-icon>
                </div>
                <span class="message-role">AI解答</span>
                <span class="message-time">{{ new Date().toLocaleTimeString('zh-CN') }}</span>
                <span class="streaming-indicator">💭 思考中...</span>
              </div>
              <div class="message-content">
                <div class="ai-response" v-html="md.render(tmp_result)"></div>
              </div>
            </div>
          </div>
          
          <!-- 追问区域 -->
          <div v-if="currentSession.sessionId" class="interaction-area">
            <!-- 分隔线 -->
            <div class="section-divider">
              <span class="divider-text">深入探讨</span>
            </div>
            
            <!-- 可以追问 -->
            <div v-if="currentSession.canFollowUp" class="follow-up-area">
              <div class="follow-up-input">
                <n-input 
                  v-model:value="followUpQuestion" 
                  type="textarea" 
                  placeholder="继续探讨..."
                  :autosize="{ minRows: 1, maxRows: 3 }"
                  maxlength="200"
                  :bordered="false"
                  size="large"
                />
              </div>
              <div class="follow-up-actions">
                <span class="remaining-count">{{ 10 - currentSession.followUpCount }}/10</span>
                <n-button 
                  type="primary" 
                  @click="submitFollowUp" 
                  :disabled="loading || !followUpQuestion.trim()"
                  :loading="loading"
                  text
                  size="small"
                >
                  {{ loading ? "..." : "发送" }}
                </n-button>
              </div>
            </div>
            
            <!-- 追问用完 -->
            <div v-else class="follow-up-finished">
              <span class="finished-text">探讨已达上限</span>
              <n-button @click="startNewDivination" text size="small">
                重新开始
              </n-button>
            </div>
          </div>
        </div>
      </n-drawer-content>
    </n-drawer>
  </div>
</template>

<style scoped>
/* 基础布局 */
.button-container {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 20px;
}

.button {
  flex: 1;
  max-width: 120px;
}

/* 结果区域头部 */
.result-header {
  padding: 0;
  margin: 0;
}

.result-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.title-text {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.title-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.result-time {
  font-size: 12px;
  color: #8a8a8a;
  white-space: nowrap;
}

/* 主要内容区域 */
.result-container {
  min-height: 60vh;
  display: flex;
  flex-direction: column;
}

/* 对话历史和消息卡片 */
.conversation-history {
  margin-bottom: 24px;
}

.message-card {
  margin-bottom: 16px;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  overflow: hidden;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.2s ease;
}

.message-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.user-message {
  border-left: 3px solid #2080f0;
  background: linear-gradient(135deg, #f8fbff 0%, #e8f4fd 100%);
}

.ai-message {
  border-left: 3px solid #18a058;
  background: linear-gradient(135deg, #f6ffed 0%, #f0f9e8 100%);
}

.message-header {
  display: flex;
  align-items: center;
  padding: 12px 16px 8px 16px;
  gap: 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  background: rgba(255, 255, 255, 0.7);
}

.message-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}

.message-role {
  font-size: 14px;
  font-weight: 600;
  color: #2c2c2c;
  flex: 1;
}

.message-time {
  font-size: 12px;
  color: #8a8a8a;
}

.message-content {
  padding: 16px;
}

.user-question {
  font-size: 15px;
  line-height: 1.6;
  color: #2c2c2c;
  font-weight: 500;
  padding: 12px 16px;
  background: rgba(32, 128, 240, 0.08);
  border-radius: 8px;
  border-left: 3px solid #2080f0;
}

.ai-response {
  line-height: 1.7;
  color: #2c2c2c;
  font-size: 15px;
}

/* AI回复内容样式优化 */
.ai-response h1, .ai-response h2, .ai-response h3 {
  color: #1a1a1a;
  margin: 16px 0 12px 0;
  font-weight: 600;
}

.ai-response h1 {
  font-size: 18px;
  border-bottom: 2px solid #18a058;
  padding-bottom: 8px;
}

.ai-response h2 {
  font-size: 16px;
  color: #18a058;
}

.ai-response h3 {
  font-size: 15px;
}

.ai-response p {
  margin: 12px 0;
  line-height: 1.8;
}

.ai-response ul, .ai-response ol {
  margin: 12px 0;
  padding-left: 24px;
}

.ai-response li {
  margin: 6px 0;
  line-height: 1.6;
}

.ai-response strong {
  color: #1a1a1a;
  font-weight: 600;
}

.ai-response code {
  background: rgba(24, 160, 88, 0.1);
  color: #18a058;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Monaco', 'Consolas', monospace;
  font-size: 14px;
}

.ai-response blockquote {
  border-left: 4px solid #18a058;
  background: rgba(24, 160, 88, 0.05);
  margin: 16px 0;
  padding: 12px 16px;
  border-radius: 0 8px 8px 0;
}

.current-result {
  margin-bottom: 24px;
}

/* 当前追问回复样式 */
.current-followup-reply {
  margin-bottom: 20px;
  border: 2px solid rgba(24, 160, 88, 0.1);
  border-radius: 16px;
  background: rgba(24, 160, 88, 0.02);
  animation: pulse-border 2s infinite;
}

.current-followup-reply .message-card {
  margin: 0;
  background: transparent;
  border: none;
}

.streaming-indicator {
  font-size: 12px;
  color: #18a058;
  margin-left: 8px;
  animation: pulse-text 1.5s infinite;
}

@keyframes pulse-border {
  0%, 100% {
    border-color: rgba(24, 160, 88, 0.1);
    box-shadow: 0 0 0 0 rgba(24, 160, 88, 0.1);
  }
  50% {
    border-color: rgba(24, 160, 88, 0.2);
    box-shadow: 0 0 0 4px rgba(24, 160, 88, 0.05);
  }
}

@keyframes pulse-text {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 1;
  }
}

/* 交互区域 */
.interaction-area {
  margin-top: auto;
  padding-top: 20px;
}

.section-divider {
  display: flex;
  align-items: center;
  margin: 24px 0 20px 0;
}

.section-divider::before,
.section-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(to right, transparent, #e5e5e5, transparent);
}

.divider-text {
  margin: 0 16px;
  font-size: 13px;
  color: #8a8a8a;
  font-weight: 500;
  white-space: nowrap;
}

/* 追问区域 */
.follow-up-area {
  background: rgba(250, 250, 250, 0.6);
  border-radius: 16px;
  padding: 16px;
  border: 1px solid rgba(0, 0, 0, 0.04);
  backdrop-filter: blur(10px);
}

.follow-up-input {
  margin-bottom: 12px;
}

.follow-up-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.remaining-count {
  font-size: 12px;
  color: #8a8a8a;
  font-weight: 500;
}

/* 追问完成状态 */
.follow-up-finished {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(248, 248, 248, 0.8);
  border-radius: 16px;
  padding: 16px 20px;
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.finished-text {
  font-size: 14px;
  color: #8a8a8a;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .result-title {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .title-meta {
    gap: 8px;
  }
  
  .message-card {
    margin-bottom: 12px;
  }
  
  .message-header {
    padding: 10px 12px 6px 12px;
  }
  
  .message-content {
    padding: 12px;
  }
  
  .user-question {
    padding: 10px 12px;
    font-size: 14px;
  }
  
  .ai-response {
    font-size: 14px;
  }
  
  .ai-response h1 {
    font-size: 16px;
  }
  
  .ai-response h2 {
    font-size: 15px;
  }
  
  .ai-response h3 {
    font-size: 14px;
  }
  
  .follow-up-area {
    padding: 12px;
  }
  
  .follow-up-finished {
    padding: 12px 16px;
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
  
  .tarot-algorithm-notice,
  .plum-flower-disclaimer {
    padding: 8px 12px;
    font-size: 12px;
    margin: 0 0 12px 0;
  }
}

/* 塔罗牌抽牌模式样式 */
.number-selection {
  background: rgba(32, 128, 240, 0.05);
  border-radius: 12px;
  padding: 16px;
  margin: 12px 0;
  border: 1px solid rgba(32, 128, 240, 0.1);
}

.random-mode {
  background: rgba(24, 160, 88, 0.05);
  border-radius: 12px;
  padding: 16px;
  margin: 12px 0;
  border: 1px solid rgba(24, 160, 88, 0.1);
}

/* 算法说明 */
.tarot-algorithm-notice,
.plum-flower-disclaimer {
  display: flex;
  align-items: center;
  background: rgba(24, 160, 88, 0.08);
  border: 1px solid rgba(24, 160, 88, 0.2);
  border-radius: 8px;
  padding: 10px 14px;
  margin: 0 0 16px 0;
  font-size: 13px;
  color: #2c5530;
  font-weight: 500;
}

.plum-flower-disclaimer {
  background: rgba(24, 160, 88, 0.06);
  border: 1px solid rgba(24, 160, 88, 0.15);
  color: #1a4a1d;
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .title-text {
    color: #f0f0f0;
  }
  
  .message-card {
    background: #2c2c2c;
    border-color: rgba(255, 255, 255, 0.1);
  }
  
  .user-message {
    background: linear-gradient(135deg, #1a2332 0%, #233147 100%);
  }
  
  .ai-message {
    background: linear-gradient(135deg, #1a2e1a 0%, #2d472d 100%);
  }
  
  .message-header {
    background: rgba(40, 40, 40, 0.7);
    border-bottom-color: rgba(255, 255, 255, 0.1);
  }
  
  .message-role {
    color: #e0e0e0;
  }
  
  .user-question {
    background: rgba(32, 128, 240, 0.15);
    color: #e0e0e0;
  }
  
  .ai-response {
    color: #e0e0e0;
  }
  
  .ai-response h1, .ai-response h2, .ai-response h3 {
    color: #f0f0f0;
  }
  
  .ai-response strong {
    color: #f0f0f0;
  }
  
  .follow-up-area {
    background: rgba(40, 40, 40, 0.8);
    border-color: rgba(255, 255, 255, 0.08);
  }
  
  .follow-up-finished {
    background: rgba(45, 45, 45, 0.8);
    border-color: rgba(255, 255, 255, 0.08);
  }
  
  .finished-text {
    color: #b0b0b0;
  }
  
  .remaining-count {
    color: #b0b0b0;
  }
  
  .number-selection {
    background: rgba(32, 128, 240, 0.1);
    border-color: rgba(32, 128, 240, 0.2);
  }
  
  .random-mode {
    background: rgba(24, 160, 88, 0.1);
    border-color: rgba(24, 160, 88, 0.2);
  }
  
  .tarot-algorithm-notice,
  .plum-flower-disclaimer {
    background: rgba(24, 160, 88, 0.15);
    border-color: rgba(24, 160, 88, 0.3);
    color: #a8d4a8;
  }
}
</style>