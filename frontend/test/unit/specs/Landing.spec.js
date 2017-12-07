import Vue from 'vue';
import LandingPage from '@/components/Landing';

describe('Landing.vue', () => {
  it('should render correct contents', () => {
    const Constructor = Vue.extend(LandingPage);
    const vm = new Constructor().$mount();
    expect(vm.$el.querySelector('.hello h1').textContent)
      .to.equal('The Daily Bark');
  });
});
