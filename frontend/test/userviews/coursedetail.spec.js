/* eslint-disable no-undef */

import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import CourseDetail from '@/userviews/coursedetail/index'
import Basic from '@/userviews/components/basic'
import {shallowMount} from '@vue/test-utils'
import Vuex from 'vuex'
Vue.use(Vuex)

Vue.use(BootstrapVue)

const $route = {
  path: '/coursedetail',
  query: {
    course_id: 1,
    page: 1
  }
}

const $store = new Vuex.Store({
  state: {
    status: true,
    user: {
      is_new_customer: null,
      customer_id: '',
      username: '',
      avatar: null
    },
    phone: '',
    money: '',
    time: ''
  }
})

describe('课程详情页单元测试', () => {
  const wrapper = shallowMount(CourseDetail, {
    mocks: {
      $route,
      $store
    }
  })

  it('标题是课程名称', () => {
    expect(wrapper.contains('.content-style')).toBe(true)
  })

  it('包含导航栏', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('测试按钮数量', () => {
    expect(wrapper.findAll('.my-btn').length).toEqual(4)
  })

  it('测试提示数量', () => {
    expect(wrapper.findAll('.reminder').length).toEqual(1)
  })

  it('测试课程简介渲染', () => {
    expect(wrapper.contains('.profile-style')).toBe(true)
  })

  it('点击按钮课程点赞数增加', () => {
    wrapper.find('#praise-button').trigger('click')
    expect(wrapper.vm.course.num_of_praise).toBe(wrapper.vm.course.num_of_praise)
  })

  it('点击分享按钮弹出模态框', () => {
    wrapper.find('#share-button').trigger('click')
    expect(wrapper.contains('#share-popup')).toBe(true)
  })

  it('点击分享按钮弹出模态框', () => {
    wrapper.find('#study-button').trigger('click')
    expect(wrapper.contains('#study-popup')).toBe(true)
  })

  it('课程简介渲染', () => {
    expect(wrapper.contains('#introduction')).toBe(true)
  })

  it('点击分享按钮弹出模态框', () => {
    wrapper.find('#pay-button').trigger('click')
    expect(wrapper.contains('#pay-popup')).toBe(true)
  })
})
