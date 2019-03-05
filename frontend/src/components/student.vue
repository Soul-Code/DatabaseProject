<!-- 这是student.vue的全部  -->
import { stringify } from 'querystring';
<template>
  <div>
    <el-container>
      <el-aside>
        <!-- <h3 >学生选课</h3> -->
        <el-menu :default-active="form" class="el-menu-vertical-demo" @select="handleSelect">
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
        <el-card class="box-card" v-if="form==='1'">
          <div slot="header" class="clearfix">
            <span>卡片名称</span>
          </div>
          <div class="text item">姓名：{{info[1]}}</div>
          <div class="text item">学号：{{info[0]}}</div>
          <div class="text item">年龄：{{info[3]}}</div>
          <div class="text item">性别：{{info[2]}}</div>
          <div class="text item">所在院系：{{info[4]}}</div>
          <!-- !!!!!!!!!!!!!!!!!!!!!!! -->
        </el-card>
        <el-table :data="HistoryScore" style="width: 100%" v-if="form==='2'">
          <el-table-column prop="kh" label="课程号" width="180"></el-table-column>
          <el-table-column prop="km" label="课程名" width="180"></el-table-column>
          <el-table-column prop="cj" label="成绩"></el-table-column>
        </el-table>
        <el-card v-if="form==='2'" style="margin-top:20px;font-size:35px">平均成绩：{{ avg }}</el-card>

        <el-form ref="form" label-width="80px" v-if="form==='3'">
          <el-row>
            <el-col :span="10">
              <el-form-item label="选课：">
                <el-input
                  placeholder="请输入课程号"
                  clearable
                  prefix-icon="el-icon-search"
                  v-model="is_add_corses"
                ></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8" class="botton_boder">
              <el-button @click="add_corses" plain>选课</el-button>
            </el-col>
          </el-row>
        </el-form>
        <el-table :data="tableData" style="width: 100%" v-if="form==='3'">
          <el-table-column prop="cno" label="课程号" width="100"></el-table-column>
          <el-table-column prop="cname" label="课程名" width="100"></el-table-column>
          <el-table-column prop="credit" label="学分" width="100"></el-table-column>
          <el-table-column prop="cdept" label="开课系" width="100"></el-table-column>

          <el-table-column prop="tname" label="任课教师"></el-table-column>
        </el-table>
        <el-form ref="form" label-width="80px" v-if="form==='4'">
          <el-row>
            <el-col :span="10">
              <el-form-item label="退课：">
                <el-input
                  placeholder="请输入课程号"
                  clearable
                  prefix-icon="el-icon-search"
                  v-model="is_delete"
                ></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8" class="botton_boder">
              <el-button @click="delete_courses" plain>退课</el-button>
            </el-col>
          </el-row>
        </el-form>

        <el-table :data="HistoryData" style="width: 100%" v-if="form==='4'">
          <el-table-column prop="cno" label="课程号" width="100"></el-table-column>
          <el-table-column prop="cname" label="课程名" width="100"></el-table-column>
          <el-table-column prop="credit" label="学分" width="100"></el-table-column>
          <el-table-column prop="cdept" label="开课系" width="100"></el-table-column>

          <el-table-column prop="tname" label="任课教师"></el-table-column>
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
      is_add_corses: "",
      is_delete: "",
      HistoryData: [],
      HistoryScore: [],
      tableData: [],
      avg: 0
    };
  },
  methods: {
    handleSelect(index) {
      this.form = index;
    },

    add_corses() {
      this.$axios
        .post(this.$url + "add_corses", {
          cno: this.is_add_corses
        })
        .then(res => {
          console.log(res);
          this.$notify({
            title: "保存成功",
            type: "success"
          });
        })
        .catch(err => {
          console.log(err);
        });
    },
    delete_courses() {
      this.$axios
        .post(this.$url + "delete_courses", {
          cno: this.is_delete
        })
        .then(res => {
          console.log(res);
          this.$notify({
            title: "保存成功",
            type: "success"
          });
        })
        .catch(err => {
          console.log(err);
        });
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
  },
  // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  watch: {
    form(newValue, oldValue) {
      console.log(newValue, oldValue);
      if (newValue == "2") {
        this.HistoryScore = [];
        var sum = 0;
        var num = 0;
        this.$axios
          .post(this.$url + "get_HistoryScore")
          .then(res => {
            console.log(res.data.HistoryScores);
            for (let i = 0; i < res.data.HistoryScore.length; i++) {
              const element = res.data.HistoryScore[i];
              if (element[2] != "-1") {
                this.HistoryScore.push({
                  kh: element[0],
                  km: element[1],
                  cj: element[2]
                });
                sum += element[2];
                num++;
              }
            }
            this.avg = sum / num;
          })
          .catch();
      }
      if (newValue == "3") {
        this.tableData = [];
        this.$axios
          .post(this.$url + "get_selected_courses")
          .then(res => {
            console.log(res.data.selected_courses);
            for (let i = 0; i < res.data.selected_courses.length; i++) {
              const element = res.data.selected_courses[i];
              this.tableData.push({
                cno: element[0],
                cname: element[1],
                credit: element[2],
                cdept: element[3],
                tname: element[4]
              });
            }
          })
          .catch();
      } else if (newValue == "4") {
        this.HistoryData = [];
        this.$axios
          .post(this.$url + "get_history_courses")
          .then(res => {
            console.log(res.data.history_courses);
            for (let i = 0; i < res.data.history_courses.length; i++) {
              const element = res.data.history_courses[i];
              this.HistoryData.push({
                cno: element[0],
                cname: element[1],
                credit: element[2],
                cdept: element[3],
                tname: element[4]
              });
            }
          })
          .catch();
      }
    }
  }
};
</script>


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
