import { ref } from "vue";
import {
    createGlobalState, useDark, useToggle, useLocalStorage
} from '@vueuse/core'

export const useGlobalState = createGlobalState(
    () => {
        const isDark = useDark()
        const toggleDark = useToggle(isDark)
        const loading = ref(false);
        const customAISettings = useLocalStorage('customAISettings', {
            enable: false,
            baseUrl: 'https://openrouter.ai/api/v1',
            apiKey: '',
            model: 'anthropic/claude-sonnet-4',
        });
        
        // 追问功能状态管理
        const currentSession = ref({
            sessionId: null,
            followUpCount: 0,
            canFollowUp: true,
            originalDivinationSummary: '',
            conversationHistory: []
        });
        
        const resetSession = () => {
            currentSession.value = {
                sessionId: null,
                followUpCount: 0,
                canFollowUp: true,
                originalDivinationSummary: '',
                conversationHistory: []
            };
        };
        
        const updateSession = (sessionData) => {
            if (sessionData.session_id) {
                currentSession.value.sessionId = sessionData.session_id;
            }
            if (typeof sessionData.follow_up_count !== 'undefined') {
                currentSession.value.followUpCount = sessionData.follow_up_count;
            }
            if (typeof sessionData.can_follow_up !== 'undefined') {
                currentSession.value.canFollowUp = sessionData.can_follow_up;
            }
        };
        
        const addToConversation = (message, isUser = false) => {
            currentSession.value.conversationHistory.push({
                content: message,
                isUser: isUser,
                timestamp: Date.now()
            });
            
            // 保持最近10条对话记录
            if (currentSession.value.conversationHistory.length > 10) {
                currentSession.value.conversationHistory = currentSession.value.conversationHistory.slice(-10);
            }
        };
        
        return {
            isDark,
            toggleDark,
            customAISettings,
            currentSession,
            resetSession,
            updateSession,
            addToConversation
        }
    },
)
