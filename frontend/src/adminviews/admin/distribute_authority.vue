<!--suppress ALL -->
<template>
  <Basic :items="items">
    <div class="my-content">
      <div>
        <h1>分配权限</h1>
        <Alert
          :count_down="wrong_count_down"
          :instruction="error_message"
          variant="danger"
          @decrease="wrong_count_down-1"
          @zero="wrong_count_down=0"/>
        <Alert
          :count_down="success_count_down"
          :instruction="error_message"
          variant="success"
          @decrease="success_count_down-1"
          @zero="success_count_down=0"/>
        <h5 class="my-text">管理员账号：{{ admin_id }}</h5>
        <div>
          <h5 class="my-text">权限选择：</h5>
          <b-form-group class="my-form-group">
            <b-form-checkbox
              v-model="all_selected"
              aria-controls="flavours"
              @change="toggle_all"
            >
              <h5>{{ all_selected ? '取消全选' : '全选' }}</h5>
            </b-form-checkbox>
            <b-form-checkbox-group
              id="flavors"
              v-model="selected"
              :options="flavours"
              stacked
              size="lg"
              name="flavs"
              class="ml-4"
              aria-label="Individual flavours"
            />
            <a
              id="save-btn"
              class="btn"
              @click="submit_message">
              保存
            </a>
          </b-form-group>
        </div>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import axios from 'axios'
import qs from 'qs'
import Alert from '../../components/alert'
export default {
  name: 'DistributeAuthority',
  components: { Alert, Basic },
  /**
   * @returns {{
   * items: *[], 路由跳转信息
   * admin_id: string, 用户ID信息
   * flavours: string[], 权限组信息
   * selected: Array, 用户勾选权限信息
   * error_message: string, 错误信息
   * wrong_count_down: number, 错误信息提示时间
   * success_count_down: number, 正确信息提示时间
   * all_selected: boolean, 全选标记器
   * test_router: boolean 跳转测试器
   * }}
   */
  data: function () {
    return {
      items: [
        {
          text: '主页',
          href: '/admin/main'
        },
        {
          text: '管理员管理',
          href: '/admin/adminmanagement'
        },
        {
          text: this.$route.query.admin_id.toString(),
          href:
            '/admin/adminmanagement/detail?admin_id=' +
            this.$route.query.admin_id.toString()
        },
        {
          text: '分配权限',
          active: true
        }
      ],
      admin_id: '',
      flavours: [
        '课程管理权限',
        '留言管理权限',
        '用户管理权限',
        '订单管理权限',
        '日志管理权限'
      ],
      selected: [],
      error_message: '',
      wrong_count_down: 0,
      success_count_down: 0,
      all_selected: false,
      test_router: false
    }
  },
  /**
   * 监测函数 selected
   * 检测每次用户勾选变化，涉及与全选按钮是否勾选的逻辑交互
   */
  watch: {
    selected () {
      if (
        this.all_selected === true &&
        this.selected.length !== this.flavours.length
      ) {
        this.all_selected = false
      }
      if (
        this.all_selected === false &&
        this.selected.length === this.flavours.length
      ) {
        this.all_selected = true
      }
    }
  },
  /**
   * 渲染函数
   * 发送请求，发送用户ID信息
   * 得到回复，对当前用户权限信息进行保存和显示
   * 得到错误，显示五秒经转换函数输出的错误信息
   */
  mounted () {
    this.admin_id = this.$route.query.admin_id
    axios
      .get(
        'http://localhost/api/v1/admin/backstage/admin-management/get-admin-detail/',
        {
          params: {
            admin_id: this.admin_id
          }
        }
      )
      .then(response => {
        for (let permission of response.data.admin_groups) {
          if (permission === 'super_admin') {
            this.toggle_all(true)
            break
          }
          this.selected.push(this.transfer_permission(permission))
        }
      })
      .catch(error => {
        this.wrong_count_down = 0
        this.success_count_down = 0
        this.error_message = this.init_error_message(error.response.data.message)
        this.wrong_count_down = 5
      })
  },
  methods: {
    /**
     * 全选函数
     * @param checked
     */
    toggle_all (checked) {
      this.selected = checked ? this.flavours.slice() : []
    },
    /**
     * 接收权限信息转换函数
     * @param permission
     * @returns {string}
     */
    transfer_permission (permission) {
      switch (permission) {
        case 'comment_admin':
          return '留言管理权限'
        case 'course_admin':
          return '课程管理权限'
        case 'customer_admin':
          return '用户管理权限'
        case 'log_admin':
          return '日志管理权限'
        case 'order_admin':
          return '订单管理权限'
      }
    },
    /**
     * 发送权限信息转换函数
     * @param sel
     * @returns {string}
     */
    reverse_permission (sel) {
      switch (sel) {
        case '留言管理权限':
          return 'comment_admin'
        case '课程管理权限':
          return 'course_admin'
        case '用户管理权限':
          return 'customer_admin'
        case '日志管理权限':
          return 'log_admin'
        case '订单管理权限':
          return 'order_admin'
      }
    },
    /**
     * 发送信息函数
     * 发送经选择后的当前用户权限信息
     * 得到回应，显示之后成功信息，执行路由跳转函数
     * 得到错误，显示五秒错误信息
     */
    submit_message () {
      let adminGroups = []
      for (let sel of this.selected) {
        adminGroups.push(this.reverse_permission(sel))
      }
      axios
        .post(
          'http://localhost/api/v1/admin/backstage/admin-management/change-admin-groups/',
          qs.stringify(
            {
              new_admin_groups: adminGroups,
              admin_id: this.admin_id
            },
            { arrayFormat: 'repeat' }
          )
        )
        .then(response => {
          this.wrong_count_down = 0
          this.success_count_down = 0
          this.error_message = '分配权限成功'
          this.success_count_down = 3
          this.router_push()
        })
        .catch(error => {
          this.wrong_count_down = 0
          this.success_count_down = 0
          this.error_message = this.init_error_message(error.response.data.message)
          this.wrong_count_down = 5
        })
    },
    /**
     * 错误信息生成函数
     * @param message
     * @returns {string}
     */
    init_error_message (message) {
      switch (message) {
        case 'Access denied.':
          return '用户无权限，拒绝访问'
        case 'Object not found.':
          return '查询的对象不存在'
        default:
          return '数据库查询出错'
      }
    },
    /**
     * 路由跳转函数
     */
    router_push () {
      this.$router.push({
        name: 'AdminDetail',
        query: { admin_id: this.$route.query.admin_id }
      })
    }
  }
}
</script>

<style scoped>
.my-content {
  padding: 20px;
  margin: 70px 20px 20px;
  text-align: left;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  margin: 25px 15px;
  color: #204269;
  text-align: left;
}

.my-form-group {
  margin-top: 40px;
  margin-left: 15px;
}

.my-text {
  margin-top: 50px;
  margin-left: 15px;
}

#save-btn {
  color: white;
}

.btn {
  margin-top: 250px;
  margin-right: 3px;
  margin-left: 3px;
  color: white;
  text-align: right;
  background-color: #4db14d;
  border: 1px solid #d3d9df;
}

.btn:hover,
.btn:active {
  background-color: #449c44;
}
</style>
