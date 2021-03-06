<template>
  <Basic :items="items">
    <div class="body">
      <div class="head-container">
        <div class="head-title">
          <h1>留言详情</h1>
          <div class="buttons">
            <a
              v-b-modal.reply
              id="reply-button"
              class="btn"
              @click="reply_id=message.comment_id">
              <simple-line-icons
                icon="pencil"
                color="white"
                class="icon"
                size="small"/>
              回复
            </a>
            <a
              v-b-modal.delete
              id="delete-button"
              class="btn">
              <simple-line-icons
                icon="trash"
                color="white"
                class="icon"
                size="small"/>
              删除</a>
          </div>
        </div>
      </div>
      <InputModal
        id="reply"
        title="回复留言"
        placeholder="请输入你要回复的内容"
        @click="reply_message"/>
      <ConfirmModal
        id="delete"
        title="确认删除"
        text="您确定要删除此条留言吗？"
        @click="delete_message"/>
      <Alert
        :count_down="wrong_count_down"
        :instruction="wrong"
        variant="danger"
        @decrease="wrong_count_down-1"
        @zero="wrong_count_down=0"/>
      <Alert
        :count_down="success_count_down"
        :instruction="success"
        variant="success"
        @decrease="success_count_down-1"
        @zero="success_count_down=0"/>
      <DetailTable
        :titles="titles"
        :data="message"/>
    </div>
  </Basic>
</template>

