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
      <chart
        v-show="form==='3'"
        :options="echarts_option"
        style="width:800px;height:600px"
        ref="chart1"
      ></chart>
      <el-tabs type="border-card" v-if="form==='4'" v-on:show="student_show">
        <el-tab-pane label="学生表维护">
          <el-button v-if="edit" class="btm-btn" type="success" @click="save('student')">保存</el-button>
          <el-button v-if="!edit" class="btm-btn" type="primary" @click="editable">修改</el-button>
          <el-button class="btm-btn" type="danger" @click="del('student')">删除</el-button>
          <el-button class="btm-btn" type="warning" @click="dialogNewStudentVisible=true">增加</el-button>
          <el-table :data="studentData" stripe style="width:100%">
            <el-table-column
              v-for="item in student_index"
              :key="item[0]"
              :prop="item[0]"
              :label="item[1]"
            >
              <template slot-scope="scope">
                <el-checkbox v-if="item[1]=='学号'" v-model="scope.row.del"></el-checkbox>
                <el-input v-model="scope.row[item[0]]" v-if="edit" type="text"></el-input>
                <span v-else>{{scope.row[item[0]]}}</span>
              </template>
            </el-table-column>
            <!-- <el-table-column prop="sno" label="学号" width="60"></el-table-column>
            <el-table-column prop="sname" label="姓名"></el-table-column>
            <el-table-column prop="sex" label="性别"></el-table-column>
            <el-table-column prop="age" label="年龄"></el-table-column>
            <el-table-column prop="sdept" label="专业"></el-table-column>
            <el-table-column prop="logn" label="用户名"></el-table-column>
            <el-table-column prop="pswd" label="密码"></el-table-column>-->
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="课程表维护">
          <el-button v-if="edit" class="btm-btn" type="success" @click="save('courses')">保存</el-button>
          <el-button v-if="!edit" class="btm-btn" type="primary" @click="editable">修改</el-button>
          <el-button class="btm-btn" type="danger" @click="del('courses')">删除</el-button>
          <el-button class="btm-btn" type="warning" @click="dialogNewCourseVisible=true">增加</el-button>
          <el-table :data="courseData" stripe style="width:100%">
            <el-table-column
              v-for="item in course_index"
              :key="item[0]"
              :prop="item[0]"
              :label="item[1]"
            >
              <template slot-scope="scope">
                <el-checkbox v-if="item[1]=='课号'" v-model="scope.row.del"></el-checkbox>
                <el-input v-model="scope.row[item[0]]" v-if="edit" type="text"></el-input>
                <span v-else>{{scope.row[item[0]]}}</span>
              </template>
            </el-table-column>
            <!-- <el-table-column prop="cno" label="课号" width="60"></el-table-column>
            <el-table-column prop="cname" label="课名"></el-table-column>
            <el-table-column prop="credit" label="学分"></el-table-column>
            <el-table-column prop="cdept" label="系别"></el-table-column>
            <el-table-column prop="tname" label="教师名"></el-table-column>-->
          </el-table>
        </el-tab-pane>
        <el-dialog title="新增学生" :visible.sync="dialogNewStudentVisible">
          <el-form :model="StudentNew">
            <el-form-item label="学号" label-width="50px">
              <el-input v-model="StudentNew.sno" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="姓名" label-width="50px">
              <el-input v-model="StudentNew.name" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="性别" label-width="50px">
              <el-select v-model="StudentNew.sex" placeholder="性别">
                <el-option label="男" value="男"></el-option>
                <el-option label="女" value="女"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="年龄" label-width="50px">
              <el-input v-model="StudentNew.age" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="专业" label-width="50px">
              <el-input v-model="StudentNew.sdept" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="用户名" label-width="50px">
              <el-input v-model="StudentNew.logn" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="密码" label-width="50px">
              <el-input v-model="StudentNew.pswd" autocomplete="off"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogNewStudentVisible = false">取 消</el-button>
            <el-button type="primary" @click="create('student')">确 定</el-button>
          </div>
        </el-dialog>
        <el-dialog title="新增课程" :visible.sync="dialogNewCourseVisible">
          <el-form :model="CourseNew">
            <el-form-item label="课号" label-width="50px">
              <el-input v-model="CourseNew.cno" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="课名" label-width="50px">
              <el-input v-model="CourseNew.name" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="学分" label-width="50px">
              <el-input v-model="CourseNew.credit" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="专业" label-width="50px">
              <el-input v-model="CourseNew.cdept" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="教师名" label-width="50px">
              <el-input v-model="CourseNew.tname" autocomplete="off"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogNewCourseVisible = false">取 消</el-button>
            <el-button type="primary" @click="create('courses')">确 定</el-button>
          </div>
        </el-dialog>
      </el-tabs>
    </el-main>
  </el-container>
