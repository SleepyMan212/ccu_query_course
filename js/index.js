Vue.component('coursebox',{
  template:'#course',
  props:['course'],
  mounted:()=>{
    // console.log(this.course)
  }
});
const vm = new Vue({
  el:'#app',
  data:{
    faculties:['全部','文學院','理學院','社科院','工學院','管學院','法學院','教育學院','其他'],
    departments:[],
    codes:[],
    courses:[],
    faculty:'0',
    department:'0',
    filter:'',
  },
  mounted:function() {
    $.getJSON("code_table.json").then((res)=>{
      this.codes = res;
      console.log("code read sucessly");
    });
    $.getJSON("courses.json").then((res)=>{
      this.courses = res
      console.log("courses read sucessly");
    });
  },
  methods:{
    change_faculty_state(id){

      this.department='0';
      this.faculty = id;

      let $opt = $('.opt');

      this.remove_class($opt);

      $opt = $($opt.get(id));
      $opt.addClass('highlight');
    },
    change_department_state(id){
      this.department = this.codes[id];
      // console.log(this.department);
      let $opt = $('.departments .opt');
      // let $opt = $(`.opt:contains(${id})`);
      console.log($opt);
      this.remove_class($opt);

      $opt = $(`.opt:contains(${id})`);
      $opt.addClass('highlight');
    },
    remove_class(target){
      Array.from(target).forEach((i)=>{
        // console.log(i);
        $(i).removeClass('highlight');
      });
    },
  },
  computed:{
    filter_courses:function () {
      let results=[];
      this.departments=[];
      for(department in this.courses){
        if((!(department.match(new RegExp('^[a-z]','i'))&&this.faculty=='8'))&&(this.faculty!=department[0])&&this.faculty!='0') continue;
        if(this.faculty!='0'){
          this.departments.push(this.codes[department]);
        }
        if(department!=this.department&&this.department!='0') continue;
        this.courses[department].forEach((course)=>{
          const flag = course.class_name.toLowerCase().indexOf(this.filter.toLowerCase());
          if(flag!=-1){
            course['department'] = this.codes[department];
            results.push(course);
          }
        });
      }
      return results;
    },
  }
});
