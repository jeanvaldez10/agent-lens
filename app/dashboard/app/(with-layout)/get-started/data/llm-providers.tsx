import {
  OpenAIIcon,
  AnthropicIcon,
  OllamaIcon,
  LiteLLMIcon,
  GeminiIcon,
  MistralIcon,
  CohereIcon,
  GoogleIcon,
  IBMIcon,
  XAIIcon,
} from '@/components/icons';
import { LLMProvider } from '../types';

export const llmProviders: LLMProvider[] = [
  {
    id: 'openai',
    name: 'OpenAI',
    installCommand: 'pip install agentlens openai',
    icon: <OpenAIIcon className="h-5 w-5" />,
    description: 'o1, o3, o4, GPTs, embeddings and more',
  },
  {
    id: 'anthropic',
    name: 'Anthropic',
    installCommand: 'pip install agentlens anthropic',
    icon: <AnthropicIcon className="h-5 w-5" />,
    description: 'Claude 3 family of models',
  },
  {
    id: 'gemini',
    name: 'Gemini',
    installCommand: 'pip install agentlens google-generativeai',
    icon: <GeminiIcon className="h-5 w-5" />,
    description: 'Google\'s multimodal AI models',
  },
  {
    id: 'ollama',
    name: 'Ollama',
    installCommand: 'pip install agentlens ollama',
    icon: <OllamaIcon className="h-5 w-5" />,
    description: 'Run LLMs locally on your machine',
  },
  {
    id: 'litellm',
    name: 'LiteLLM',
    installCommand: 'pip install agentlens litellm',
    icon: <LiteLLMIcon className="h-5 w-5" />,
    description: 'Universal interface for 100+ LLMs',
  },
  {
    id: 'mistralai',
    name: 'Mistral AI',
    installCommand: 'pip install agentlens mistralai',
    icon: <MistralIcon className="h-5 w-5" />,
    description: 'Open-weight European AI models',
  },
  {
    id: 'cohere',
    name: 'Cohere',
    installCommand: 'pip install agentlens cohere',
    icon: <CohereIcon className="h-5 w-5" />,
    description: 'Enterprise-focused language models',
  },
  {
    id: 'watsonx',
    name: 'IBM Watsonx.ai',
    installCommand: 'pip install agentlens ibm-watson-ai',
    icon: <IBMIcon className="h-5 w-5" />,
    description: 'Enterprise AI platform by IBM',
  },
  {
    id: 'xai',
    name: 'xAI (Grok)',
    installCommand: 'pip install agentlens xai',
    icon: <XAIIcon className="h-5 w-5" />,
    description: 'Advanced AI models by xAI',
  },
];