</template>

<script>
import echarts from "echarts";
export default {
  data() {
    return {
      student_index: [
        ["sno", "学号"],
        ["sname", "姓名"],
        ["sex", "性别"],
        ["age", "年龄"],
        ["sdept", "专业"],
        ["logn", "用户名"],
        ["pswd", "密码"]
      ],
      course_index: [
        ["cno", "课号"],
        ["cname", "课名"],
        ["credit", "学分"],
        ["cdept", "系别"],
        ["tname", "教师名"]
      ],
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
      studentData: [],
      courseData: [],
      edit: false,

      dialogNewStudentVisible: false,
      dialogNewCourseVisible: false,
      StudentNew: {},
      CourseNew: {},

      echarts_option: {
        title: [
          {
            text: "成绩分布",
            left: "auto",
            top: "auto",
            textStyle: {
              fontSize: 18
            }
          }
        ],
        toolbox: {
          show: true,
          orient: "vertical",
          left: "95%",
          top: "center",
          feature: {
            saveAsImage: {
              show: true,
              title: "save as image"
            },
            restore: {
              show: true,
              title: "restore"
            },
            dataView: {
              show: true,
              title: "data view"
            }
          }
        },
        series_id: 4734126,
        tooltip: {
          trigger: "item",
          triggerOn: "mousemove|click",
          axisPointer: {
            type: "line"
          },
          textStyle: {
            fontSize: 14
          },
          backgroundColor: "rgba(50,50,50,0.7)",
          borderColor: "#333",
          borderWidth: 0
        },
        series: [
          {
            type: "bar",
            name: "平均成绩",
            color: "#66CCCC",
            data: [74.75, 69.25, 79.0, 78.0, 66.0, 88.0],
            barCategoryGap: "40%",
            label: {
              normal: {
                show: false,
                position: "top",
                textStyle: {
                  fontSize: 12
                }
              },
              emphasis: {
                show: true,
                textStyle: {
                  fontSize: 12
                }
              }
            },
            markPoint: {
              data: []
            },
            markLine: {
              data: []
            },
            seriesId: 4734126
          }
        ],
        legend: [
          {
            data: ["平均成绩"],
            selectedMode: "multiple",
            show: true,
            left: "center",
            top: "top",
            orient: "horizontal",
            textStyle: {
              fontSize: 12
            }
          }
        ],
        animation: true,
        xAxis: [
          {
            show: true,
            nameLocation: "middle",
            nameGap: 25,
            nameTextStyle: {
              fontSize: 14
            },
            axisTick: {
              alignWithLabel: false
            },
            inverse: false,
            boundaryGap: true,
            type: "category",
            splitLine: {
              show: false
            },
            axisLine: {
              lineStyle: {
                width: 1
              }
            },
            axisLabel: {
              interval: "auto",
              rotate: 0,
              margin: 8,
              textStyle: {
                fontSize: 12
              }
            },
            data: [
              "PASCAL",
              "\u6570\u636e\u7ed3\u6784",
              "\u79bb\u6563\u6570\u5b66",
              "\u8ba1\u7b97\u673a\u539f\u7406",
              "Windows\u6280\u672f",
              "\u7f16\u8bd1\u539f\u7406"
            ]
          }
        ],
        yAxis: [
          {
            show: true,
            nameLocation: "middle",
            nameGap: 25,
            nameTextStyle: {
              fontSize: 14
            },
            axisTick: {
              alignWithLabel: false
            },
            inverse: false,
            boundaryGap: true,
            type: "value",
            splitLine: {
              show: true
            },
            axisLine: {
              lineStyle: {
                width: 1
              }
            },
            axisLabel: {
              interval: "auto",
              formatter: "{value} ",
              rotate: 0,
              margin: 8,
              textStyle: {
                fontSize: 12
              }
            }
          }
        ],
        color: [
          "#c23531",
          "#2f4554",
          "#61a0a8",
          "#d48265",
          "#749f83",
          "#ca8622",
          "#bda29a",
          "#6e7074",
          "#546570",
          "#c4ccd3",
          "#f05b72",
          "#ef5b9c",
          "#f47920",
          "#905a3d",
          "#fab27b",
          "#2a5caa",
          "#444693",
          "#726930",
          "#b2d235",
          "#6d8346",
          "#ac6767",
          "#1d953f",
          "#6950a1",
          "#918597",
          "#f6f5ec"
        ]
      }
    };
  },
  mounted() {
    // 这个函数在页面加载完成后首先执行
    // 下面这个代码是在服务器获取全部的课程信息存入变量来初始化课程选择框
    this.refersh();
  },
  computed: {},
  methods: {
    editable() {
      this.edit = !this.edit;
      console.log(this.edit);
    },
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
    del(what) {
      var data;
      var dataToDel = [];
      var no = "sno";
      switch (what) {
        case "student":
          data = this.studentData;
          no = "sno";
          break;
        case "courses":
          data = this.courseData;
          no = "cno";
          break;
      }
      for (let i = 0; i < data.length; i++) {
        const element = data[i];
        if (element.del === true) {
          dataToDel.push(element[no]);
        }
      }
      console.log(dataToDel, dataToDel.length);
      this.$axios
        .post(this.$url + "del", { what: what, data: dataToDel })
        .then(res => {
          console.log(res);
          this.edit = false;
          // todo
          this.$notify({
            title: "删除成功！",
            type: "success",
            offset: 70
          });
          this.dialogNewVisible = false;
          this.refersh();
        })
        .catch(err => {
          console.log(err);
          this.$notify({
            title: "删除失败……",
            message: response.data.errmsg,
            type: "error",
            offset: 70
          });
        });
    },
    create(what) {
      var data;
      switch (what) {
        case "student":
          data = this.StudentNew;
          break;
        case "courses":
          data = this.CourseNew;
          break;
      }
      this.$axios
        .post(this.$url + "new", { what: what, data: data })
        .then(res => {
          console.log(res);
          this.edit = false;
          // todo
          this.$notify({
            title: "新增成功！",
            type: "success",
            offset: 70
          });
          this.refersh();
          this.dialogNewStudentVisible = false;
          this.dialogNewCourseVisible = false;
        })
        .catch(err => {
          console.log(err);
          this.$notify({
            title: "新增失败……",
            message: response.data.errmsg,
            type: "error",
            offset: 70
          });
        });
    },
    save(what) {
      var data;
      switch (what) {
        case "student":
          data = this.studentData;
          break;
        case "courses":
          data = this.courseData;
          break;
      }
      this.$axios
        .post(this.$url + "save", { what: what, data: data })
        .then(res => {
          console.log(res);
          this.edit = false;
          // todo
          this.$notify({
            title: "保存成功！",
            type: "success",
            offset: 70
          });
        })
        .catch(err => {
          console.log(err);
          this.$notify({
            title: "保存失败……",
            message: response.data.errmsg,
            type: "error",
            offset: 70
          });
        });
    },
    student_show() {
      console.log("显示了学生维护界面");
    },
    refersh() {
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

          this.$axios
            .post(this.$url + "get_courses")
            .then(res => {
              // 获取到后端数据
              console.log(res);
              // 初始化一个数组变量。用来初始化选择框。
              var options = new Array(res.data.courses.length);
              var courseData = new Array(res.data.courses.length);
              // 循环给这个变量赋值
              for (let index = 0; index < res.data.courses.length; index++) {
                const element = res.data.courses[index];
                // console.log(element);
                options[index] = { label: element[1], value: element[0] };
                courseData[index] = {
                  cno: element[0],
                  cname: element[1],
                  credit: element[2],
                  cdept: element[3],
                  tname: element[4]
                };
              }
              this.options = options;
              this.courseData = courseData;
            })
            .catch(err => {
              console.log(err);
            });
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  watch: {
    form(newValue, oldValue) {
      if (newValue == "4") {
        this.refersh();
      } else if (newValue == "3") {
        this.$axios
          .post(this.$url + "echarts")
          .then(res => {
            console.log(res);
            this.echarts_option.xAxis.data = res.data.key;
            this.echarts_option.series[0].data = res.data.value;
            // todo
          })
          .catch(err => {
            console.log(err);
            this.$notify({
              title: "获取数据失败……",
              message: response.data.errmsg,
              type: "error",
              offset: 70
            });
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
