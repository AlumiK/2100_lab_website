<template>
  <body>
    <div class="remind">
      <label id="list-title">{{ course_type === 'free' ? '免费':'付费' }}
      </label>
      <div
        class="watch-more">
        <label
          id="watch-more"
          @click="watch_more">更多</label>
      </div>
    </div>
    <div
      id="course-list"
      class="course-list-style">
      <b-container
        fluid
        class="bv-example-row">
        <b-row>
          <b-col
            v-for="course in courselist"
            id="course-card"
            :key="course.course_id"
            sm="6"
            md="4"
            lg="3"
            class="col-style"
            @click="open_detail_page(course.course_id)">
            <div class="border-radius">
              <img
                :src="$store.state.address+course.thumbnail"
                class="course-image">
              <div class="padding-style">
                <h5 class="card-title">
                  {{ course.title }}
                </h5>
                <p class="card-text card-text-height">
                  {{ course.description }}
                </p>
              </div>
            </div>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </body>
</template>

<script>
export default {
  name: 'RecommendList',
  props: {
    course_type: {
      type: String,
      default: function () {
        return ''
      }
    },
    courselist: {
      type: Array,
      default: function () {
        return []
      }
    }
  },
  methods: {
    /**
     * 查看更多
     * 如果当前列表为免费列表，查看更多将跳转到全部免费课程页
     * 如果当前列表为付费列表，查看更多将跳转到全部付费课程页 */
    watch_more: function () {
      if (this.course_type === 'free') {
        this.$router.push({ name: 'AllFreeCourse' })
      } else {
        this.$router.push({ name: 'AllPaidCourse' })
      }
    },
    /**
     * 跳转课程详情页
     * 接收课程id
     * 跳转至并将id传至课程详情页 */
    open_detail_page: function (id) {
      this.$router.push({ name: 'CourseDetail', query: { course_id: id } })
    }
  }
}
</script>

<style scoped>
.padding-style {
  padding: 15px;
}

.border-radius {
  border-radius: 25px;
}

.remind {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

#list-title {
  padding-left: 1rem;
  margin-left: 1.2rem;
  font-size: 2rem;
  font-weight: bold;
  border-left: 3px solid #ccc;
}

.course-image {
  width: 100%;
  height: 100%;
  border-radius: 15px 15px 0 0;
}

#watch-more {
  padding-top: 1rem;
  padding-right: 2rem;
  font-weight: bold;
  cursor: pointer;
}

.col-style {
  flex: 1 0 20%;
  min-width: 15rem;
  min-height: 18rem;
  padding: 0;
  margin: 2rem 1.5rem;
  text-align: center;
  cursor: pointer;
  border-radius: 15px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

.col-style:hover {
  -ms-transform: translate(0, -20px); /* IE 9 */
  -webkit-transform: translate(0, -20px); /* Safari and Chrome */
  transform: translate(0, -20px);
}

p {
  word-break: break-word;
}

.card-text-height {
  max-height: 5.5rem;
  overflow: hidden;
  font-size: 15px;
  text-align: justify;
  text-indent: 2rem;
}

.card-title {
  height: 1.5rem;
  overflow: hidden;
  font-weight: bold;
}

#course-list {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
}

.course-list-style {
  margin: 0;
}
</style>
