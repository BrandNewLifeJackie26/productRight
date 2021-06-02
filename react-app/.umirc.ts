import { defineConfig } from 'umi';

export default defineConfig({
  locale: {
    default: 'en-US',
  },
  nodeModulesTransform: {
    type: 'none',
  },
  routes: [
    { path: '/', component: '@/pages/index' },
    { path: '/asset/placeholder', component: '../assets/placeholder.png' },
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
