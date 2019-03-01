<template>
  <el-container>
    <el-aside width="200px">
      <el-menu :default-active="form" class="el-menu-vertical-demo" @select="handleSelect">
        <el-menu-item index="1">
          <i class="el-icon-location"></i>
          <span slot="title">成绩查询</span>
        </el-menu-item>
        <el-menu-item index="2">
          <i class="el-icon-menu"></i>
          <span slot="title">成绩录入</span>
        </el-menu-item>
        <el-menu-item index="3">
          <i class="el-icon-document"></i>
          <span slot="title">成绩分布</span>
        </el-menu-item>
        <el-menu-item index="4">
          <i class="el-icon-setting"></i>
          <span slot="title">数据表维护</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main>
      <div v-show="form==='1' || form==='2'">
        <div class="block">
          <span class="demonstration" style="margin-right:15px">请选择课程进行操作:</span>
          <el-select placeholder="单击此处可搜索" v-model="course" @change="handleCourseChange" filterable>
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
          <el-button
            v-if="form==='2'"
            type="primary"
            style="margin-left:10px"
            @click="save_score"
          >保存</el-button>
        </div>
        <el-table :data="scoreData" stripe border class="table-score">
          <el-table-column prop="sno" label="学号"></el-table-column>
          <el-table-column prop="name" label="姓名"></el-table-column>
          <el-table-column prop="score" label="成绩">
            <template slot-scope="scope">
              <el-input
                v-model="scope.row.score"
                v-if="form==='2'"
                @change="handleScoreChange"
                type="number"
              ></el-input>
              <span v-else>{{scope.row.score}}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <el-tabs type="border-card" v-if="form==='4'" v-on:show="student_show">
        <el-tab-pane label="学生表维护">
          <el-button class="btm-btn" type="success">保存</el-button>
          <el-button class="btm-btn" type="primary">修改</el-button>
          <el-table :data="studentData" stripe style="width:100%">
            <el-table-column prop="sno" label="学号"></el-table-column>
            <el-table-column prop="sname" label="姓名"></el-table-column>
            <el-table-column prop="sex" label="性别"></el-table-column>
            <el-table-column prop="age" label="年龄"></el-table-column>
            <el-table-column prop="sdept" label="专业"></el-table-column>
            <el-table-column prop="logn" label="用户名"></el-table-column>
            <el-table-column prop="pswd" label="密码"></el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="课程表维护">课程表维护</el-tab-pane>
      </el-tabs>
    </el-main>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      form: "1",
      course: [],
      options: [
        {
          value: "zhinan",
          label: "计算机组成原理"
        },
        {
          value: "zujian",
          label: "操作系统"
        },
        {
          value: "ziyuan",
          label: "数据库"
        }
      ],
      haschenged: false,
      scoreData: [],
      studentData: []
    };
  },
  mounted() {
    this.$axios
      .post(this.$url + "get_courses")
      .then(res => {
        console.log(res);
        var options = new Array(res.data.courses.length);
        for (let index = 0; index < res.data.courses.length; index++) {
          const element = res.data.courses[index];
          // console.log(element);
          options[index] = { label: element[0], value: element[1] };
        }
        this.options = options;
      })
      .catch(err => {
        console.log(err);
      });
  },
  computed: {},
  methods: {
    handleSelect(index) {
      this.form = index;
    },
    handleCourseChange(val) {
      this.$axios
        .post(this.$url + "get_score", { cno: val })
        .then(res => {
          var students = res.data.students;
          var scoreData = Array(students.length);
          // console.log(students);
          for (let i = 0; i < students.length; i++) {
            const element = students[i];
            scoreData[i] = {
              name: element[0],
              score: element[1],
              sno: element[2]
            };
          }
          this.scoreData = scoreData;
          this.haschenged = false;
        })
        .catch(err => {
          console.log(err);
        });
    },
    handleScoreChange(val) {
      this.haschenged = true;
    },
    save_score() {
      this.$axios
        .post(this.$url + "save_score", {
          datas: this.scoreData,
          cno: this.course
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
    student_show() {
      console.log("显示了学生维护界面");
    }
  },
  watch: {
    form(newValue, oldValue) {
      if (newValue == "4") {
        this.$axios
          .post(this.$url + "get_students")
          .then(res => {
            var studentData = Array(res.data.info.length);
            for (let i = 0; i < res.data.info.length; i++) {
              const element = res.data.info[i];
              console.log(element);
              studentData[i] = {
                sno: element[0],
                sname: element[1],
                sex: element[2],
                age: element[3],
                sdept: element[4],
                logn: element[5],
                pswd: element[6]
              };
            }
            this.studentData = studentData;
          })
          .catch(err => {
            console.log(err);
          });
      }
    }
  }
};
</script>

<style>
.block {
  margin: 0px 20px 20px 20px;
}
.table-score {
  width: 390px;
  margin-left: 20px;
}
.btm-btn {
  float: right;
  margin: 0 10px;
}
</style>
