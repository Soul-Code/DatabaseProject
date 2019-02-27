<template>
  <el-row>
    <el-col
      :xl={span:6,offset:9}
      :lg={span:6,offset:9}
      :md={span:12,offset:6}
      :sm={span:12,offset:6}
    >
      <el-card style="padding:0 12px 12px 12px;margin-top:70px">
        <el-form
          ref="form"
          :model="form"
          label-width="80px"
        >
          <h1 style="text-align:center;margin-top:0">请登陆</h1>
          <el-form-item label-width="0">
            <el-input
              v-model="form.username"
              placeholder="用户名"
              type="text"
            ></el-input>
          </el-form-item>
          <el-form-item label-width="0">
            <el-input
              v-model="form.psword"
              placeholder="密码"
              type="password"
            ></el-input>
          </el-form-item>

          <el-form-item
            label-width="0"
            style="margin:0"
          >
            <el-button
              type="primary"
              @click="onSubmit"
              style="width:100%"
            >登陆</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: "",
        psword: ""
      }
    };
  },
  mounted() {},
  computed: {},
  methods: {
    onSubmit() {
      console.log("submit!");
      let that = this;
      this.$axios
        .post(this.$url + "login", this.form)
        .then(function(response) {
          console.log(response);
          if (response.data.ok) {
            that.$notify({
              title: "登陆成功",
              message: response.data.msg,
              type: "success",
              offset: 70
            });

            that.$router.push({
              path: "/" + response.data.role
            });
          } else {
            that.$notify({
              title: "登陆失败",
              message: response.data.msg,
              type: "error",
              offset: 70
            });
          }
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>

<style>
</style>