<script>
import ConfirmModal from '../components/confirm_modal'
import InputModal from '../components/input_modal'
import Basic from '../basic/basic'
import DetailTable from '../components/detail_table'
import axios from 'axios'
import qs from 'qs'
import Alert from '../../components/alert'
export default {
  name: 'MessageDetail',
  components: { Alert, DetailTable, Basic, InputModal, ConfirmModal },
  /**
   * @returns {{
   * items: *[], 面包屑路由地址
   * titles: Array, 留言详情标题
   * message: Array, 留言详情数据
   * dismiss_second: number,
   * wrong_count_down: number,
   * wrong: string,
   * success_count_down: number,
   * success: string
   * Alert组件所需参数
   * }}
   */
  data () {
    return {
      items: [
        {
          text: '主页',
          href: '/admin/main'
        },
        {
          text: '留言管理',
          href: '/admin/message'
        },
        {
          text: this.$route.query.message_id,
          active: true
        }
      ],
      titles: [
        '留言日期',
        '用户',
        '课程代码',
        '课程名',
        '点赞数',
        '点踩数',
        '状态',
        '删除日期',
        '内容'
      ],
      message: [],
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: '',
      success_count_down: 0,
      success: ''
    }
  },
  /**
   * 该函数初始化留言详情页面，
   * 通过get方法向后端发送comment_id，表示当前详情页的留言ID，
   * 获取该留言的详细信息，并赋值给message变量，
   * 获取信息失败时，根据返回的错误显示相应的提示信息。
   */
  created () {
    const that = this
    axios
      .get(
        'http://localhost/api/v1/courses/backstage/comment-management/get-comment-detail/',
        {
          params: {
            comment_id: that.$route.query.message_id
          }
        }
      )
      .then(function (response) {
        that.message = that.computed_message(response.data)
      })
      .catch(function (error) {
        if (error.response.data.message === 'Object not found.') {
          that.wrong = '该留言不存在！'
          that.wrong_count_down = that.dismiss_second
        } else {
          that.wrong = '获取留言详情失败！'
          that.wrong_count_down = that.dismiss_second
        }
      })
  },
  methods: {
    /**
     * 该函数刷新订单详情，
     * 获取该留言的详细信息，并赋值给message变量，
     * 捕捉错误并提示信息。
     */
    search: function () {
      const that = this
      axios
        .get(
          'http://localhost/api/v1/courses/backstage/comment-management/get-comment-detail/',
          {
            params: {
              comment_id: that.$route.query.message_id
            }
          }
        )
        .then(function (response) {
          that.message = that.computed_message(response.data)
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.wrong = '该留言不存在！'
            that.wrong_count_down = that.dismiss_second
          } else {
            that.wrong = '获取留言详情失败！'
            that.wrong_count_down = that.dismiss_second
          }
        })
    },
    /**
     * 该函数接收一个boolean类型的参数，
     * 返回一个字符串，表示留言是否被删除。
     * @param deleted
     * @returns {string}
     */
    compute_state: function (deleted) {
      if (deleted) {
        return '已删除'
      } else {
        return '未删除'
      }
    },
    /**
     * 该函数接收一个从后端获取的Object类型的对象，
     * 返回一个包含留言详情信息的有序数组。
     * @param val
     * @returns {any[]}
     */
    computed_message: function (val) {
      let temp = new Array(9)
      temp[0] = (val.created_at + '').slice(0, 10)
      temp[1] = val.username
      temp[2] = val.course_codename
      temp[3] = val.course_title
      temp[4] = val.up_votes
      temp[5] = val.down_votes
      if (val.is_deleted) {
        temp[6] = '已删除'
      } else {
        temp[6] = '未删除'
      }
      if (val.deleted_at === null) {
        temp[7] = '-'
      } else {
        temp[7] = (val.deleted_at + '').slice(0, 10)
      }
      temp[8] = val.content
      return temp
    },
    /**
     * 该函数删除留言，
     * 通过post方法向后端发送表示该留言ID的数据comment_id,
     * 获取后端执行操作后的返回信息，
     * 进行操作成功、失败的提示。
     */
    delete_message: function () {
      const that = this
      axios
        .post(
          'http://localhost/api/v1/courses/backstage/comment-management/delete-comment/',
          qs.stringify({
            comment_id: that.$route.query.message_id
          })
        )
        .then(function (response) {
          if (response.data.message === 'Object deleted.') {
            that.search()
            that.success = '您已经成功删除此留言。'
            that.success_count_down = that.dismiss_second
          }
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.wrong = '你所删除的留言不存在，删除失败！'
            that.wrong_count_down = that.dismiss_second
          } else {
            that.wrong = '删除失败！' + error
            that.wrong_count_down = that.dismiss_second
          }
        })
    },
    /**
     * 该函数回复留言，
     * 接收一个表示留言内容的字符串参数，
     * 通过post方法发送表示留言ID的reply_to_id以及表示回复内容的comment_content，
     * 并根据后端返回的成功或失败信息，显示提示。
     * @param val
     */
    reply_message: function (val) {
      const that = this
      axios
        .post(
          'http://localhost/api/v1/courses/backstage/comment-management/add-comment/',
          qs.stringify({
            reply_to_id: that.$route.query.message_id,
            comment_content: val
          })
        )
        .then(function (response) {
          if (response.data.message === 'Success.') {
            that.success = '您已经成功回复此留言。'
            that.success_count_down = that.dismiss_second
          }
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.wrong = '您所回复留言的课程不存在，回复失败！'
            that.wrong_count_down = that.dismiss_second
          } else if (error.response.data.message === 'Commenting is not allowed.') {
            that.wrong = '该留言不能回复，回复失败！'
            that.wrong_count_down = that.dismiss_second
          } else {
            that.wrong = '回复失败！' + error
            that.wrong_count_down = that.dismiss_second
          }
        })
    }
  }
}
</script>

<style scoped>
.body {
  padding: 20px;
  margin: 70px 20px 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #204269;
  text-align: left;
}

.buttons {
  display: inline-block;
}

.btn {
  margin-left: 3px;
  border: 1px solid #d3d9df;
}

#reply-button {
  color: white;
  background-color: #4db14d;
}

#reply-button:hover,
#reply-button:active {
  background-color: #449c44;
}

#delete-button {
  color: white;
  background-color: #dd514c;
}

#delete-button:hover,
#delete-button:active {
  background-color: #ba2d28;
}

.head-title {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  margin: 25px 0;
}

.head-container {
  padding: 0 15px;
  margin-bottom: 15px;
  text-align: left;
}
</style>
