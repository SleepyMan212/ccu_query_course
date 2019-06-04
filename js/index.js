Vue.component('coursebox', {
  template: '#course',
  props: ['course'],
  mounted: () => {
  },
  data: () => {
    return {
      grade_color: ['rgb(255, 128, 1)', 'rgb(111, 255, 0)', 'rgb(0, 165, 255)', 'rgb(247, 0, 255)']
    };
  },
  methods: {
    outline() {
      return this.course.outline;
    },
    color() {
      let font_color = "color: ";
      return font_color + this.grade_color[parseInt(this.course.grade) - 1];
    },
    ccuplus() {
      return 'https://ccu.plus/#!/courses/' + this.course.class_id;
    },
  }
});
const vm = new Vue({
  el: '#app',
  data: {
    faculties: ['全部', '文學院', '理學院', '社科院', '工學院', '管學院', '法學院', '教育學院', '其他'],
    departments: [],
    grades: ['0', '1', '2', '3', '4'],
    directions: ['中國語文知識與應用', '英文能力訓練', '基礎概論課程', '自然科學與技術', '公民與社會參與', '經濟與國際脈動', '能源、環境與生態', '人文思維與生命探索', '藝術與美學',
      '中正講座'
    ],
    codes: [],
    courses:{},
    faculty: '0',
    department: '0',
    grade: '0',
    direction: '0',
    filter: '',
    is_read: false,
    query_options: ['課程名稱', '老師名稱','課程代碼'],
    query_transalte: {
      '課程名稱': 'class_name',
      '老師名稱': 'teacher',
      '課程代碼': 'class_id'
    },
    selected: '老師名稱',
  },
  mounted: function () {
    $.getJSON("code_table.json").then((res) => {
      this.codes = res;
      console.log("code read sucessly");
    })
    // .then(()=>{
    //   Object.keys(this.codes).forEach((key)=>{
    //     if(key.match(new RegExp('[a-zA-Z0-9]{4}','i'))) {
    //       $.getJSON("./courses_data/"+key+".json").then((res)=>{
    //         this.courses[`${key}`] = res;
    //
    //       })
    //     }
    //   })
    // })
    // .then(()=>{
    //     console.log("courses read sucessly");
    //     this.is_read = true;
    // });
    $.getJSON("courses.json").then((res) => {
      this.courses = res
      console.log("courses read sucessly");
    });
    // console.log(this.query_transalte['課程名稱']);
  },
  methods: {
    change_faculty_state(id) {

      this.department = '0';
      this.grade = '0';
      this.faculty = id;

      let $opt = $('.opt');

      // remove the all highlight of options
      this.remove_class($opt);

      $opt = $($opt.get(id));
      $opt.addClass('highlight');

      // show the the Faulting of departments
      this.departments = [];    // init
      for (department in this.courses) {
          if ((!(department.match(new RegExp('^[a-z]', 'i')) && this.faculty == '8')) && (this.faculty != department[0]) || this.faculty == '0') continue;

          this.departments.push(this.codes[department]);

      }
    },
    change_department_state(id) {
      this.department = this.codes[id];
      this.grade = '0';
      let $opt = $('.departments>.opt');
      this.remove_class($opt);
      // 下面的選項(年級)
      // remove the direction and grade highlight
      let $sub1_opt = $('.directions>.opt');
      this.remove_class($sub1_opt);
      let $sub2_opt = $('.grades>.opt');
      this.remove_class($sub2_opt);

      $opt = $(`.opt:contains(${id})`);

      // add highlight at the select option
      $opt.each((i, o) => {
        if (o.innerText == id) {
          $(o).addClass('highlight');
        }
      });

    },
    remove_class(target) {
      Array.from(target).forEach((i) => {
        $(i).removeClass('highlight');
      });
    },
    change_grade_state(grade) {
      let $opt = $('.grades>.opt');
      this.grade = grade;
      this.remove_class($opt);

      let $grade = $($opt.get(grade));
      $grade.addClass('highlight');
    },
    change_direction_state(index, direction) {
      let $opt = $('.directions>.opt');

      this.remove_class($opt);
      // this.department='0';
      this.direction = direction;
      // console.log(direction);
      // console.log(this.direction);
      let $direction = $($opt.get(index));
      $direction.addClass('highlight')
    }

  },
  computed: {
    filter_courses: function () {
      let results = this.courses;
      results = [];
      // 要用哪一個項目來查詢
      const query_item = this.query_transalte[this.selected];
      // if(this.is_read === true){
      //     this.selected = '課程名稱',
      //     this.is_read = false;
      //
      // }
      for (department in this.courses) {
        // 如果不符合的系 或者 不是全部的 就跳過
        if (department != this.department && this.department != '0') continue;
        // console.log(this.department);
        // console.log(this.courses);

        this.courses[department].forEach((course) => {
          if (this.department == 'I001') {
            // 如果是第一次，就全部顯示出來，因為初始化為0
            if (this.direction == '0') flag1 = false;
            else {
              flag1 = course.direction.indexOf(this.direction) != -1 ? false : true;
            }
          } else {
            // 判斷年級是否有被選取
            flag1 = course.grade != this.grade && this.grade != '0';
          }
          // 判斷是否有用關鍵字進行查詢
          const flag2 = course[query_item].toLowerCase().indexOf(this.filter.toLowerCase());
          if (flag2 != -1 && !flag1) {
            course['department'] = this.codes[department];
            results.push(course);
          }
        });
      }
      return results;
    },
  }
});
