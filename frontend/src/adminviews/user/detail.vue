<template>
  <div>
    <AdminNavbar
      style="min-width: 1000px;"/>
    <div id="body">
      <div>
        <Menu/>
      </div>
      <div id="detail">
        <BreadCrumb :items="items"/>
        <div class="title">
          <h1>用户详情</h1>
          <div class="buttons">
            <button
              type="button"
              class="btn-primary btn-lg"
              style="margin-right: 10px;">
              认证用户
            </button>
            <button
              type="button"
              class="btn-primary btn-lg"
              style="margin-right: 10px;">
              禁言用户
            </button>
            <button
              v-b-modal.delete
              type="button"
              class="btn-primary btn-lg"
              style="margin-right: 10px;">
              删除用户
            </button>
            <b-modal
              id="delete"
              ref="modal"
              title="确认删除"
              centered
              ok-title="确定"
              cancel-title="取消">
              <p id="delete_confirm">您确定要删除此用户吗？</p>
            </b-modal>
          </div>
        </div>
        <div class="table_div">
          <table class="table table-bordered">
            <tbody class="w-100">
              <tr class="row mx-0">
                <td class="col-2">头像</td>
                <td class="col-10">
                  <img :src="user.img">
                </td>
              </tr>
              <tr class="row mx-0">
                <td class="col-2">用户名</td>
                <td class="col-10">{{ user.name }}</td>
              </tr>
              <tr class="row mx-0">
                <td class="col-2">手机号码</td>
                <td class="col-10">{{ user.phone }}</td>
              </tr>
              <tr class="row mx-0">
                <td class="col-2">奖励金</td>
                <td class="col-10">{{ user.balance }}</td>
              </tr>
              <tr class="row mx-0">
                <td class="col-2">注册时间</td>
                <td class="col-10">{{ user.register_time }}</td>
              </tr>
              <tr class="row mx-0">
                <td class="col-2">修改时间</td>
                <td class="col-10">{{ user.change_time }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="title">
          <h2>相关订单</h2>
          <button
            type="button"
            class="btn-primary"
            style="margin-right: 10px;">
            查看更多
          </button>
        </div>
        <div class="table_div">
          <table
            id="order_table"
            class="table table-striped table">
            <thead>
              <tr style="background-color: #6c757d; color: white; font-weight: bold;">
                <td
                  v-for="order_title in order_titles"
                  :key="order_title.id">
                  {{ order_title.label }}
                </td>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="order in orders"
                :key="order.id">
                <td>{{ order.order_code }}</td>
                <td>{{ order.course_code }}</td>
                <td>{{ order.course_name }}</td>
                <td>{{ order.charge }}</td>
                <td>{{ order.state }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="title">
          <h2>相关课程</h2>
          <div class="buttons">
            <button
              type="button"
              class="btn-primary"
              style="margin-right: 10px;">
              查看更多
            </button>
          </div>
        </div>
        <div class="table_div">
          <table
            id="study_table"
            class="table table-striped">
            <thead>
              <tr style="background-color: #6c757d; color: white; font-weight: bold;">
                <td
                  v-for="study_title in study_titles"
                  :key="study_title.id">
                  {{ study_title.label }}
                </td>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="study_log in study_logs"
                :key="study_log.id">
                <td>{{ study_log.course_code }}</td>
                <td>{{ study_log.course_name }}</td>
                <td>{{ study_log.progress }}</td>
                <td>{{ study_log.time }}</td>
                <td>{{ study_log.state }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
export default {
  name: 'UserDetail',
  components: {BreadCrumb, AdminNavbar, Menu},
  data () {
    return {
      user: { img: require('../../assets/logo.png'),
        name: '小红',
        phone: '13102250001',
        balance: '15.00',
        register_time: '2018-01-01',
        change_time: '2018-08-01' },
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '用户管理',
        href: '/admin/user'
      }, {
        text: '用户详情',
        active: true
      }],
      order_titles: [
        { label: '订单编号' },
        { label: '课程代码' },
        { label: '课程名' },
        { label: '金额' },
        { label: '状态' }
      ],
      orders: [
        { order_code: '0001', course_code: 'SOFT1', course_name: '计算机', charge: '110.00', state: '已完成' },
        { order_code: '0010', course_code: 'ENGLISH2', course_name: '口语', charge: '120.00', state: '已退款' }
      ],
      study_titles: [
        { label: '课程代码' },
        { label: '课程名' },
        { label: '学习进度' },
        { label: '最近学习时间' },
        { label: '是否焚毁' }
      ],
      study_logs: [
        { course_code: 'SOFT1', course_name: '计算机', progress: '01:22', time: '2018-08-14', state: '已焚毁' },
        { course_code: 'ENGLISH3', course_name: '英语写作', progress: '15:00', time: '2018-05-14', state: '未焚毁' }
      ]
    }
  }
}
</script>

<style scoped>
  h1,
  h2 {
    padding-left: 15px;
    text-align: left;
  }

  .buttons {
    display: flex;
    justify-content: flex-end;
    text-align: right;
  }

  #body {
    display: flex;
    justify-content: space-between;
    min-width: 1000px;
  }

  #detail {
    flex-basis: 100%;
    padding: 0;
  }

  table {
    font-size: 1.5em;
    text-align: center;
  }

  img {
    width: 40px;
  }

  #delete_confirm {
    text-align: left;
  }

  #order_table,
  #study_table {
    border: 1px solid #d3d9df;
  }

  button {
    margin-right: 7px;
    margin-left: 7px;
    background-color: #0056b3;
    border-color: #0062cc;
    border-radius: 10px;
    outline: none;
    box-shadow: #0062cc inset;
  }

  .title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-right: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
  }

  .table_div {
    padding-right: 15px;
    padding-left: 15px;
  }

  .col-2 {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  .col-10 {
    background-color: rgba(0, 0, 0, 0.05);
  }
</style>