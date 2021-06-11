import { defineConfig } from 'umi';

export default defineConfig({
  locale: {
    default: 'en-US',
  },
  nodeModulesTransform: {
    type: 'none',
  },
  links: [
    { rel: 'icon', href: '@/assets/logo.svg' },
  ],
  routes: [
    { path: '/', component: '@/pages/index' },
  ],
  fastRefresh: {},
  proxy: {
    '/api': {
      'target': 'http://localhost:5000',
      'changeOrigin': true,
      'pathRewrite': {'^/api': ''},
    },
  },
});
