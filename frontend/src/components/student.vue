<template>
  <div>
    <el-container>
      <el-aside>
        <!-- <h3 >学生选课</h3> -->
        <el-menu
          :default-active="form"
          class="el-menu-vertical-demo"
          @select="handleSelect"
        >
          <el-menu-item index="1">
            <i class="el-icon-location"></i>
            <span slot="title">学生详细信息</span>
          </el-menu-item>
          <el-menu-item index="2">
            <i class="el-icon-menu"></i>
            <span slot="title">已选修课程成绩</span>
          </el-menu-item>
          <el-menu-item index="3">
            <i class="el-icon-document"></i>
            <span slot="title">可选课程</span>
          </el-menu-item>
          <el-menu-item index="4">
            <i class="el-icon-setting"></i>
            <span slot="title">已选课程</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-main>

        <!-- <h1>我是内容{{form}}</h1> -->
        <!-- <p v-if="form==='1'">nihao</p>
        <p v-if="form==='2'">buhao</p>-->
        <el-card
          class="box-card"
          v-if="form==='1'"
        >
          <div
            slot="header"
            class="clearfix"
          >
            <span>卡片名称</span>
          </div>
          <div class="text item">姓名：{{info[1]}}</div>
          <div class="text item">学号：{{info[0]}}</div>
          <div class="text item">年龄：{{info[3]}}</div>
          <div class="text item">性别：{{info[2]}}</div>
          <div class="text item">所在院系：{{info[4]}}</div>

        </el-card>
        <el-table
          :data="tableData"
          style="width: 100%"
          v-if="form==='2'"
        >
          <el-table-column
            prop="date"
            label="课程号"
            width="180"
          >
          </el-table-column>
          <el-table-column
            prop="name"
            label="课程名"
            width="180"
          >
          </el-table-column>
          <el-table-column
            prop="address"
            label="成绩"
          >
          </el-table-column>
        </el-table>

        <el-form
          ref="form"
          :model="form"
          label-width="80px"
          v-if="form==='3'"
        >
          <el-row>
            <el-col :span="10">
              <el-form-item label="选课：">
                <el-input
                  placeholder="请输入课程号"
                  clearable
                  prefix-icon="el-icon-search"
                  v-model="input21"
                ></el-input>
              </el-form-item>
            </el-col>
            <el-col
              :span="8"
              class='botton_boder'
            >
              <el-button plain>选课</el-button>
            </el-col>
          </el-row>
        </el-form>
        <el-table
          :data="tableData"
          style="width: 100%"
          v-if="form==='3'"
        >
          <el-table-column
            prop="date"
            label="课程号"
            width="100"
          >
          </el-table-column>
          <el-table-column
            prop="name"
            label="课程名"
            width="100"
          >
          </el-table-column>
          <el-table-column
            prop="name"
            label="学分"
            width="100"
          >
          </el-table-column>
          <el-table-column
            prop="name"
            label="开课系"
            width="100"
          >
          </el-table-column>

          <el-table-column
            prop="address"
            label="任课教师"
          >
          </el-table-column>
        </el-table>
        <el-form
          ref="form"
          :model="form"
          label-width="80px"
          v-if="form==='4'"
        >
          <el-row>
            <el-col :span="10">
              <el-form-item label="退课：">
                <el-input
                  placeholder="请输入课程号"
                  clearable
                  prefix-icon="el-icon-search"
                  v-model="input21"
                ></el-input>
              </el-form-item>
            </el-col>
            <el-col
              :span="8"
              class='botton_boder'
            >
              <el-button plain>退课</el-button>
            </el-col>
          </el-row>
        </el-form>

        <el-table
          :data="tableData"
          style="width: 100%"
          v-if="form==='4'"
        >
          <el-table-column
            prop="date"
            label="备注"
            width="50"
          >
          </el-table-column>
          <el-table-column
            prop="date"
            label="课程号"
            width="100"
          >
          </el-table-column>
          <el-table-column
            prop="name"
            label="课程名"
            width="100"
          >
          </el-table-column>
          <el-table-column
            prop="name"
            label="学分"
            width="100"
          >
          </el-table-column>
          <el-table-column
            prop="name"
            label="开课系"
            width="100"
          >
          </el-table-column>

          <el-table-column
            prop="address"
            label="任课教师"
          >
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </div>

</template>

<script>
export default {
  name: "student",
  data() {
    return {
      info: [],
      msg: "Welcome to Your Vue.js App",
      form: "1",
      input21: "",
      input22: "",
      tableData: [
        {
          date: "2016-05-02",
          name: "沙雕hch",
          address: "100"
        },
        {
          date: "2016-05-04",
          name: "沙雕洋",
          address: "100"
        },
        {
          date: "2016-05-01",
          name: "沙雕鹿",
          address: "100"
        },
        {
          date: "2016-05-03",
          name: "沙雕刚",
          address: "100"
        }
      ]
    };
  },
  methods: {
    handleSelect(index) {
      this.form = index;
    }
  },
  created() {
    this.$axios
      .post(this.$url + "sdata")
      .then(res => {
        console.log(res.data.info);
        this.info = res.data.info[0];
      })
      .catch(err => {
        console.log(err);
      });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both;
}

.box-card {
  width: 480px;
}

.botton_boder {
  padding: 0px 40px 10px;
}
</style>
