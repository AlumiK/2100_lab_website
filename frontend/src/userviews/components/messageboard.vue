<template>
  <div id="message-board">
    <Alert
      :count_down="success_count_down"
      :instruction="success"
      variant="success"
      @decrease="success_count_down-1"
      @zero="success_count_down=0"/>
    <div class="text-align-left">
      {{ rows }}
      <simple-line-icons
        icon="bubble"
        size="small"
        color="#009966"/>
    </div>
    <InputModal
      id="reply-popup"
      :input="new_reply"
      ok_title="回复"
      title="回复留言"
      placeholder="请输入你要回复的内容"
      @click="reply_comment"/>
    <div>
      <b-modal
        id="reply-list-popup"
        hide-footer
        title="全部回复">
        <div
          v-for="i in replies.length"
          :key="i"
          class="modal-reply-message">
          <div>
            <div class="modal-each-message">
              <div class="row1">
                <div class="row2">
                  <div class="row3">
                    {{ replies[i-1].username }}
                    <label
                      v-if="replies[i-1].user_is_vip === true"
                      class="vip-style">
                      V
                    </label>
                  </div>
                  <div class="comment-wrap">
                    {{ replies[i-1].content }}
                  </div>
                </div>
                <div
                  v-if="replies[i-1].username ===
                  $store.state.user.username"
                  class="delete-comment"
                  @click="delete_list_comment(i-1,replies[i-1].comment_id)">
                  删除</div>
              </div>
              <div class="modal-zone">
                <label class="time-style">
                  {{ get_date(replies[i-1].created_at).substring(0,10) }}
                </label>
                <div>
                  {{ replies[i-1].up_votes }}
                  <b-img
                    id="vote-up"
                    :src="replies[i-1].up_voted === true ? up_icon_after :
                    up_icon_before"
                    class="vote-style "
                    @click="modal_up_vote_reply
                  (i-1, replies[i-1].comment_id)"/>
                  {{ replies[i-1].down_votes }}
                  <b-img
                    :src="replies[i-1].down_voted === true ? down_icon_after
                    : down_icon_before"
                    class="vote-style "
                    @click="modal_down_vote_reply
                  (i-1, replies[i-1].comment_id)"/>
                </div>
              </div>
              <hr>
            </div>
          </div>
        </div>
        <b-pagination
          id="popup-pagination"
          :total-rows="modal_rows"
          :per-page="modal_page_limit"
          v-model="modal_page"
          align="center"
          size="sm"
          @input="get_replies(get_all_reply_id)"/>
      </b-modal>
    </div>
    <div v-if="!can_comment">该课程已禁止评论！</div>
    <div v-if="can_comment">
      <b-alert
        :show="created_test"
        variant="danger"
        dismissible
        fade
        @dismissed="created_test=false">
        {{ created_error_msg }}
      </b-alert>
      <b-alert
        :show="get_all_message_test"
        variant="danger"
        dismissible
        fade
        @dismissed="get_all_message_test=false">
        {{ get_all_message_error_msg }}
      </b-alert>
      <b-alert
        :show="up_vote_test"
        variant="danger"
        dismissible
        fade
        @dismissed="up_vote_test=false">
        {{ up_vote_error_msg }}
      </b-alert>
      <b-alert
        :show="down_vote_test"
        variant="danger"
        dismissible
        fade
        @dismissed="down_vote_test=false">
        {{ down_vote_error_msg }}
      </b-alert>
      <b-alert
        :show="delete_message_test"
        variant="danger"
        dismissible
        fade
        @dismissed="delete_message_test=false">
        {{ delete_message_error_msg }}
      </b-alert>
      <b-alert
        :show="add_message_test"
        variant="danger"
        dismissible
        fade
        @dismissed="add_message_test=false">
        {{ add_message_error_msg }}
      </b-alert>
      <div
        class="comment-style" >
        <div class="user-avatar">
          <img
            :src="$store.state.address + this.$store.state.user.avatar"
            class="userimg">
        </div>
        <div class="message-area">
          <textarea
            id="input-message"
            v-model="new_msg"
            class="textarea-style"
            placeholder="请输入留言"
            @keyup.enter="add_comment"/>
          <div
            id="commit-button"
            class="commit-button-style">
            <b-button
              class="add_comment"
              @click="add_comment">发表<br>评论</b-button>
          </div>
        </div>
      </div>
      <div
        v-for="index in message_list.length"
        id="piece-of-message"
        :key="index"
        class="piece-of-message">
        <div class="user-avatar">
          <img
            :src="$store.state.address + message_list[index-1].avatar"
            class="userimg">
        </div>
        <div class="message-list-area">
          <div class="message-username">
            <div class="message-list-username">
              {{ message_list[index-1].username }}
              <label
                v-if="message_list[index-1].user_is_vip === true"
                class="vip-style">
                V
              </label>
            </div>
            <div
              v-if="message_list[index-1].username ===
              $store.state.user.username"
              id="delete-button"
              class="delete-comment"
              @click="delete_comment(message_list[index-1].comment_id)">
              删除</div>
          </div>
          <div
            id="comment"
            class="comment-wrap">{{ message_list[index-1].content }}
          </div>
          <div class="time-remind">
            <div
              class="time-style">
              {{ get_date(message_list[index-1].created_at) }}
              <span
                id="reply-button"
                @click="want_reply(message_list[index-1].comment_id)">
                回复
              </span>
            </div>
            <div class="margin-right-1">
              {{ message_list[index-1].up_votes }}
              <b-img
                id="praise-button"
                :src="message_list[index-1].up_voted === true ?
                up_icon_after : up_icon_before"
                class="vote-style"
                @click="up_vote(index-1,message_list[index-1].comment_id)"/>
              {{ message_list[index-1].down_votes }}
              <b-img
                id="detest-button"
                :src="message_list[index-1].down_voted === true ?
                down_icon_after : down_icon_before"
                class="vote-style "
                @click="down_vote
              (index-1,message_list[index-1].comment_id)"/>
            </div>
          </div>
          <div
            v-if="message_list [index-1].reply_count !== 0"
            class="all-reply">
            <div class="margin-right-1">
              共{{ message_list [index-1].reply_count }}条回复
            </div>
            <div
              id="watch-more"
              class="look-all"
              @click="watch_all_replies(message_list[index-1].comment_id)">
              点击查看
            </div>
          </div>
          <div
            v-for="i in message_list[index-1].replies.length"
            :key="i"
            class="reply-message">
            <div>
              <div>
                <div class="row1">
                  <div class="row2">
                    <div class="row3">
                      {{ message_list[index-1].replies[i-1].username }}
                      <label
                        v-if="message_list[index-1].replies[i-1].user_is_vip
                        === true"
                        class="vip-style">
                        V
                      </label>
                    </div>
                    <div class="comment-wrap">{{ message_list[index-1].
                    replies[i-1].content }}</div>
                  </div>
                  <div
                    v-if="message_list[index-1].replies[i-1].username ===
                    $store.state.user.username"
                    class="delete-comment"
                    @click="delete_comment(message_list[index-1].replies[i-1]
                    .comment_id)">删除</div>
                </div>
                <div class="zone">
                  <label class="time-style">
                    {{ get_date(message_list[index-1].replies[i-1].created_at) }}
                  </label>
                  <div>
                    {{ message_list[index-1].replies[i-1].up_votes }}
                    <b-img
                      id="vote-up"
                      :src="message_list[index-1].replies[i-1].up_voted ===
                      true ? up_icon_after : up_icon_before"
                      class="vote-style "
                      @click="up_vote_child_reply(index-1, i-1,
                                                  message_list[index-1].replies[i-1].comment_id)"/>
                    {{ message_list[index-1].replies[i-1].down_votes }}
                    <b-img
                      :src="message_list[index-1].replies[i-1].down_voted
                      === true ? down_icon_after : down_icon_before"
                      class="vote-style "
                      @click="down_vote_child_reply(index-1, i-1,
                                                    message_list[index-1].replies[i-1].comment_id)"/>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div>
        <Pagination
          id="pagination"
          :rows="rows"
          :perpage="page_limit"
          @change="change_page"/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import qs from 'qs'
