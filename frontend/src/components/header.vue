<template>
  <el-row
    class="container flex"
    style="background-color: #555;border-radius: 4px;box-shadow:0 2px 12px 0 rgba(0, 0, 0, 0.7)"
  >
    <!-- <el-col
      :span="6"
      style="width: 60px;"
    >
      <a href="/"><img
          src="../assets/logo.png"
          style="padding-left:8px;padding-top:5px;width:50px"
        ></a>
    </el-col> -->
    <el-col :span="6">
      <p
        href="/"
        style="color: #FFF;line-height:30px;margin-left:20px"
      >课程管理系统</p>
    </el-col>
    <el-col
      :span="2"
      :offset="16"
      :xl={span:2,offset:16}
      :lg={span:2,offset:16}
      :md={span:3,offset:15}
      :sm={span:5,offset:13}
      style="padding-right:15px"
    >
      <el-button
        type="danger"
        style="margin:10px 0 10px 0;width:100%"
        @click="logout"
      >退出登陆</el-button>
      <!-- <p style="color: #FFF;line-height:30px;margin-left:20px">老师</p> -->
    </el-col>

  </el-row>
</template>

<script>
export default {
  data() {
    return {
      activeIndex: "1"
    };
  },
  mounted() {},
  computed: {},
  methods: {
    logout() {
      let that = this;
      this.$axios
        .post(this.$url + "logout")
        .then(res => {
          console.log(res);
          that.$router.push({
            path: "/"
          });
          that.$notify({
            title: "退出登陆成功！",
            type: "success",
            offset: 70
          });
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>

<style>
</style>