import Pagination from '../../components/pagination'
import Alert from '../../components/alert'
import InputModal from '../../adminviews/components/input_modal'

export default {
  name: 'MessageBoard',
  components: {
    InputModal,
    Alert,
    Pagination
  },
  props: {
    course_id: {
      type: Number,
      default: 0
    }
  },
  /**
   * @return {
   *     username:string,用户名
   *     new_msg:string,添加的留言
   *     message_list:array,全端留言列表
   *     created_tet: boolean,判断是否正确访问API
   *     created_error_msg: string,访问API如错误返回的信息
   *     get_all_message_test: boolean,判断是否正确访问留言列表API
   *     get_all_message_error_msg: string，访问API如错误返回的信息
   *     up_vote_test: boolean,判断点赞是否正确访问API
   *     up_vote_error_msg: string，访问API如错误返回的信息
   *     down_vote_test: boolean，判断点踩是否正确访问API
   *     down_vote_error_msg: string，访问API如错误返回的信息
   *     add_message_test: boolean，判断添加留言是否正确访问API
   *     add_message_error_msg: string，访问API如错误返回的信息
   *     delete_message_test: boolean，判断删除留言是否正确访问API
   *     delete_message_error_msg: string，访问API如错误返回的信息
   *     page_limit: number，每页留言的条数
   *     page: number,当前留言板的页码值
   *     rows: number,当前留言板留言的总条数
   *     modal_page_limit: number，留言子楼全部留言
   *     modal_page: number,留言子楼当前的页码
   *     modal_rows: number,子楼总留言数,
   *     up_icon_before: string,点赞按钮的点赞前样式
   *     up_icon_after: string,点赞按钮的点赞后的样式
   *     down_icon_before: string，点踩按钮的点踩前的样式
   *     down_icon_after: string，点踩按钮的点踩后的样式,
   *     can_comment: boolean,当前课程是否可以评论
   *     reply_comment_id: number,当前渲染留言回复的留言ID
   *     new_reply: string,新添加的留言
   *     child_reply_num: number,子楼回复的数量
   *     get_all_reply_id: number,查询所有回复的留言的ID
   *     replies: array,查询所有回复的留言数组
   *     dismiss_second: number,提示框自动消失的时间
   *     success_count_down: number,成功关闭的时间
   *     success: string，成功的提示信息
   * } */
  data () {
    return {
      username: '小可爱',
      new_msg: '',
      message_list: [],
      created_test: false,
      created_error_msg: '',
      get_all_message_test: false,
      get_all_message_error_msg: '',
      up_vote_test: false,
      up_vote_error_msg: '',
      down_vote_test: false,
      down_vote_error_msg: '',
      add_message_test: false,
      add_message_error_msg: '',
      delete_message_test: false,
      delete_message_error_msg: '',
      page_limit: 5,
      page: 1,
      rows: 0,
      modal_page_limit: 5,
      modal_page: 1,
      modal_rows: 0,
      up_icon_before: require('../../assets/up-before.png'),
      up_icon_after: require('../../assets/up-after.png'),
      down_icon_before: require('../../assets/down-before.png'),
      down_icon_after: require('../../assets/down-after.png'),
      can_comment: true,
      reply_comment_id: 0,
      new_reply: '',
      child_reply_num: 0,
      get_all_reply_id: 0,
      replies: [],
      dismiss_second: 5,
      success_count_down: 0,
      success: ''
    }
  },
  created: function () {
    this.page = this.$route.query.page
    this.get_all_message()
  },
  methods: {
    /**
     * 工具函数
     * 将从数据库中读取的数据
     * 转换成本地时间以及标准形式 */
    get_date: function (date) {
      let temp = new Date(date)
      return temp.toLocaleString()
    },
    /**
     * 子组件传值
     * 接受分页器子组件的页码值
     * 将该页面的页码信息设置为分页器的当前指向的页码 */
    change_list_page: function (page) {
      let that = this
      that.modal_page = page
      that.get_replies(that.get_all_reply_id)
    },
    /**
     * 关闭回复留言列表的弹框
     */
    hide_reply_list_popup: function () {
      this.$root.$emit('bv::hide::modal', 'reply-list-popup')
    },
    /**
     * 关闭回复留言的弹框
     */
    hide_reply_popup: function () {
      this.$root.$emit('bv::hide::modal', 'reply-popup')
    },
    /**
     * 打开回复留言的弹框
     * 接收所回复留言的ID
     */
    want_reply: function (Id) {
      this.reply_comment_id = Id
      this.$root.$emit('bv::show::modal', 'reply-popup')
    },
    /**
     * 访问后端api
     * 获取全部留言
     * 发送课程ID、每页展示留言条数、当前页码
     * 获得总留言条数、总留言里列表、当前课程是否可评论
     */
    get_all_message: function () {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play/' +
            'get-course-comments/',
          {
            params: {
              course_id: that.course_id,
              page_limit: that.page_limit,
              page: that.page
            }
          }
        )
        .then(function (response) {
          that.rows = response.data.count
          that.message_list = response.data.content
          that.can_comment = true
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.get_all_message_test = true
            that.get_all_message_error_msg = that.$t('error.object_not_found')
          } else if (
            error.response.data.message === 'Commenting is not allowed.'
          ) {
            that.can_comment = false
          }
        })
    },
    /**
     * 给留言点赞
     * 传入前端留言列表访问留言的索引值
     * 传入当前留言的ID
     * 如访问成功且未点赞，则点赞数加1
     * 如访问成功且已点赞，则点赞数减1
     * 如没有点赞和点踩权限，则提示错误信息
     * */
    up_vote: function (index, Id) {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play/' +
            'up-vote-comment?' +
            'comment_id=' +
            Id
        )
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.object_not_found')
          } else if (response.data.message === 'Access denied.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.access_denied')
          } else if (response.data.up_voted === true) {
            that.message_list[index].up_votes = response.data.up_votes
            that.message_list[index].up_voted = true
          } else if (response.data.up_voted === false) {
            that.message_list[index].up_votes = response.data.up_votes
            that.message_list[index].up_voted = false
          }
        })
        .catch(function (error) {
          that.up_vote_test = true
          that.up_vote_error_msg = error.response.data.message
        })
    },
    /**
     * 给子楼回复点赞
     * 传入前端留言列表访问留言的索引值
     * 传入当前留言的ID
     * 传入当前留言的回复ID
     * 如访问成功且未点赞，则点赞数加1
     * 如访问成功且已点赞，则点赞数减1
     * 如没有点赞和点踩权限，则提示错误信息
     * */
    up_vote_child_reply: function (index, reply_index, Id) {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play' +
            '/up-vote-comment?' +
            'comment_id=' +
            Id
        )
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.object_not_found')
          } else if (response.data.message === 'Access denied.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.access_denied')
          } else if (response.data.up_voted === true) {
            that.message_list[index].replies[reply_index].up_votes =
              response.data.up_votes
            that.message_list[index].replies[reply_index].up_voted = true
          } else if (response.data.up_voted === false) {
            that.message_list[index].replies[reply_index].up_votes =
              response.data.up_votes
            that.message_list[index].replies[reply_index].up_voted = false
          }
        })
        .catch(function (error) {
          that.up_vote_test = true
          that.up_vote_error_msg = error.response.data.message
        })
    },
    /**
     * 给模态框中子楼回复点赞
     * 传入留言所有回复列表中当前回复的索引
     * 传入当前留言的ID
     * 如访问成功且未点赞，则点赞数加1
     * 如访问成功且已点赞，则点赞数减1
     * 如没有点赞和点踩权限，则提示错误信息
     * */
    modal_up_vote_reply: function (reply_index, Id) {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play/' +
            'up-vote-comment?' +
            'comment_id=' +
            Id
        )
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.object_not_found')
          } else if (response.data.message === 'Access denied.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.access_denied')
          } else if (response.data.up_voted === true) {
            that.replies[reply_index].up_votes = response.data.up_votes
            that.replies[reply_index].up_voted = true
          } else if (response.data.up_voted === false) {
            that.replies[reply_index].up_votes = response.data.up_votes
            that.replies[reply_index].up_voted = false
          }
        })
        .catch(function (error) {
          that.up_vote_test = true
          that.up_vote_error_msg = error.response.data.message
        })
    },
    /**
     * 给留言点踩
     * 传入前端留言列表访问留言的索引值
     * 传入当前留言的ID
     * 如访问成功且未点踩，则点踩数加1
     * 如访问成功且已点踩，则点踩数减1
     * 如没有点赞和点踩权限，则提示错误信息
     * */
    down_vote: function (index, Id) {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play/' +
            'down-vote-comment?' +
            'comment_id=' +
            Id
        )
        .then(function (response) {
          if (response.data.down_voted === true) {
            that.message_list[index].down_votes = response.data.down_votes
            that.message_list[index].down_voted = true
          } else if (response.data.down_voted === false) {
            that.message_list[index].down_votes = response.data.down_votes
            that.message_list[index].down_voted = false
          }
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.down_vote_test = true
            that.down_vote_error_msg = that.$t('error.object_not_found')
          } else if (error.response.data.message === 'Access denied.') {
            that.down_vote_test = true
            that.down_vote_error_msg = that.$t('error.access_denied')
          }
        })
    },
    /**
     * 给子楼回复点踩
     * 传入前端留言列表访问留言的索引值
     * 传入当前留言的ID
     * 传入当前留言的回复ID
     * 如访问成功且未点踩，则点踩数加1
     * 如访问成功且已点踩，则点踩数减1
     * 如没有点赞和点踩权限，则提示错误信息
     * */
    down_vote_child_reply: function (index, reply_index, msgCommentId) {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play/' +
            'down-vote-comment?' +
            'comment_id=' +
            msgCommentId
        )
        .then(function (response) {
          if (response.data.down_voted === true) {
            that.message_list[index].replies[reply_index].down_votes =
              response.data.down_votes
            that.message_list[index].replies[reply_index].down_voted = true
          } else if (response.data.down_voted === false) {
            that.message_list[index].replies[reply_index].down_votes =
              response.data.down_votes
            that.message_list[index].replies[reply_index].down_voted = false
          }
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.down_vote_test = true
            that.down_vote_error_msg = that.$t('error.object_not_found')
          } else if (error.response.data.message === 'Access denied.') {
            that.down_vote_test = true
            that.down_vote_error_msg = that.$t('error.access_denied')
          }
        })
    },
    /**
     * 给模态框中子楼回复点踩
     * 传入留言所有回复列表中当前回复的索引
     * 传入当前留言的ID
     * 如访问成功且未点踩，则点踩数加1
     * 如访问成功且已点踩，则点踩数减1
     * 如没有点赞和点踩权限，则提示错误信息
     * */
    modal_down_vote_reply: function (reply_index, msgCommentId) {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play/' +
            'down-vote-comment?' +
            'comment_id=' +
            msgCommentId
        )
        .then(function (response) {
          if (response.data.down_voted === true) {
            that.replies[reply_index].down_votes = response.data.down_votes
            that.replies[reply_index].down_voted = true
          } else if (response.data.down_voted === false) {
            that.replies[reply_index].down_votes = response.data.down_votes
            that.replies[reply_index].down_voted = false
          }
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.down_vote_test = true
            that.down_vote_error_msg = that.$t('error.object_not_found')
          } else if (error.response.data.message === 'Access denied.') {
            that.down_vote_test = true
            that.down_vote_error_msg = that.$t('error.access_denied')
          }
        })
    },
    /**
     * 查看当前留言所有回复
     * 传入留言ID
     * 调用获取全部回复的API
     * 并弹出显示当前留言的所有回复的模态框 */
    watch_all_replies: function (commentId) {
      this.get_all_reply_id = commentId
      this.get_replies(commentId)
      this.$root.$emit('bv::show::modal', 'reply-list-popup')
    },
    /**
     * 获取全部留言
     * 传入留言ID
     * 向后端发送留言ID、每页显示留言数目、模态框中留言列表的当前页码
     * 接受到当前留言当前页码的回复
     * 接受到回复的总条数
     * */
    get_replies: function (commentId) {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play/' + 'get-replies/',
          {
            params: {
              comment_id: commentId,
              page_limit: that.modal_page_limit,
              page: that.modal_page
            }
          }
        )
        .then(function (response) {
          that.replies = response.data.content
          that.modal_rows = response.data.count
        })
    },
    /**
     * 删除留言
     * 接收留言ID，并发送给后端
     * 发送成功将删除该留言
     * 发送失败将提示失败原因
     * */
    delete_comment: function (commentId) {
      let that = this
      axios
        .post(
          'http://localhost/api/v1/courses/forestage/play' + '/delete-comment/',
          qs.stringify({
            comment_id: commentId
          })
        )
        .then(function (response) {
          if (response.data.message === 'Object deleted.') {
            that.get_all_message()
            that.success = that.$t('prompt.object_deleted')
            that.success_count_down = that.dismiss_second
          }
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.delete_message_test = true
            that.delete_message_error_msg = that.$t('error.object_not_found')
          } else if (error.response.data.message === 'Access denied.') {
            that.delete_message_test = true
            that.delete_message_error_msg = that.$t('error.access_denied')
          }
        })
    },
    /**
     * 删除模态框子楼的留言回复
     * 接收在本地回复数组的索引值
     * 接收留言的ID
     * 向后端发送数据
     * 如发送成功，将删除该留言的该条回复
     * 如发送失败，将提示错误信息
     * */
    delete_list_comment: function (index, commentId) {
      let that = this
      axios
        .post(
          'http://localhost/api/v1/courses/forestage/play' + '/delete-comment/',
          qs.stringify({
            comment_id: commentId
          })
        )
        .then(function (response) {
          if (response.data.message === 'Object deleted.') {
            that.replies.splice(index, 1)
            that.get_replies(that.get_all_reply_id)
            that.get_all_message()
            that.success = that.$t('prompt.object_deleted')
            that.success_count_down = that.dismiss_second
          }
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.delete_message_test = true
            that.delete_message_error_msg = that.$t('error.object_not_found')
          } else if (error.response.data.message === 'Access denied.') {
            that.delete_message_test = true
            that.delete_message_error_msg = that.$t('error.access_denied')
          }
        })
    },
    /**
     * 添加留言
     * 通过绑定留言内容并向后端发送
     * 发送成功将在留言列表中添加新评论的内容
     * 发送失败将提示失败信息 */
    add_comment: function () {
      let that = this
      const value = that.new_msg && that.new_msg.trim()
      if (!value) {
        return
      }
      axios
        .post(
          'http://localhost/api/v1/courses/forestage/play/add-comment/',
          qs.stringify({
            content: value,
            course_id: that.course_id
          })
        )
        .then(function (response) {
          if (response.data.message === 'Success.') {
            that.get_all_message()
          }
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.add_message_test = true
            that.add_message_error_msg = that.$t('error.object_not_found')
          } else if (error.response.data.message === 'Access denied.') {
            that.add_message_test = true
            that.add_message_error_msg = that.$t('error.access_denied')
          } else if (
            error.response.data.message === 'Commenting is not allowed.'
          ) {
            that.add_message_test = true
            that.add_message_error_msg = that.$t(
              'prompt.user_comment_not_allowed'
            )
          }
        })
      that.new_msg = ''
    },
    /**
     * 回复评论
     * 接收留言内容
     * 向后端发送回复内容、课程ID、留言ID
     * 如发送成功将回复内容添加到留言的回复列表
     * 如发送失败将提示失败信息 */
    reply_comment: function (val) {
      let that = this
      if (!val) {
        return
      }
      if (that.reply_comment_id !== 0) {
        axios
          .post(
            'http://localhost/api/v1/courses/forestage/play/add-comment/',
            qs.stringify({
              content: val,
              course_id: that.course_id,
              reply_to_id: that.reply_comment_id
            })
          )
          .then(function (response) {
            if (response.data.message === 'Success.') {
              that.get_all_message()
            }
          })
          .catch(function (error) {
            if (error.response.data.message === 'Object not found.') {
              that.add_message_test = true
              that.add_message_error_msg = that.$t('error.object_not_found')
            } else if (error.response.data.message === 'Access denied.') {
              that.add_message_test = true
              that.add_message_error_msg = that.$t('error.access_denied')
            } else if (
              error.response.data.message === 'Commenting is not allowed.'
            ) {
              that.add_message_test = true
              that.add_message_error_msg = that.$t(
                'prompt.user_comment_not_allowed'
              )
            }
          })
      }
      that.$root.$emit('bv::hide::modal', 'reply-popup')
    },
    /**
     * 改变页码
     * @params page 分页器当前页码
     * 发送给父组件该分页组件的页码值
     * 传入函数：change_page
     * */
    change_page: function (page) {
      this.page = page
      this.get_all_message()
    }
  }
}
</script>

<style scoped>
.zone {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.comment-wrap {
  text-indent: 2rem;
  word-break: break-word;
}

.time-style {
  padding-top: 3px;
  margin: 0;
  font-size: 14px;
  color: #adb5bd;
}

.time-remind {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.reply-message {
  padding: 1rem 0 0 3rem;
}

.textarea-style {
  width: 93%;
  height: 70%;
  padding: 0;
  resize: none;
  border: solid 2px #ddd;
}

.textarea-style:focus {
  border: solid 2px #cce5ff;
}

.commit-button-style {
  width: 8%;
  height: 70%;
  text-align: right;
}

.all-reply {
  display: flex;
  flex-direction: row;
  font-size: 14px;
}

.look-all {
  color: #096;
  cursor: pointer;
}

.row1 {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.row2 {
  display: flex;
  flex-direction: row;
}

.row3 {
  font-size: 14px;
  font-weight: bold;
  color: #999;
}

.text-align-left {
  text-align: left;
}

.message-area {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 90%;
  height: 100%;
  border-bottom: 1px solid #eee;
}

.message-list-area {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  width: 90%;
  height: 100%;
  padding-bottom: 8px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.comment-style {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  height: 6rem;
  margin: 1rem 0.5rem 1rem 0;
}

.piece-of-message {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  height: auto;
  margin: 1rem 0.5rem 1rem 0;
}

.user-avatar {
  width: 10%;
  padding-top: 0.3rem;
  vertical-align: center;
}

.vote-style {
  width: 15px;
  height: 15px;
  cursor: pointer;
}

.vote-style:hover {
  filter: brightness(110%);
}

.userimg {
  width: 50px;
  height: 50px;
  margin-right: 20px;
  border-radius: 50%;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.delete-comment {
  text-align: right;
  cursor: pointer;
}

.add_comment {
  width: 100%;
  height: 100%;
  font-size: 14px;
  font-weight: bold;
  color: #333;
  background-color: #cce5ff;
  border: none;
}

.message-username {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.message-list-username {
  font-size: 15px;
  font-weight: bold;
  color: #333;
}

.vip-style {
  font-size: 16px;
  font-weight: bold;
  color: rgba(255, 234, 18, 0.75);
}

#reply-button {
  cursor: pointer;
}

.modal-reply-message {
  padding: 0 2px;
  margin: 2px;
}

.modal-each-message {
  padding: 0 2px;
}

.modal-zone {
  display: flex;
  justify-content: space-between;
}

div .row3 {
  padding-top: 2px;
}

#comment {
  margin: 12px 0;
}
</style>
